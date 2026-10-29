# ==============================================================================
# Scene:      KLDivergenceDemo
# Source:     videos/_2026/cross_entropy/robot.py (lines 8420-8628)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl KLDivergenceDemo.py KLDivergenceDemo -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *


# ----- From _2026/cross_entropy/distribution.py -----

class StackedProbDistribution(VGroup):
    def __init__(
        self,
        distribution,
        width=12,
        height=0.5,
        fill_colors=(BLUE_E, TEAL_E),
        fill_opacity=1,
        stroke_width=1,
        stroke_color=WHITE,
        labels=None,
        label_height_ratio=0.5,
        label_width_ratio=0.8,
        fit_labels_to_height=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.distribution = distribution
        self.cdf = np.cumsum(distribution)
        self.bar_color_bounds = fill_colors
        self.label_height_ratio = label_height_ratio
        self.label_width_ratio = label_width_ratio

        # Set bars with dummy values
        self.bars = Rectangle().get_grid(1, len(distribution), buff=0)
        self.bars.set_shape(width, height)
        self.bars.set_fill(fill_colors, 1, gradient_direction=RIGHT)
        self.bars.set_stroke(stroke_color, stroke_width)

        # Initialize labels as empty
        self.labels = VGroup()

        self.add(self.bars, self.labels)

        self.set_distribution(distribution)
        self.fit_labels_to_height = fit_labels_to_height
        if labels is not None:
            self.set_labels(labels)

    def set_labels(self, labels: VMobject):
        self.labels.set_submobjects(labels)
        self.original_labels = labels.copy()
        self.reposition_labels()
        return self

    def reposition_labels(self):
        self.labels.become(self.original_labels)
        if self.fit_labels_to_height:
            self.labels.set_height(self.bars.get_height() * self.label_height_ratio)
        self.labels.move_to(self.bars)
        for label, bar in zip(self.labels, self.bars):
            label.match_x(bar)
            fill_opacity = float(label.get_width() < bar.get_width() * self.label_width_ratio)
            label.set_fill(opacity=fill_opacity)
        return self

    def set_distribution(self, distribution):
        center = self.bars.get_center().copy()
        width, height = self.bars.get_shape()[:2]
        n_bars = len(distribution)
        bar_style = self.bars[0].get_style()

        if len(self.bars) != n_bars:
            self.bars.set_submobjects(Rectangle().replicate(n_bars))

        for bar, prob in zip(self.bars, distribution):
            bar.set_shape(width * prob, height)
            bar.set_style(**bar_style)
        self.bars.arrange(RIGHT, buff=0)
        self.bars.move_to(center)
        self.bars.set_fill(self.bar_color_bounds, gradient_direction=RIGHT)

        if len(self.labels) > 0:
            self.reposition_labels()

        return self

    def highlight(self, index, color=None, other_bar_opacity=0.35, fade_labels=True):
        self.bars.set_fill(self.bar_color_bounds, opacity=other_bar_opacity, gradient_direction=RIGHT)
        self.bars[index].set_fill(color, opacity=1)
        if fade_labels:
            for idx, label in enumerate(self.labels):
                if label.get_fill_opacity() == 0:
                    op = 0
                elif idx == index:
                    op = 1
                else:
                    op = other_bar_opacity
                label.set_fill(opacity=op)
        return self

    def renormalize_around(self, index: int):
        width, height = self.get_shape()[:2]
        center = self.get_center().copy()
        bar_width = self.bars[index].get_width()
        self.bars.stretch(width / bar_width, 0)
        self.bars.shift(center - self.bars[index].get_center())
        self.reposition_labels()
        return self

    def stretch(self, factor, dim, **kwargs):
        super().stretch(factor, dim, **kwargs)
        if dim == 0:
            self.reposition_labels()
        return self

    def float_to_index(self, value: float):
        """
        Given a value in [0, 1], returns the index of the
        corresponding event from the distribution
        """
        for idx, upper_value in enumerate(self.cdf):
            if value < upper_value:
                return idx
        # Otherwise, last element
        return len(self.distribution) - 1



# ----- From _2026/cross_entropy/robot.py -----

PURE_MAGENTA = "#FF00FF"


class FancyCircumscribe(VShowPassingFlash):
    def __init__(self, mobject, time_width=1.5, run_time=3, **kwargs):
        rect = SurroundingRectangle(mobject).set_stroke(YELLOW, 3)
        rect.add_line_to(rect.get_corner(UL))
        rect.insert_n_curves(100)
        super().__init__(rect, time_width=time_width, run_time=run_time, **kwargs)


def random_distribution(n, thresh=1 / 16):
    if n <= 0:
        return []
    if n * thresh > 1:
        raise ValueError("Threshold is too high to sum to 1")
    remaining_sum = 1 - (n * thresh)
    random_parts = np.random.dirichlet(np.ones(n), size=1).flatten()
    numbers = (random_parts * remaining_sum) + thresh
    return numbers.tolist()


class EntropyChart(VGroup):
    def __init__(
        self,
        initial_distribution,
        event_labels=None,
        probability_labels="default",
        bar_labels=None,
        bar_heights=None,
        width=6,
        height=6,
        segments_height=0.5,
        stroke_width=3,
        fit_event_labels_to_height=True,
        include_vertical_axis=True,
        vertical_axis_label_text=R"\text{Information } \\ (-\log_2 p_i \text{ bits})",
        vertical_axis_font_size=42,
        fill_colors=(BLUE_E, TEAL_E),
        bar_fill_colors=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.stroke_width = stroke_width
        self.distribution_trackers = [ValueTracker(p) for p in initial_distribution]
        self.segments = StackedProbDistribution(
            initial_distribution,
            labels=event_labels,
            width=width,
            height=segments_height,
            fit_labels_to_height=fit_event_labels_to_height,
            fill_colors=(BLUE_E, TEAL_E),
            stroke_width=self.stroke_width
        )

        def update_segments(m):
            m.set_distribution([t.get_value() for t in self.distribution_trackers])
        self.segments.add_updater(update_segments)
        self.add(self.segments)
        if event_labels is not None:
            self.event_labels = self.segments.labels
        else:
            self.event_labels = None

        self.width = width
        self.height = height

        i = 0
        include_labels_every = 1
        self.include_vertical_axis = include_vertical_axis
        if self.include_vertical_axis:
            self.reference_lines = VGroup()
            while i * self.height / self.width <= self.height:
                group = VGroup()
                line = Line(
                    ORIGIN, RIGHT * self.segments.get_width(),
                    stroke_width=1.3,
                ).align_to(
                    self.segments, UL
                ).shift(
                    UP * i * self.height / self.width
                ).set_opacity(0.4)
                group.add(line)
                label = Tex(str(i), font_size=20).next_to(line)
                if i % include_labels_every == 0:
                    group.add(label)
                self.reference_lines.add(group)

                i += 1
            self.add(self.reference_lines)

        self.bar_heights = [ValueTracker(h) for h in bar_heights] if bar_heights is not None else None

        def get_bars():
            colors = fill_colors if bar_fill_colors is None else bar_fill_colors
            bars = VGroup()
            for (i, segment), t in zip(enumerate(self.segments.bars), self.distribution_trackers):
                bar_height = -math.log2(t.get_value()) if self.bar_heights is None else self.bar_heights[i].get_value()
                bar = Rectangle(
                    width=segment.get_width(),
                    height=bar_height * self.height / self.width,
                    fill_opacity=0.8,
                    fill_color=interpolate_color(colors[0], colors[1], i / (len(self.distribution_trackers) - 1))
                ).set_stroke(
                    width=self.stroke_width, color=WHITE
                ).next_to(
                    segment, UP, buff=0
                )
                bar.height = bar_height
                bars.add(bar)
            return bars
        self.bars = always_redraw(get_bars)
        self.add(self.bars)

        if bar_labels is not None:
            self.bar_labels = VGroup(*bar_labels)
            self.add(self.bar_labels)
            for i, label in enumerate(self.bar_labels):
                label.set_color(BLACK)

            def update_labels(m):
                for label, bar in zip(m, self.bars):
                    label.move_to(bar)
            self.bar_labels.add_updater(update_labels)
        else:
            self.bar_labels = None

        if probability_labels == "default":
            self.probability_labels = VGroup(*[Tex(F"p_{i}") for i in range(len(self.distribution_trackers))])
        elif probability_labels is not None:
            self.probability_labels = VGroup(*probability_labels)
        else:
            self.probability_labels = None
        if self.probability_labels is not None:
            for i, label in enumerate(self.probability_labels):
                label.set_color(interpolate_color(fill_colors[0], fill_colors[1], i / (len(self.distribution_trackers) - 1)))

            def update_labels(m):
                for label, segment in zip(m, self.segments.bars):
                    label.next_to(segment, DOWN).match_y(m[0])
            self.probability_labels.add_updater(update_labels)
            self.add(self.probability_labels)

        if self.include_vertical_axis:
            self.vertical_axis = Line(ORIGIN, UP * self.height, stroke_width=self.stroke_width).align_to(self.segments.get_corner(UL), DL)
            self.vertical_axis_label = Tex(
                vertical_axis_label_text, font_size=vertical_axis_font_size
            ).next_to(self.vertical_axis, LEFT)
            self.vertical_axis_label["Information"].match_x(self.vertical_axis_label[len("Information"):])
            self.add(self.vertical_axis, self.vertical_axis_label)

    def set_distribution(self, distribution):
        return AnimationGroup(*[
            t.animate.set_value(p)
            for p, t in zip(distribution, self.distribution_trackers)
        ])
        self.segments.set_distribution(distribution)

    def create_bars(self):
        return AnimationGroup(*[
            UpdateFromAlphaFunc(
                bar,
                lambda m, a, t=t, i=i: m.stretch_to_fit_height(
                    max(0.0001, a) * (-math.log2(t.get_value()) if self.bar_heights is None else self.bar_heights[i].get_value()) * self.height / self.width,
                    about_point=m.get_bottom()
                ).set_stroke(
                    width=self.stroke_width * a
                ),
                suspend_mobject_updating=True
            )
            for i, (bar, t) in enumerate(zip(self.bars, self.distribution_trackers))
        ], lag_ratio=0.2)

    def create_reference_lines(self):
        anims = []
        for line in self.reference_lines:
            anim = [ShowCreation(line[0])]
            if len(line) > 1:
                anim.append(Write(line[1]))
            anims.append(AnimationGroup(*anim, lag_ratio=0.8))
        return AnimationGroup(*anims, lag_ratio=0.04)

    def create(self):
        anims_1 = []
        anims_2 = []
        for i in range(len(self.segments.bars)):
            fadeins = []
            fadeins.append(FadeIn(self.segments.bars[i]))
            if self.event_labels is not None:
                fadeins.append(FadeIn(self.event_labels[i]))
            if self.probability_labels is not None:
                fadeins.append(FadeIn(self.probability_labels[i]))
            anims_1.append(AnimationGroup(*fadeins))
        anims_2.append(self.create_bars())
        if self.bar_labels is not None:
            anims_2.append(
                AnimationGroup(*[
                    FadeIn(bar_label)
                    for bar_label in self.bar_labels
                ])
            )
        if self.include_vertical_axis:
            anims_2.append(
                AnimationGroup(
                    Write(self.vertical_axis_label),
                    ShowCreation(self.vertical_axis),
                    self.create_reference_lines()
                )
            )
        return AnimationGroup(AnimationGroup(*anims_1), AnimationGroup(*anims_2, lag_ratio=0.5))


class KLDivergenceDemo(InteractiveScene):
    def construct(self):
        # Add the charts
        Q = [0.4, 0.1, 0.08, 0.15, 0.27]
        P = [0.1, 0.2, 0.3, 0.35, 0.05]

        p_entropy_chart = EntropyChart(
            P,
            event_labels=None,
            probability_labels=VGroup(*[
                Tex(
                    (("p_" + str(i + 1)) if i < len(P) - 2 else R"\ldots" if i == len(P) - 2 else "p_n"),
                    font_size=40
                )
                for i in range(len(P))
            ]),
            bar_labels=None,
            width=5,
            height=3.5,
            include_vertical_axis=False,
            segments_height=0.2,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[YELLOW_B, YELLOW_B],
            stroke_width=1
        ).shift(UP * 1.2)
        p_entropy_chart.add_updater(lambda m: m.bars.set_fill(opacity=0.1).set_stroke(width=1))
        self.add(p_entropy_chart)

        q_entropy_chart = EntropyChart(
            Q,
            event_labels=None,
            probability_labels=VGroup(*[
                Tex(
                    (("q_" + str(i + 1)) if i < len(Q) - 2 else R"\ldots" if i == len(P) - 2 else "q_n"),
                    font_size=40
                )
                for i in range(len(Q))
            ]),
            bar_labels=None,
            width=5,
            height=3.5,
            include_vertical_axis=False,
            segments_height=0.2,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            stroke_width=1
        )
        q_entropy_chart.bars.add_updater(lambda m: m.set_opacity(0))
        self.add(q_entropy_chart)
        VGroup(p_entropy_chart, q_entropy_chart).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=2)

        def get_kl_divergence_bars():
            current_distribution = [t.get_value() for t in p_entropy_chart.distribution_trackers]
            bar_heights = [math.log2(p / q.get_value()) for p, q in zip(current_distribution, q_entropy_chart.distribution_trackers)]
            bars = EntropyChart(
                current_distribution,
                event_labels=None,
                probability_labels=None,
                bar_labels=None,
                bar_heights=bar_heights,
                width=5,
                height=3.5,
                include_vertical_axis=False,
                segments_height=0.2
            ).bars.set_stroke(width=1)
            bars.clear_updaters()
            for bar, height, p_entropy_bar in zip(bars, bar_heights, p_entropy_chart.bars):
                bar.match_x(p_entropy_bar).align_to(p_entropy_bar.get_top(), DOWN)
                if height > 0:
                    bar.set_fill(color=PURE_GREEN)
                else:
                    bar.set_fill(color=PURE_RED)
            return bars
        kl_divergence_chart_bars = always_redraw(get_kl_divergence_bars)
        self.add(kl_divergence_chart_bars)

        # Add the equation
        kl_divergence_formula = Tex(
            R"\begin{gathered}\text{KL Divergence of Q relative to P:} \\ \left(\sum_i p_i(-\log_2 q_i)\right) - \left(\sum_i p_i(-\log_2 p_i)\right)\end{gathered}",
            font_size=26, tex_to_color_map={"Q": PINK, "P": GREEN, "p_i": GREEN, "q_i": PINK}
        ).next_to(p_entropy_chart, UP, buff=0.9)
        self.add(kl_divergence_formula)

        # Add Q and P symbols
        def get_kl_divergence(Q, P):
            return sum([p * math.log2(p / q) for q, p in zip(Q, P)])
        Q_symbol = Tex("Q", font_size=80).set_color(PINK).set_stroke(width=15, color=BLACK, behind=True)
        P_symbol = Tex("P", font_size=80).set_color(GREEN).set_stroke(width=15, color=BLACK, behind=True)
        VGroup(Q_symbol, P_symbol).to_edge(RIGHT, buff=3)
        multiplier = 3
        Q_symbol.add_updater(
            lambda m:
            m.set_y(
                -multiplier * get_kl_divergence(
                    [t.get_value() for t in q_entropy_chart.distribution_trackers],
                    [t.get_value() for t in p_entropy_chart.distribution_trackers]
                )
            )
        )
        P_symbol.add_updater(
            lambda m:
            m.set_y(
                multiplier * get_kl_divergence(
                    [t.get_value() for t in q_entropy_chart.distribution_trackers],
                    [t.get_value() for t in p_entropy_chart.distribution_trackers]
                )
            )
        )
        self.add(Q_symbol, P_symbol)

        # Add the connecting line
        connecting_line = always_redraw(
            lambda:
            Line(
                Q_symbol,
                P_symbol,
                stroke_width=clip(
                    1 / (
                        get_kl_divergence(
                            [t.get_value() for t in q_entropy_chart.distribution_trackers],
                            [t.get_value() for t in p_entropy_chart.distribution_trackers]
                        )
                    ),
                    0.2,
                    9
                ),
                stroke_color=BLUE_B,
                stroke_opacity=0.5
            )
        )
        self.add(connecting_line)
        connecting_line.add_updater(lambda m: self.bring_to_back(m))

        # Add Dashed lines
        dashed_lines = VGroup(*[
            DashedLine(q_entropy_chart.segments.bars.get_bottom(), p_entropy_chart.segments.bars.get_top(), stroke_width=3)
            for _ in range(len(p_entropy_chart.segments.bars) + 1)
        ]).set_color(GREY).set_opacity(0.5).align_to(q_entropy_chart.segments.bars, DOWN)
        for line, bar in zip(dashed_lines, p_entropy_chart.segments.bars):
            line.set_x(bar.get_left()[0])
        dashed_lines[-1].set_x(p_entropy_chart.segments.bars[-1].get_right()[0])
        self.add(dashed_lines)
        self.bring_to_back(dashed_lines)

        # Change the distribution
        np.random.seed(10)
        for i in range(15):
            new_distribution = random_distribution(5) if i != 1 else P
            anims = [q_entropy_chart.set_distribution(new_distribution)]
            if i == 3:
                kl_divergence_formula.save_state()
                kl_divergence_formula_2 = Tex(
                    R"\begin{gathered}\text{KL Divergence of P relative to Q:} \\ \left(\sum_i q_i(-\log_2 p_i)\right) - \left(\sum_i q_i(-\log_2 q_i)\right)\end{gathered}",
                    font_size=26, tex_to_color_map={"Q": PINK, "P": GREEN, "p_i": GREEN, "q_i": PINK}
                ).next_to(p_entropy_chart, UP, buff=1.2)
                kl_divergence_formula.generate_target()
                VGroup(kl_divergence_formula.target, kl_divergence_formula_2).scale(1.05).arrange(buff=1.3)
                rect = SurroundingRectangle(kl_divergence_formula_2, buff=0.2, stroke_width=3, stroke_color=YELLOW)
                p_entropy_chart.suspend_updating()
                charts_group = VGroup(q_entropy_chart, p_entropy_chart, kl_divergence_chart_bars, dashed_lines)
                charts_group.save_state()
                charts_group.suspend_updating()
                symbols_group = VGroup(connecting_line, Q_symbol, P_symbol)
                symbols_group.save_state()
                symbols_group.suspend_updating()
                self.play(
                    charts_group.animate(run_time=1.5).shift(DL * 2).set_opacity(0),
                    symbols_group.animate(run_time=1.5).shift(RIGHT * 2).set_opacity(0),
                    AnimationGroup(
                        MoveToTarget(kl_divergence_formula),
                        Write(kl_divergence_formula_2, run_time=2),
                        FadeIn(rect), lag_ratio=0.6, run_time=4)
                )
                self.wait(1)
                not_equal = Tex(R"\neq", font_size=50).set_color(RED).move_to(VGroup(kl_divergence_formula, kl_divergence_formula_2))
                self.play(FadeOut(rect), FadeIn(not_equal))
                self.wait(2)
                self.play(
                    FadeOut(VGroup(not_equal, kl_divergence_formula_2), shift=UP * 3 + RIGHT * 5),
                    kl_divergence_formula.animate.restore(),
                    charts_group.animate(run_time=2).shift(UR * 2).restore(),
                    symbols_group.animate(run_time=2).restore(), run_time=2)
                charts_group.resume_updating()
                symbols_group.resume_updating()
            if i == 5:
                kl_divergence_formula_compact = Tex(
                    R"= \displaystyle\sum_i p_i \left(\log_2 \frac{p_i}{q_i}\right)",
                    font_size=30, tex_to_color_map={"p_i": GREEN, "q_i": PINK}
                ).next_to(kl_divergence_formula, DOWN, buff=0.25).align_to(kl_divergence_formula, LEFT)
                anims.append(Write(kl_divergence_formula_compact))
            if i == 8:
                rect1 = SurroundingRectangle(
                    kl_divergence_formula[R"\left(\sum_i p_i(-\log_2 q_i)\right) - \left(\sum_i p_i(-\log_2 p_i)\right)"],
                    buff=0.07,
                    stroke_width=2,
                    stroke_color=YELLOW
                )
                rect2 = SurroundingRectangle(
                    kl_divergence_formula_compact,
                    buff=0.07,
                    stroke_width=2,
                    stroke_color=YELLOW
                )
                anims.append(FadeIn(VGroup(rect1, rect2)))
            if i == 10:
                anims.append(FadeOut(VGroup(kl_divergence_formula_compact, rect1, rect2)))
            if i == 11:
                anims.append(FancyCircumscribe(VGroup(p_entropy_chart, kl_divergence_chart_bars, q_entropy_chart)))
            self.play(*anims, run_time=2)
            self.wait(1)
