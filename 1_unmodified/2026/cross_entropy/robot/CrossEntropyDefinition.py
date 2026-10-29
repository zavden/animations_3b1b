# ==============================================================================
# Scene:      CrossEntropyDefinition
# Source:     videos/_2026/cross_entropy/robot.py (lines 3348-3704)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl CrossEntropyDefinition.py CrossEntropyDefinition -w -m --fps 15
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
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


class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, *args, **kwargs):
        super().__init__("images/arrow.svg", *args, **kwargs)
        if (direction == UP).all():
            self.rotate(PI / 2)
        elif (direction == LEFT).all():
            self.rotate(PI)
        elif (direction == DOWN).all():
            self.rotate(3 * PI / 2)
        self.direction = direction


def random_distribution(n, thresh=1 / 16):
    if n <= 0:
        return []
    if n * thresh > 1:
        raise ValueError("Threshold is too high to sum to 1")
    remaining_sum = 1 - (n * thresh)
    random_parts = np.random.dirichlet(np.ones(n), size=1).flatten()
    numbers = (random_parts * remaining_sum) + thresh
    return numbers.tolist()


class CrossEntropyDefinition(InteractiveScene):
    def construct(self):
        # Show the chart for the first distribution
        encoding = ["0", "10", "110", "111"]
        first_distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        first_distribution_chart = EntropyChart(
            first_distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]),
            probability_labels=[
                Tex(R"\frac{1}{" + ["2", "4", "8", "8"][i] + "}", font_size=65)
                for i in range(4)
            ],
            bar_labels=[
                Tex(encoding[i], font_size=57)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=12,
            height=4.5,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).scale(0.3).to_corner(UL, buff=0.7).shift(DOWN * 0.7)
        first_distribution_chart.update()
        first_distribution_chart.clear_updaters()
        first_distribution_chart.bar_labels.set_color(WHITE)
        self.play(first_distribution_chart.create(), run_time=2)
        self.wait(2)
        self.play(first_distribution_chart.animate.set_x(-FRAME_WIDTH * 0.25), run_time=2.5)
        self.wait(2)

        # Build the segments for the second chart
        second_distribution = [1 / 8, 1 / 8, 1 / 4, 1 / 2]
        second_distribution_chart = EntropyChart(
            second_distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]),
            probability_labels=[
                Tex(R"\frac{1}{" + ["8", "8", "4", "2"][i] + "}", font_size=65)
                for i in range(4)
            ],
            bar_labels=[
                Tex(encoding[i], font_size=57)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=12,
            height=4.5,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).scale(0.3).to_edge(UP, buff=1.4).set_x(FRAME_WIDTH * 0.25)
        second_distribution_chart.update()
        second_distribution_chart.clear_updaters()
        second_distribution_chart.bar_labels.set_color(WHITE)
        for segment, e_label, p_label in list(zip(
            second_distribution_chart.segments.bars,
            second_distribution_chart.event_labels,
            second_distribution_chart.probability_labels
        )):
            self.play(
                AnimationGroup(
                    GrowFromCenter(segment),
                    FadeIn(e_label),
                    FadeIn(p_label),
                    suspend_mobject_updating=True, run_time=2)
            )
            self.wait(2)
        self.wait(4)

        # The bars hop over from the old distribution to the new one
        self.play(
            AnimationGroup(*[
                TransformFromCopy(VGroup(bar1, label1), VGroup(bar2, label2), run_time=3)
                for bar1, label1, bar2, label2 in list(zip(
                    first_distribution_chart.bars,
                    first_distribution_chart.bar_labels,
                    second_distribution_chart.bars,
                    second_distribution_chart.bar_labels
                ))[::-1]
            ], lag_ratio=0.3)
        )
        self.wait(2)

        # Center everything
        self.play(
            VGroup(first_distribution_chart, second_distribution_chart).animate.scale(1.5).arrange(buff=2).shift(DOWN * 0.5), run_time=2.5)

        # Calculate the cross entropy
        weighted_sum_lines = VGroup(
            Tex(R"\frac{1}{8} \cdot 1", font_size=26).next_to(second_distribution_chart.bars[0], UP),
            Tex(R"\frac{1}{8} \cdot 2", font_size=26).next_to(second_distribution_chart.bars[1], UP),
            Tex(R"\frac{1}{4} \cdot 3", font_size=26).next_to(second_distribution_chart.bars[2], UP),
            Tex(R"\frac{1}{2} \cdot 3", font_size=26).next_to(second_distribution_chart.bars[3], UP)
        )
        for line in weighted_sum_lines:
            line[:3].set_color(GREEN)
            line[4:].set_color(PINK)

        self.play(
            AnimationGroup(
                TransformFromCopy(second_distribution_chart.probability_labels[0], weighted_sum_lines[0][:-2]),
                FadeIn(weighted_sum_lines[0][-2:], shift=UP * 0.1), run_time=1.5)
        )
        self.wait(1.5)
        self.play(
            AnimationGroup(
                TransformFromCopy(second_distribution_chart.probability_labels[1], weighted_sum_lines[1][:-2]),
                FadeIn(weighted_sum_lines[1][-2:], shift=UP * 0.1), run_time=1.5)
        )
        self.wait(2.5)
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    TransformFromCopy(label, line[:-2]),
                    FadeIn(line[-2:], shift=UP * 0.1), run_time=1.5)
                for label, line in zip(second_distribution_chart.probability_labels[2:], weighted_sum_lines[2:])
            ], lag_ratio=0.3)
        )

        self.wait(1)
        sum_result = Tex(
            R"\frac{1}{8} \cdot 1 + \frac{1}{8} \cdot 2 + \frac{1}{4} \cdot 3 + \frac{1}{2} \cdot 3 \\ = 2.625 \text{ bits}",
            font_size=32,
            tex_to_color_map={
                R"\frac{1}{8}": GREEN,
                R"\frac{1}{4}": GREEN,
                R"\frac{1}{2}": GREEN,
                " 1 ": PINK,
                " 2 ": PINK,
                " 3 ": PINK
            }
        ).next_to(second_distribution_chart, UP, buff=0.3)

        self.play(TransformMatchingShapes(weighted_sum_lines, sum_result[:-10], path_arc=PI * 0.2, run_time=1.5))
        self.wait(0.5)
        self.play(FadeIn(sum_result[R"= 2.625 \text{ bits}"]))
        self.wait(2)

        # Write "cross entropy"
        cross_entropy_text = TexText("Cross Entropy:").set_fill(color=[PINK, GREEN]).next_to(sum_result, UP)
        for i, letter in enumerate(cross_entropy_text):
            letter.set_color(interpolate_color(PINK, GREEN, i / (len(cross_entropy_text) - 1)))
        self.play(Write(cross_entropy_text, run_time=2.5))
        self.wait(0.5)
        rect1 = SurroundingRectangle(
            first_distribution_chart.probability_labels, stroke_width=2, stroke_color=PINK
        ).stretch_to_fit_width(first_distribution_chart.bars.get_width()).match_x(first_distribution_chart.bars)
        self.play(FadeIn(rect1), run_time=1.5)
        self.wait(3)
        rect2 = SurroundingRectangle(
            second_distribution_chart.probability_labels, stroke_width=2, stroke_color=GREEN
        ).stretch_to_fit_width(second_distribution_chart.bars.get_width()).match_x(second_distribution_chart.bars)
        self.play(ReplacementTransform(rect1, rect2), run_time=2.5)
        self.wait(2)
        self.play(FadeOut(rect2))
        self.wait(2)

        # Label the two charts with p and q
        p_chart = EntropyChart(
            second_distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]).scale(0.6) for i in range(4)]),
            probability_labels=VGroup(*[Tex(f"p_{i + 1}", font_size=42) for i in range(4)]),
            bar_labels=[
                Tex(encoding[i], font_size=27)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=second_distribution_chart.get_width(),
            height=3,
            include_vertical_axis=False,
            segments_height=0.5,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        p_chart.suspend_updating()
        p_chart.bar_labels.set_color(WHITE)

        q_chart = EntropyChart(
            first_distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]).scale(0.6) for i in range(4)]),
            probability_labels=VGroup(*[Tex(f"q_{i + 1}", font_size=42) for i in range(4)]),
            bar_labels=[
                Tex(encoding[i], font_size=27)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=first_distribution_chart.get_width(),
            height=3,
            include_vertical_axis=False,
            segments_height=0.5,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        q_chart.suspend_updating()
        q_chart.bar_labels.set_color(WHITE)

        p_chart.match_x(second_distribution_chart).align_to(second_distribution_chart.bars, UP)
        q_chart.match_x(first_distribution_chart).align_to(first_distribution_chart.bars, UP)
        self.play(ReplacementTransform(second_distribution_chart, p_chart, suspend_mobject_updating=True), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(first_distribution_chart, q_chart, suspend_mobject_updating=True), run_time=2)
        self.wait(3)

        # Show the encoding and the original distribution
        arrow = Arrow(q_chart.bars, p_chart.bars)
        arrow_label = TexText("encoding", font_size=27).next_to(arrow, UP, buff=0.1)
        arrow_label_2 = TexText(R"codeword length: \\ $-\log_2 q_i$", font_size=20).next_to(arrow, DOWN, buff=0.1)
        arrow_label_2["q_i"].set_color(PINK)
        q_chart.save_state()
        p_chart.save_state()
        self.play(
            VGroup(
                p_chart.segments,
                p_chart.probability_labels
            ).animate.fade(0.8),
            GrowArrow(arrow, run_time=1.4),
            Write(arrow_label, run_time=1.5)
        )
        self.wait(4)
        self.play(FadeIn(arrow_label_2))
        self.wait(4)
        self.play(
            FadeOut(VGroup(arrow, arrow_label, arrow_label_2)),
            q_chart.animate.fade(0.8),
            p_chart.animate.restore(),
            p_chart.bars.animate.fade(0.8),
            p_chart.bar_labels.animate.fade(0.8)
        )
        self.wait(1)
        self.play(q_chart.animate.restore(), p_chart.animate.restore(), run_time=2)
        general_equation = TexText(
            R"Avg. bits per instruction: \\[0.1in] $\displaystyle\sum_i p_i (-\log_2 q_i)$",
            font_size=40,
            tex_to_color_map={
                "p_i": GREEN,
                "q_i": PINK
            }
        ).next_to(second_distribution_chart, UP, buff=0.3)
        self.play(FadeOut(VGroup(cross_entropy_text, sum_result)), FadeIn(general_equation), run_time=1.5)
        self.wait(2)

        # Replace "Avg. bits per instruction" with "Cross Entropy(Q, P)"
        cross_entropy_text = TexText(
            "``Cross Entropy of Q relative to P''",
            tex_to_color_map={"Q": PINK, "P": GREEN}
        ).match_height(
            general_equation["Avg. bits per instruction:"]
        ).move_to(
            general_equation["Avg. bits per instruction:"]
        )
        self.play(FadeOut(general_equation["Avg. bits per instruction:"]), FadeIn(cross_entropy_text))
        self.wait(3)

        # Show special notation
        full_sum = general_equation[len("Avg.bitsperinstruction:"):]
        self.play(
            FadeOut(VGroup(q_chart, p_chart), run_time=1.6, shift=DOWN * 2),
            VGroup(cross_entropy_text, full_sum).animate(run_time=2).set_y(0).to_edge(LEFT, buff=2)
        )
        notations = BulletedList(
            R"$H(P, Q)$",
            R"$H(P \parallel Q)$",
            R"$H_Q(P)$",
            R"$\mathbb{E}_P[-\log Q]$",
            R"$\langle -\log Q \rangle_P$",
            tex_to_color_map={"Q": PINK, "P": GREEN}
        ).to_edge(RIGHT, buff=2)
        brace = Brace(notations, LEFT)
        self.play(
            GrowFromEdge(brace, RIGHT),
            AnimationGroup(*[FadeIn(line, shift=DOWN * 0.3) for line in notations], lag_ratio=0.2), run_time=3)
        self.wait(2)

        # Focus on the full sum
        self.play(
            FadeOut(VGroup(brace, notations), shift=RIGHT * 3),
            VGroup(cross_entropy_text, full_sum).animate.scale(1.2).center(), run_time=2)
        self.wait(2)

        # Show where the spacing of the bars and the heights of the bars come from
        self.play(VGroup(cross_entropy_text, full_sum).animate.to_edge(UP, buff=0.7))
        np.random.seed(0)
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
            height=3.5,
            include_vertical_axis=False,
            segments_height=0.2,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            stroke_width=1
        )
        p_cross_entropy_chart = EntropyChart(
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
            height=3.5,
            include_vertical_axis=False,
            segments_height=0.2,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            stroke_width=1
        )
        q_entropy_chart.generate_target()
        VGroup(q_entropy_chart.target, p_cross_entropy_chart).arrange(buff=1.5).to_edge(DOWN, buff=1)
        q_entropy_chart.to_edge(DOWN, buff=1)
        self.play(q_entropy_chart.create())
        self.wait(1.5)
        self.play(MoveToTarget(q_entropy_chart), run_time=1.5)

        self.play(
            AnimationGroup(*[
                TransformFromCopy(bar1, bar2, run_time=3)
                for bar1, bar2 in list(zip(
                    q_entropy_chart.bars,
                    p_cross_entropy_chart.bars,
                ))[::-1]
            ], lag_ratio=0.3),
            AnimationGroup(*[
                FadeIn(VGroup(segment, prob))
                for segment, prob in list(zip(
                    p_cross_entropy_chart.segments.bars,
                    p_cross_entropy_chart.probability_labels
                ))[::-1]
            ]), run_time=4)
        self.add(p_cross_entropy_chart)

        # Change the distribution P to be more similar to Q
        Almost_Q = [0.34, 0.16, 0.03, 0.22, 0.25]
        self.play(p_cross_entropy_chart.set_distribution(Almost_Q), run_time=2)
        self.wait(2)

        # Show more inefficient distributions
        self.play(p_cross_entropy_chart.set_distribution(random_distribution(5)), run_time=2)
        self.wait(1)
        self.play(p_cross_entropy_chart.set_distribution(P), run_time=2)
        for _ in range(3):
            self.play(p_cross_entropy_chart.set_distribution(random_distribution(5)), run_time=2)


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
