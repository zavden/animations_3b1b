# ==============================================================================
# Scene:      MoreComplicatedCrossEntropyExampleAndKLDivergence
# Source:     videos/_2026/cross_entropy/robot.py (lines 8140-8389)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl MoreComplicatedCrossEntropyExampleAndKLDivergence.py MoreComplicatedCrossEntropyExampleAndKLDivergence -w -m --fps 15
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


class MoreComplicatedCrossEntropyExampleAndKLDivergence(InteractiveScene):
    def construct(self):
        # Create the charts
        Q = [0.4, 0.1, 0.08, 0.15, 0.27]
        P = [0.1, 0.2, 0.3, 0.35, 0.05]
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
            height=3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"-\log_2 q_i",
            segments_height=0.2,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            stroke_width=1.5
        )
        qp_cross_entropy_chart = EntropyChart(
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
            bar_heights=[-math.log2(q) for q in Q],
            width=5,
            height=3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"-\log_2 q_i",
            segments_height=0.2,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            stroke_width=1.5
        ).shift(UP * 1.2)
        VGroup(qp_cross_entropy_chart, q_entropy_chart).set_y(0)
        self.camera.frame.save_state()
        self.camera.frame.match_y(VGroup(qp_cross_entropy_chart.segments, q_entropy_chart.segments))

        self.add(qp_cross_entropy_chart.segments, qp_cross_entropy_chart.probability_labels)
        self.add(q_entropy_chart.segments, q_entropy_chart.probability_labels)

        # Fix P and move around Q
        num_changes = 2
        for i in range(num_changes):
            anims = [q_entropy_chart.set_distribution(random_distribution(5) if i < num_changes - 1 else Q)]
            if i == 0:
                pins = VGroup(*[
                    SVGMobject("push_pin.svg").rotate(35 * DEG).scale(0.25).set_fill([GREY_D, GREY_B], 1)
                    for _ in range(len(qp_cross_entropy_chart.segments.bars))
                ])
                for pin, segment in zip(pins, qp_cross_entropy_chart.segments.bars):
                    pin.align_to(segment.get_center(), DR)
                self.bring_to_back(qp_cross_entropy_chart.segments)
                anims.append(
                    AnimationGroup(*[
                        FadeIn(pin, shift=DR * 0.25)
                        for pin in pins
                    ], lag_ratio=0.15)
                )
            self.play(*anims, run_time=2.125)

        # Add the bars and write the cross entropy formula
        number_line = NumberLine(
            [0, 5, 1],
            include_numbers=True,
            numbers_to_exclude=[1, 2, 3, 4],
            line_to_number_direction=UP,
            width=q_entropy_chart.segments.get_width()
        ).rotate(PI * 0.5).to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        for num in number_line.numbers:
            num.rotate(-90 * DEGREES)
        cross_entropy_formula = Tex(
            R"\sum_i p_i(-\log_2 q_i)", font_size=40, tex_to_color_map={"p_i": GREEN, "q_i": PINK}
        ).next_to(number_line, UP)
        cross_entropy_triangle = Triangle().set_width(0.2).set_color(GREY).set_opacity(0.8).rotate(PI * 0.5).stretch(1.4, 0)
        cross_entropy_triangle.align_to(number_line[0].get_center(), LEFT)
        cross_entropy_triangle.add_updater(
            lambda m: m.set_y(
                number_line.n2p(
                    sum([
                        p.get_value() * -math.log2(q.get_value())
                        for p, q in zip(qp_cross_entropy_chart.distribution_trackers, q_entropy_chart.distribution_trackers)
                    ])
                )[1]
            )
        )
        cross_entropy_display = Tex(R"0.00 \text{ bits}", font_size=30)
        cross_entropy_value = cross_entropy_display.make_number_changeable("0.00")
        cross_entropy_display.add_updater(lambda m: m.next_to(cross_entropy_triangle, RIGHT))
        cross_entropy_value.add_updater(
            lambda m: m.set_value(
                sum([
                    p.get_value() * -math.log2(q.get_value())
                    for p, q in zip(qp_cross_entropy_chart.distribution_trackers, q_entropy_chart.distribution_trackers)
                ])
            )
        )
        self.play(
            self.camera.frame.animate(run_time=1).restore().align_to(qp_cross_entropy_chart, LEFT).shift(LEFT * 0.7),
            qp_cross_entropy_chart.create_bars(),
            FadeOut(pins),
            ShowCreation(number_line),
            FadeIn(VGroup(cross_entropy_triangle, cross_entropy_display)),
            AnimationGroup(
                Write(qp_cross_entropy_chart.vertical_axis_label, run_time=2),
                ShowCreation(qp_cross_entropy_chart.vertical_axis),
                AnimationGroup(*[
                    ShowCreation(line)
                    for line in qp_cross_entropy_chart.reference_lines
                ], lag_ratio=0.1)
            ),
            FadeIn(cross_entropy_formula)
        )
        VGroup(
            q_entropy_chart.vertical_axis,
            q_entropy_chart.vertical_axis_label,
            q_entropy_chart.reference_lines,
            q_entropy_chart.bars
        ).set_opacity(0)
        q_entropy_chart.bars.add_updater(lambda m: m.set_opacity(0))
        self.add(
            q_entropy_chart,
            qp_cross_entropy_chart
        )

        # Change Q
        def update_qp_cross_entropy_bar_heights(m):
            for t, h in zip(q_entropy_chart.distribution_trackers, m.bar_heights):
                h.set_value(-math.log2(t.get_value()))
        qp_cross_entropy_chart.add_updater(update_qp_cross_entropy_bar_heights)
        num_changes = 3
        for i in range(num_changes):
            new_distribution = random_distribution(5) if i < num_changes - 1 else P
            self.play(q_entropy_chart.set_distribution(new_distribution), run_time=0.8 if i < 2 else 1.5)

        # Show that the distributions are now equal
        dashed_lines = Group(*[
            DashedLine(q_entropy_chart.segments.bars.get_bottom(), qp_cross_entropy_chart.segments.bars.get_top(), stroke_width=3)
            for _ in range(len(q_entropy_chart.segments.bars) + 1)
        ]).set_color(GREY).set_opacity(0.8).align_to(q_entropy_chart.segments.bars, DOWN)
        for line, bar in zip(dashed_lines, q_entropy_chart.segments.bars):
            line.set_x(bar.get_left()[0])
        dashed_lines[-1].set_x(q_entropy_chart.segments.bars[-1].get_right()[0])
        self.play(AnimationGroup(*[ShowCreation(line) for line in dashed_lines]), run_time=0.6)
        self.wait(0.1)
        self.play(AnimationGroup(*[Uncreate(line) for line in dashed_lines]), run_time=0.6)

        # Show how the expression for cross entropy is the same as that for the entropy of P when Q = P
        entropy_of_p_triangle = cross_entropy_triangle.copy().set_color(GREEN).flip().next_to(cross_entropy_triangle, LEFT, buff=0)
        entropy_of_p_triangle.clear_updaters()
        entropy_formula = Tex(
            R"\sum_i p_i (-\log_2 p_i)",
            font_size=27,
            tex_to_color_map={"p_i": GREEN}
        ).next_to(entropy_of_p_triangle, LEFT)
        entropy_formula.shift(DOWN * (entropy_formula[-1].get_y() - entropy_of_p_triangle.get_y()))
        self.play(
            AnimationGroup(
                TransformFromCopy(cross_entropy_formula, entropy_formula, path_arc=PI * 0.2),
                GrowFromEdge(entropy_of_p_triangle, RIGHT), lag_ratio=0.5), run_time=2)

        # Show some more random distributions
        for i in range(7):
            new_distribution = random_distribution(5, thresh=0)
            anims = [q_entropy_chart.set_distribution(new_distribution)]
            self.play(*anims, run_time=3)
            self.wait(0.75)

        # Transition to KL Divergence
        kl_divergence_formula = Tex(
            R"\left(\sum_i p_i(-\log_2 q_i)\right) - \left(\sum_i p_i(-\log_2 p_i)\right)",
            font_size=45, tex_to_color_map={"p_i": GREEN, "q_i": PINK}
        )
        self.play(
            self.camera.frame.animate(run_time=2).center(),
            FadeOut(cross_entropy_formula[-9:], run_time=2),
            FadeOut(
                VGroup(
                    q_entropy_chart,
                    qp_cross_entropy_chart,
                    number_line,
                    entropy_of_p_triangle,
                    cross_entropy_display,
                    cross_entropy_triangle
                ),
                shift=DOWN * 4,
                suspend_mobject_updating=True,
                run_time=2
            ),
            AnimationGroup(
                AnimationGroup(
                    TransformMatchingShapes(
                        cross_entropy_formula[R"\sum_i p_i(-\log_2 q_i)"],
                        kl_divergence_formula[R"\left(\sum_i p_i(-\log_2 q_i)\right)"], run_time=2),
                    TransformMatchingShapes(
                        entropy_formula,
                        kl_divergence_formula[R"\left(\sum_i p_i(-\log_2 p_i)\right)"], run_time=2)
                ),
                Write(kl_divergence_formula["-"][1]), lag_ratio=0.7)
        )
        self.add(kl_divergence_formula)

        # Put labels
        cross_entropy_label = TexText(
            R"Cross Entropy of \\ Q relative to P",
            tex_to_color_map={"Q": PINK, "P": GREEN},
            font_size=30
        ).next_to(
            kl_divergence_formula[R"\left(\sum_i p_i(-\log_2 q_i)\right)"], DOWN, buff=0.3
        )
        self.play(FadeIn(cross_entropy_label, shift=UP * 0.1))
        self.wait(1)
        entropy_label = TexText(
            R"Entropy of P",
            tex_to_color_map={"Q": PINK, "P": GREEN},
            font_size=30
        ).next_to(
            kl_divergence_formula[R"\left(\sum_i p_i(-\log_2 p_i)\right)"], DOWN, buff=0.3
        ).match_y(cross_entropy_label)
        self.play(FadeIn(entropy_label, shift=UP * 0.1))

        # Write "KL Divergence"
        kl_divergence_text = TexText(
            "Kullback-Leibler Divergence:",
            font_size=60,
            tex_to_color_map={"K": YELLOW, "L": YELLOW}
        ).shift(UP * 2)
        self.play(
            AnimationGroup(
                VGroup(kl_divergence_formula, cross_entropy_label, entropy_label).animate.shift(DOWN * 0.5),
                Write(kl_divergence_text, run_time=2), lag_ratio=0.8)
        )
        self.wait(0.5)
        kl_divergence_text_shortened = TexText("KL Divergence:").match_height(kl_divergence_text).move_to(kl_divergence_text)
        kl_divergence_text_shortened[:2].set_color(YELLOW)
        self.play(
            TransformMatchingShapes(kl_divergence_text["Kullback-Leibler"], kl_divergence_text_shortened["KL"]),
            TransformMatchingShapes(kl_divergence_text["Divergence:"], kl_divergence_text_shortened["Divergence:"]), run_time=1.3)
        self.wait(2)
