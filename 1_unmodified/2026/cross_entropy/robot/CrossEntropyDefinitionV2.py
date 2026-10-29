# ==============================================================================
# Scene:      CrossEntropyDefinitionV2
# Source:     videos/_2026/cross_entropy/robot.py (lines 3985-5711)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl CrossEntropyDefinitionV2.py CrossEntropyDefinitionV2 -w -m --fps 15
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *
import random


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


class CrossEntropyDefinitionV2(InteractiveScene):
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
            VGroup(first_distribution_chart, second_distribution_chart).animate.scale(1.3).arrange(buff=2).shift(DOWN * 0.5), run_time=2.5)

        # Calculate the cross entropy
        weighted_sum_lines = VGroup(
            Tex(R"\frac{1}{8} \cdot 1", font_size=23).next_to(second_distribution_chart.bars[0], UP),
            Tex(R"\frac{1}{8} \cdot 2", font_size=23).next_to(second_distribution_chart.bars[1], UP),
            Tex(R"\frac{1}{4} \cdot 3", font_size=23).next_to(second_distribution_chart.bars[2], UP),
            Tex(R"\frac{1}{2} \cdot 3", font_size=23).next_to(second_distribution_chart.bars[3], UP)
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
            height=2.3,
            include_vertical_axis=False,
            segments_height=0.4,
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
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=False,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        q_chart.suspend_updating()
        q_chart.bar_labels.set_color(WHITE)

        p_chart.match_x(second_distribution_chart).align_to(second_distribution_chart.bars, UP)
        q_chart.match_x(first_distribution_chart).align_to(first_distribution_chart.bars, UP)
        self.play(
            FadeOut(VGroup(cross_entropy_text, sum_result)),
            ReplacementTransform(second_distribution_chart, p_chart, suspend_mobject_updating=True), run_time=2)
        self.wait(2)
        self.play(ReplacementTransform(first_distribution_chart, q_chart, suspend_mobject_updating=True), run_time=2)
        self.wait(3)

        # Generalize the charts
        p_chart_general = EntropyChart(
            second_distribution,
            event_labels=VGroup(*[
                Tex(
                    (("s_" + str(i + 1)) if i < len(second_distribution) - 2 else R"\ldots" if i == len(second_distribution) - 2 else "s_n"),
                    font_size=35
                ).set_color(BLACK)
                for i in range(len(second_distribution))
            ]),
            probability_labels=VGroup(*[
                Tex(
                    (("p_" + str(i + 1)) if i < len(second_distribution) - 2 else R"\ldots" if i == len(second_distribution) - 2 else "p_n"),
                    font_size=42
                )
                for i in range(len(second_distribution))
            ]),
            bar_labels=VMobject(),
            bar_heights=[1, 2, 3, 3],
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        p_chart_general.suspend_updating()

        q_chart_general = EntropyChart(
            first_distribution,
            event_labels=VGroup(*[
                Tex(
                    (("s_" + str(i + 1)) if i < len(first_distribution) - 2 else R"\ldots" if i == len(first_distribution) - 2 else "s_n"),
                    font_size=35
                ).set_color(BLACK)
                for i in range(len(first_distribution))
            ]),
            probability_labels=VGroup(*[
                Tex(
                    (("q_" + str(i + 1)) if i < len(first_distribution) - 2 else R"\ldots" if i == len(first_distribution) - 2 else "q_n"),
                    font_size=42
                )
                for i in range(len(first_distribution))
            ]),
            bar_labels=VMobject(),
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        )
        q_chart_general.suspend_updating()

        p_chart_general.shift(p_chart.bars.get_center() - p_chart_general.bars.get_center())
        q_chart_general.shift(q_chart.bars.get_center() - q_chart_general.bars.get_center())
        self.play(
            ReplacementTransform(
                VGroup(q_chart.bars, q_chart.segments, q_chart.probability_labels),
                VGroup(q_chart_general.bars, q_chart_general.segments, q_chart_general.probability_labels), suspend_mobject_updating=True),
            ReplacementTransform(
                VGroup(p_chart.bars, p_chart.segments, p_chart.probability_labels),
                VGroup(p_chart_general.bars, p_chart_general.segments, p_chart_general.probability_labels), suspend_mobject_updating=True),
            FadeOut(VGroup(q_chart.bar_labels, p_chart.bar_labels)), run_time=2)
        self.wait(2)

        self.remove(q_chart, p_chart)
        self.add(q_chart_general, p_chart_general)
        VGroup(
            q_chart_general.vertical_axis,
            q_chart_general.vertical_axis_label,
            q_chart_general.reference_lines,
            p_chart_general.vertical_axis,
            p_chart_general.vertical_axis_label,
            p_chart_general.reference_lines
        ).set_opacity(0)

        # Show different possibilities for what the symbols could mean
        alternate_symbols_q_1 = VGroup(*[
            InstructionArrow([UP, DOWN, LEFT, RIGHT][i]).scale(0.08)
            for i in range(4)
        ])
        alternate_symbols_p_1 = alternate_symbols_q_1.copy()
        for i, (q_symb, p_symb) in enumerate(zip(alternate_symbols_q_1, alternate_symbols_p_1)):
            q_symb.move_to(q_chart_general.event_labels[i])
            p_symb.move_to(p_chart_general.event_labels[i])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(q_chart_general.event_labels, alternate_symbols_q_1)
            ], lag_ratio=0.2),
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(p_chart_general.event_labels, alternate_symbols_p_1)
            ], lag_ratio=0.2)
        )
        self.wait(0.8)

        alternate_symbols_q_2 = VGroup(*[
            TexText(["a", "b", "c", "d"][i], font_size=35).set_color(BLACK)
            for i in range(4)
        ])
        alternate_symbols_p_2 = alternate_symbols_q_2.copy()
        for i, (q_symb, p_symb) in enumerate(zip(alternate_symbols_q_2, alternate_symbols_p_2)):
            q_symb.next_to(q_chart_general.probability_labels[0], UP, buff=0.345).match_x(q_chart_general.probability_labels[i])
            p_symb.next_to(p_chart_general.probability_labels[0], UP, buff=0.345).match_x(p_chart_general.probability_labels[i])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(alternate_symbols_q_1, alternate_symbols_q_2)
            ], lag_ratio=0.2),
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(alternate_symbols_p_1, alternate_symbols_p_2)
            ], lag_ratio=0.2)
        )
        self.wait(0.8)

        alternate_symbols_q_3 = VGroup(*[
            Tex(["e", R"\wedge", R"\pi", "i"][i], font_size=40 if i != 1 else 20).set_color(BLACK)
            for i in range(4)
        ])
        alternate_symbols_p_3 = alternate_symbols_q_3.copy()
        for i, (q_symb, p_symb) in enumerate(zip(alternate_symbols_q_3, alternate_symbols_p_3)):
            q_symb.next_to(q_chart_general.probability_labels[0], UP, buff=0.33 if i != 1 else 0.455).match_x(q_chart_general.probability_labels[i])
            p_symb.next_to(p_chart_general.probability_labels[0], UP, buff=0.33 if i != 1 else 0.455).match_x(p_chart_general.probability_labels[i])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(alternate_symbols_q_2, alternate_symbols_q_3)
            ], lag_ratio=0.2),
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(label),
                    FadeIn(alternate_label)
                )
                for label, alternate_label in zip(alternate_symbols_p_2, alternate_symbols_p_3)
            ], lag_ratio=0.2)
        )
        self.wait(0.8)

        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(alternate_label),
                    FadeIn(label)
                )
                for alternate_label, label in zip(alternate_symbols_q_3, q_chart_general.event_labels)
            ], lag_ratio=0.2),
            AnimationGroup(*[
                AnimationGroup(
                    FadeOut(alternate_label),
                    FadeIn(label)
                )
                for alternate_label, label in zip(alternate_symbols_p_3, p_chart_general.event_labels)
            ], lag_ratio=0.2)
        )
        self.wait(0.8)

        # Show bar heights for q chart
        q_chart = q_chart_general
        p_chart = p_chart_general
        self.play(FancyCircumscribe(VGroup(q_chart.bars, q_chart.probability_labels)))

        p_chart.save_state()
        self.play(
            self.camera.frame.animate.match_x(VGroup(q_chart, p_chart)).shift(UP * 0.7),
            AnimationGroup(
                p_chart.animate.fade(0.9),
                AnimationGroup(
                    Write(q_chart.vertical_axis_label.set_opacity(1), run_time=2),
                    ShowCreation(q_chart.vertical_axis.set_opacity(1)),
                    AnimationGroup(*[
                        ShowCreation(line.set_opacity(1))
                        for line in q_chart.reference_lines
                    ], lag_ratio=0.1)
                ), lag_ratio=0.3), run_time=2)
        self.wait(2)
        Group(*self.mobjects).shift(-self.camera.frame.get_center())
        self.camera.frame.center()

        # Show the avg. bits per instruction for Q
        q_bits_per_instruction = TexText(
            R"Avg. bits per instruction: \\[0.1in] $\displaystyle\sum_i q_i (-\log_2 q_i)$",
            font_size=35,
            tex_to_color_map={
                "q_i": PINK
            }
        ).next_to(q_chart.bars, UP, buff=1)
        self.play(Write(q_bits_per_instruction), run_time=3)
        self.wait(1.5)

        q_bits_per_instruction.save_state()
        q_chart.save_state()
        for i in range(4):
            anims = [
                AnimationGroup(
                    VGroup(
                        q_chart.segments.bars[i + 1:],
                        q_chart.event_labels[i + 1:],
                        q_chart.probability_labels[i + 1:],
                        q_chart.segments.bars[:i],
                        q_chart.event_labels[:i],
                        q_chart.probability_labels[:i]
                    ).animate.set_opacity(0.2),
                    VGroup(
                        q_chart.segments.bars[i],
                        q_chart.event_labels[i],
                        q_chart.probability_labels[i]
                    ).animate.set_opacity(1),
                )
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        q_bits_per_instruction.animate.fade(0.8),
                        q_bits_per_instruction["q_i"][0].animate.set_opacity(1),
                        q_chart.bars.animate.fade(0.8)
                    )
                )
            self.play(AnimationGroup(*anims))

        for i in range(4):
            anims = [
                AnimationGroup(
                    VGroup(
                        q_chart.bars[i + 1:],
                        q_chart.bars[:i],
                        q_chart.bar_labels[:i],
                    ).animate.set_opacity(0.2),
                    q_chart.bars[i].animate.set_opacity(1),
                )
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        q_bits_per_instruction[-8:-1].animate.set_opacity(1),
                        q_bits_per_instruction["q_i"][0].animate.fade(0.8),
                        VGroup(
                            q_chart.segments.bars[3],
                            q_chart.event_labels[3],
                            q_chart.probability_labels[3]
                        ).animate.fade(0.8)
                    )
                )
            self.play(AnimationGroup(*anims))
        self.play(q_chart.animate.restore(), q_bits_per_instruction.animate.restore(), run_time=2)
        self.wait(2)

        # Label the equation with "entropy"
        entropy_text = TexText(
            "Entropy of Q",
            tex_to_color_map={"Q": PINK}
        ).match_height(
            q_bits_per_instruction["Avg. bits per instruction:"]
        ).move_to(
            q_bits_per_instruction["Avg. bits per instruction:"]
        )
        self.play(FadeOut(q_bits_per_instruction["Avg. bits per instruction:"]), FadeIn(entropy_text))
        self.wait(2)

        # Highlight the area of the diagram
        q_entropy_formula = q_bits_per_instruction[len("Avg.bitsperinstruction:"):]

        self.play(AnimationGroup(*[Indicate(bar, scale_factor=1.1) for bar in q_chart.bars], lag_ratio=0.1, run_time=2.5))

        # Show why the area represents the expression
        entropy_text.save_state()
        q_entropy_formula.save_state()
        q_chart.save_state()
        for i in range(4):
            anims = [
                AnimationGroup(
                    VGroup(
                        q_chart.segments.bars[i + 1:],
                        q_chart.event_labels[i + 1:],
                        q_chart.probability_labels[i + 1:],
                        q_chart.segments.bars[:i],
                        q_chart.event_labels[:i],
                        q_chart.probability_labels[:i]
                    ).animate.set_opacity(0.2),
                    VGroup(
                        q_chart.segments.bars[i],
                        q_chart.event_labels[i],
                        q_chart.probability_labels[i]
                    ).animate.set_opacity(1),
                )
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        entropy_text.animate.fade(0.8),
                        q_entropy_formula.animate.fade(0.8),
                        q_bits_per_instruction["q_i"][0].animate.set_opacity(1),
                        q_chart.bars.animate.fade(0.8)
                    )
                )
            self.play(AnimationGroup(*anims), run_time=0.62)

        for i in range(4):
            anims = [
                AnimationGroup(
                    VGroup(
                        q_chart.bars[i + 1:],
                        q_chart.bars[:i],
                        q_chart.bar_labels[:i],
                    ).animate.set_opacity(0.2),
                    q_chart.bars[i].animate.set_opacity(1),
                )
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        q_bits_per_instruction[-8:-1].animate.set_opacity(1),
                        q_bits_per_instruction["q_i"][0].animate.fade(0.8),
                        VGroup(
                            q_chart.segments.bars[3],
                            q_chart.event_labels[3],
                            q_chart.probability_labels[3]
                        ).animate.fade(0.8)
                    )
                )
            self.play(AnimationGroup(*anims), run_time=0.62)
        self.play(q_chart.animate.restore(), q_entropy_formula.animate.restore(), entropy_text.animate.restore(), run_time=1.2)
        self.bring_to_back(q_chart.reference_lines, p_chart.reference_lines)

        # Switch focus to the p chart
        self.play(VGroup(p_chart.segments, p_chart.probability_labels).animate.set_opacity(1))

        # Show the encoding and the original distribution
        self.play(
            AnimationGroup(
                AnimationGroup(
                    Write(p_chart.vertical_axis_label.set_opacity(1), run_time=2),
                    ShowCreation(p_chart.vertical_axis.set_opacity(1)),
                    AnimationGroup(*[
                        ShowCreation(line.set_opacity(1))
                        for line in p_chart.reference_lines
                    ], lag_ratio=0.1)
                ),
                AnimationGroup(*[
                    TransformFromCopy(bar1, bar2, run_time=3)
                    for bar1, bar2 in list(zip(
                        q_chart.bars.copy().set_opacity(0.8),
                        p_chart.bars.copy().set_opacity(0.8),
                    ))[::-1]
                ], lag_ratio=0.3), lag_ratio=0.7)
        )
        self.clear()
        p_chart.bars.set_opacity(0.8)
        self.add(q_chart, p_chart, entropy_text, q_entropy_formula)
        self.bring_to_back(q_chart.reference_lines, p_chart.reference_lines)

        # Write cross entropy equation
        general_equation = TexText(
            R"Avg. bits per instruction: \\[0.1in] $\displaystyle\sum_i p_i (-\log_2 q_i)$",
            font_size=35,
            tex_to_color_map={
                "p_i": GREEN,
                "q_i": PINK
            }
        ).next_to(p_chart.bars, UP, buff=1)
        self.play(Write(general_equation), run_time=3)
        self.wait(2)
        self.play(Flash(general_equation["p_i"], flash_radius=0.5))

        # Replace "Avg. bits per instruction" with "Cross Entropy(Q, P)"
        self.play(FancyCircumscribe(general_equation))
        cross_entropy_text = TexText(
            "Cross Entropy of Q relative to P",
            tex_to_color_map={"Q": PINK, "P": GREEN}
        ).match_height(
            general_equation["Avg. bits per instruction:"]
        ).move_to(
            general_equation["Avg. bits per instruction:"]
        )
        self.play(FadeOut(general_equation["Avg. bits per instruction:"]), FadeIn(cross_entropy_text), run_time=2)
        self.wait(3)

        # Show special notation
        full_sum = general_equation[len("Avg.bitsperinstruction:"):]
        cross_entropy_group = VGroup(cross_entropy_text, full_sum)
        cross_entropy_group.save_state()
        self.play(
            FadeOut(
                VGroup(
                    q_chart,
                    p_chart,
                    entropy_text,
                    q_bits_per_instruction[len("Avg.bitsperinstruction:"):]
                ), run_time=1.6, shift=DOWN * 3),
            cross_entropy_group.animate(run_time=2, path_arc=PI * 0.2).set_y(0).to_edge(LEFT, buff=2)
        )
        notations = BulletedList(
            R"$H(P, Q)$",
            R"$H(P \parallel Q)$",
            R"$H_Q(P)$",
            R"$\mathbb{E}_P[-\log Q]$",
            R"$\langle -\log Q \rangle_P$",
            tex_to_color_map={"Q": PINK, "P": GREEN}
        ).to_edge(RIGHT, buff=2.2)
        brace = Brace(notations, LEFT)
        self.play(
            GrowFromEdge(brace, RIGHT),
            AnimationGroup(*[FadeIn(line, shift=DOWN * 0.3) for line in notations], lag_ratio=0.2), run_time=3)
        self.wait(1)

        # Put everything back
        self.play(
            FadeOut(VGroup(brace, notations), shift=RIGHT * 5, run_time=1.5),
            FadeIn(
                VGroup(
                    q_chart,
                    p_chart,
                    entropy_text,
                    q_bits_per_instruction[len("Avg.bitsperinstruction:"):]
                ), run_time=2, shift=UP * 3),
            cross_entropy_group.animate(run_time=2, path_arc=-PI * 0.2).restore()
        )
        self.bring_to_back(q_chart.reference_lines, p_chart.reference_lines)
        self.wait(1)

        # Highlight the diagram
        self.play(FancyCircumscribe(p_chart, run_time=5))

        # Show the widths and heights of each bar in the cross entropy diagram
        self.play(FancyCircumscribe(p_chart.probability_labels), FancyCircumscribe(general_equation["p_i"]))
        self.play(FancyCircumscribe(p_chart.vertical_axis_label, run_time=5), FancyCircumscribe(general_equation[-8:-1], run_time=5))
        self.wait(3)

        # Create all four charts
        q_entropy_chart = q_chart
        qp_cross_entropy_chart = p_chart
        p_entropy_chart = EntropyChart(
            second_distribution,
            event_labels=VGroup(*[
                Tex(
                    (("s_" + str(i + 1)) if i < len(second_distribution) - 2 else R"\ldots" if i == len(second_distribution) - 2 else "s_n"),
                    font_size=35
                ).set_color(BLACK)
                for i in range(len(second_distribution))
            ]),
            probability_labels=VGroup(*[
                Tex(
                    (("p_" + str(i + 1)) if i < len(second_distribution) - 2 else R"\ldots" if i == len(second_distribution) - 2 else "p_n"),
                    font_size=42
                )
                for i in range(len(second_distribution))
            ]),
            bar_labels=None,
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(qp_cross_entropy_chart)

        pq_cross_entropy_chart = EntropyChart(
            first_distribution,
            event_labels=VGroup(*[
                Tex(
                    (("s_" + str(i + 1)) if i < len(first_distribution) - 2 else R"\ldots" if i == len(first_distribution) - 2 else "s_n"),
                    font_size=35
                ).set_color(BLACK)
                for i in range(len(first_distribution))
            ]),
            probability_labels=VGroup(*[
                Tex(
                    (("q_" + str(i + 1)) if i < len(first_distribution) - 2 else R"\ldots" if i == len(first_distribution) - 2 else "q_n"),
                    font_size=42
                )
                for i in range(len(first_distribution))
            ]),
            bar_labels=None,
            bar_heights=[1, 2, 3, 3],
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(q_entropy_chart)
        q_entropy_text = entropy_text
        q_entropy_formula = q_entropy_formula
        q_entropy_group = VGroup(q_entropy_text, q_entropy_formula, q_entropy_chart)
        qp_cross_entropy_text = cross_entropy_text
        qp_cross_entropy_formula = full_sum
        qp_cross_entropy_group = VGroup(qp_cross_entropy_text, qp_cross_entropy_formula, qp_cross_entropy_chart)
        p_entropy_text = TexText(
            "Entropy of P",
            tex_to_color_map={"P": GREEN}
        ).match_height(
            q_entropy_text
        ).move_to(
            qp_cross_entropy_text
        )
        p_entropy_formula = Tex(
            R"\displaystyle\sum_i p_i (-\log_2 p_i)",
            tex_to_color_map={
                "p_i": GREEN
            }
        ).match_height(q_entropy_formula).move_to(qp_cross_entropy_formula)
        p_entropy_group = VGroup(p_entropy_text, p_entropy_formula, p_entropy_chart)
        pq_cross_entropy_text = TexText(
            "Cross Entropy of P relative to Q",
            tex_to_color_map={"P": GREEN, "Q": PINK}
        ).match_height(
            q_entropy_text
        ).move_to(
            q_entropy_text
        )
        pq_cross_entropy_formula = Tex(
            R"\displaystyle\sum_i q_i (-\log_2 p_i)",
            tex_to_color_map={
                "p_i": GREEN,
                "q_i": PINK
            }
        ).match_height(q_entropy_formula).move_to(q_entropy_formula)
        pq_cross_entropy_group = VGroup(pq_cross_entropy_text, pq_cross_entropy_formula, pq_cross_entropy_chart)

        # Show the 2x2 grid of charts
        q_entropy_group.generate_target()
        qp_cross_entropy_group.generate_target()
        VGroup(q_entropy_group.target, qp_cross_entropy_group.target).arrange(buff=3)
        pq_cross_entropy_group.match_x(q_entropy_group.target)
        p_entropy_group.match_x(qp_cross_entropy_group.target)
        VGroup(
            VGroup(q_entropy_group.target, qp_cross_entropy_group.target),
            VGroup(pq_cross_entropy_group, p_entropy_group)
        ).arrange(DOWN, buff=1.6)
        VGroup(p_entropy_chart.segments, p_entropy_chart.probability_labels).set_opacity(0)
        self.play(
            self.camera.frame.animate(run_time=2).scale(1.5),
            AnimationGroup(
                MoveToTarget(q_entropy_group, run_time=2),
                MoveToTarget(qp_cross_entropy_group, run_time=2)
            ),
            AnimationGroup(
                TransformFromCopy(
                    VGroup(qp_cross_entropy_chart.segments, qp_cross_entropy_chart.probability_labels),
                    VGroup(p_entropy_chart.segments.copy(), p_entropy_chart.probability_labels.copy()).set_opacity(1), run_time=2),
                p_entropy_chart.create(),
                Write(VGroup(p_entropy_text, p_entropy_formula)), lag_ratio=0.7)
        )
        self.clear()
        VGroup(p_entropy_chart.segments, p_entropy_chart.probability_labels).set_opacity(1)
        self.add(q_entropy_group, qp_cross_entropy_group, p_entropy_group)
        self.bring_to_back(q_entropy_chart.reference_lines, qp_cross_entropy_chart.reference_lines)
        # q_entropy_chart.add_updater(lambda m: m.set_stroke(width = 1))
        # qp_cross_entropy_chart.add_updater(lambda m: m.set_stroke(width = 1))
        # pq_cross_entropy_chart.add_updater(lambda m: m.set_stroke(width = 1))
        # p_entropy_chart.add_updater(lambda m: m.set_stroke(width = 1))

        # q_entropy_chart.resume_updating()
        # qp_cross_entropy_chart.resume_updating()
        # q_entropy_chart.update()
        # qp_cross_entropy_chart.update()

        # pq_cross_entropy_chart.update()
        # p_entropy_chart.update()
        self.wait(2)

        # Change the distribution p
        n = len(qp_cross_entropy_chart.distribution_trackers)
        dashed_lines_1 = VGroup(*[
            DashedLine(stroke_width=2)
            for _ in range(n + 1)
        ])
        line_opacity_tracker_1 = ValueTracker(0)

        def update_dashed_lines(m):
            for i, line in enumerate(m):
                line.put_start_and_end_on(
                    p_entropy_chart.segments.bars[i].get_corner(DL) if i < n else p_entropy_chart.segments.bars[-1].get_corner(DR),
                    qp_cross_entropy_chart.segments.bars[i].get_corner(DL) if i < n else qp_cross_entropy_chart.segments.bars[-1].get_corner(DR)
                ).set_opacity(line_opacity_tracker_1.get_value())
        self.add(dashed_lines_1)
        self.bring_to_back(dashed_lines_1)
        dashed_lines_1.add_updater(update_dashed_lines)
        qp_cross_entropy_chart.resume_updating()
        for i in range(4):
            new_distribution = random_distribution(4, thresh=1 / 8)
            anims = [
                AnimationGroup(
                    p_entropy_chart.set_distribution(new_distribution),
                    qp_cross_entropy_chart.set_distribution(new_distribution), run_time=2)
            ]
            if i == 0:
                anims.append(line_opacity_tracker_1.animate(run_time=1.2).set_value(0.4))
            self.play(*anims)
        self.wait(2)

        # Change the distribution q
        dashed_lines_2 = VGroup(*[
            DashedLine(stroke_width=2)
            for _ in range(n + 1)
        ])
        line_opacity_tracker_2 = ValueTracker(0)

        def update_dashed_lines(m):
            for i, line in enumerate(m):
                line.put_start_and_end_on(
                    q_entropy_chart.bars[i - 1].get_corner(UL) if i > 0 else q_entropy_chart.bars[0].get_corner(DL),
                    qp_cross_entropy_chart.bars[i - 1].get_corner(UL) if i > 0 else qp_cross_entropy_chart.bars[0].get_corner(DL)
                ).set_opacity(line_opacity_tracker_2.get_value())
        self.add(dashed_lines_2)
        self.bring_to_back(dashed_lines_2)
        dashed_lines_2.add_updater(update_dashed_lines)
        q_entropy_chart.resume_updating()
        for i in range(5):
            new_distribution = random_distribution(4, thresh=1 / 8)
            anims = [
                AnimationGroup(
                    q_entropy_chart.set_distribution(new_distribution),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(q))
                        for h, q in zip(qp_cross_entropy_chart.bar_heights, new_distribution)
                    ]), run_time=2)
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        line_opacity_tracker_1.animate(run_time=1).set_value(0),
                        line_opacity_tracker_2.animate(run_time=1.2).set_value(0.4)
                    )
                )
            self.play(*anims)
        self.wait(2)

        # Add the pq cross entropy diagram
        q_entropy_chart.suspend_updating()
        for t1, t2 in zip(pq_cross_entropy_chart.distribution_trackers, q_entropy_chart.distribution_trackers):
            t1.set_value(t2.get_value())
        for h, t in zip(pq_cross_entropy_chart.bar_heights, p_entropy_chart.distribution_trackers):
            h.set_value(-math.log2(t.get_value()))
        pq_cross_entropy_chart.update()

        VGroup(pq_cross_entropy_chart.segments, pq_cross_entropy_chart.probability_labels, pq_cross_entropy_chart.bars).set_opacity(0)
        self.play(
            AnimationGroup(
                TransformFromCopy(
                    VGroup(q_entropy_chart.segments, q_entropy_chart.probability_labels),
                    VGroup(pq_cross_entropy_chart.segments.copy(), pq_cross_entropy_chart.probability_labels.copy()).set_opacity(1), run_time=2),
                AnimationGroup(*[
                    TransformFromCopy(bar1, bar2.copy().set_opacity(1))
                    for bar1, bar2 in zip(p_entropy_chart.bars, pq_cross_entropy_chart.bars)
                ], lag_ratio=0.1, run_time=2),
                pq_cross_entropy_chart.create(),
                Write(VGroup(pq_cross_entropy_text, pq_cross_entropy_formula)), lag_ratio=0.7)
        )
        self.wait(2)
        self.clear()
        q_entropy_chart.resume_updating()
        VGroup(pq_cross_entropy_chart.segments, pq_cross_entropy_chart.probability_labels).set_opacity(1)
        pq_cross_entropy_chart.bars.set_opacity(0.8)
        self.add(q_entropy_group, qp_cross_entropy_group, p_entropy_group, pq_cross_entropy_group, dashed_lines_1, dashed_lines_2)
        self.bring_to_back(q_entropy_chart.reference_lines, qp_cross_entropy_chart.reference_lines)

        # Add the last two sets of dashed lines
        dashed_lines_3 = VGroup(*[
            DashedLine(stroke_width=2)
            for _ in range(n + 1)
        ])
        line_opacity_tracker_3 = ValueTracker(0)

        def update_dashed_lines(m):
            for i, line in enumerate(m):
                line.put_start_and_end_on(
                    pq_cross_entropy_chart.segments.bars[i].get_corner(DL) if i < n else pq_cross_entropy_chart.segments.bars[-1].get_corner(DR),
                    q_entropy_chart.segments.bars[i].get_corner(DL) if i < n else q_entropy_chart.segments.bars[-1].get_corner(DR)
                ).set_opacity(line_opacity_tracker_3.get_value())
        self.add(dashed_lines_3)
        self.bring_to_back(dashed_lines_3)
        dashed_lines_3.add_updater(update_dashed_lines)

        dashed_lines_4 = VGroup(*[
            DashedLine(stroke_width=2)
            for _ in range(n + 1)
        ])
        line_opacity_tracker_4 = ValueTracker(0)

        def update_dashed_lines(m):
            for i, line in enumerate(m):
                line.put_start_and_end_on(
                    pq_cross_entropy_chart.bars[i - 1].get_corner(UL) if i > 0 else pq_cross_entropy_chart.bars[0].get_corner(DL),
                    p_entropy_chart.bars[i - 1].get_corner(UL) if i > 0 else p_entropy_chart.bars[0].get_corner(DL)
                ).set_opacity(line_opacity_tracker_4.get_value())
        self.add(dashed_lines_4)
        self.bring_to_back(dashed_lines_4)
        dashed_lines_4.add_updater(update_dashed_lines)

        # Change both distributions
        for i in range(5):
            new_distribution_1 = random_distribution(4, thresh=1 / 8) if i % 2 == 1 else [t.get_value() for t in q_entropy_chart.distribution_trackers]
            new_distribution_2 = random_distribution(4, thresh=1 / 8) if i % 2 == 0 else [t.get_value() for t in p_entropy_chart.distribution_trackers]
            anims = [
                AnimationGroup(
                    q_entropy_chart.set_distribution(new_distribution_1),
                    qp_cross_entropy_chart.set_distribution(new_distribution_2),
                    p_entropy_chart.set_distribution(new_distribution_2),
                    pq_cross_entropy_chart.set_distribution(new_distribution_1),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(q))
                        for h, q in zip(qp_cross_entropy_chart.bar_heights, new_distribution_1)
                    ]),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(p))
                        for h, p in zip(pq_cross_entropy_chart.bar_heights, new_distribution_2)
                    ]), run_time=2)
            ]
            if i == 0:
                anims.append(
                    AnimationGroup(
                        line_opacity_tracker_1.animate(run_time=1.2).set_value(0.4),
                        line_opacity_tracker_3.animate(run_time=1.2).set_value(0.4),
                        line_opacity_tracker_4.animate(run_time=1.2).set_value(0.4)
                    )
                )
            if i == 2:
                anims.append(
                    AnimationGroup(*[
                        t.animate.set_value(0)
                        for t in [line_opacity_tracker_1, line_opacity_tracker_2, line_opacity_tracker_3, line_opacity_tracker_4]
                    ])
                )
            # if i == 3:
            #     rect1 = SurroundingRectangle(qp_cross_entropy_formula, stroke_width = 2)
            #     rect2 = SurroundingRectangle(pq_cross_entropy_formula, stroke_width = 2)
            #     anims.append(FadeIn(VGroup(rect1, rect2), run_time = 1.5))
            self.play(*anims)
            if i == 2:
                self.remove(dashed_lines_1, dashed_lines_2, dashed_lines_3, dashed_lines_4)

        # Simplify to distributions over two events
        distribution_1 = [0.5, 0.5]
        distribution_2 = [0.9, 0.1]
        q_entropy_chart_two_events = EntropyChart(
            distribution_1,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(str(distribution_1[i]), font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).move_to(q_entropy_chart)
        q_entropy_chart_two_events.suspend_updating()

        qp_cross_entropy_chart_two_events = EntropyChart(
            distribution_2,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(str(distribution_2[i]), font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            bar_heights=[-math.log2(q) for q in distribution_1],
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).move_to(qp_cross_entropy_chart)
        qp_cross_entropy_chart_two_events.suspend_updating()

        p_entropy_chart_two_events = EntropyChart(
            distribution_2,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(str(distribution_2[i]), font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(p_entropy_chart)
        p_entropy_chart_two_events.suspend_updating()

        pq_cross_entropy_chart_two_events = EntropyChart(
            distribution_1,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(str(distribution_1[i]), font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            bar_heights=[-math.log2(p) for p in distribution_2],
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(pq_cross_entropy_chart)
        pq_cross_entropy_chart_two_events.suspend_updating()
        VGroup(
            q_entropy_chart_two_events,
            qp_cross_entropy_chart_two_events,
            p_entropy_chart_two_events,
            pq_cross_entropy_chart_two_events
        ).set_stroke(width=0.5)

        # Replace the charts
        self.play(
            FadeOut(VGroup(q_entropy_chart, qp_cross_entropy_chart, p_entropy_chart, pq_cross_entropy_chart), suspend_mobject_updating=True),
            FadeIn(VGroup(q_entropy_chart_two_events, qp_cross_entropy_chart_two_events, p_entropy_chart_two_events, pq_cross_entropy_chart_two_events))
        )
        self.wait(2)
        self.play(
            FancyCircumscribe(q_entropy_chart_two_events.probability_labels, run_time=5),
            FancyCircumscribe(pq_cross_entropy_chart_two_events.probability_labels, run_time=5)
        )
        self.wait(1)
        self.play(
            FancyCircumscribe(qp_cross_entropy_chart_two_events.probability_labels, run_time=5),
            FancyCircumscribe(p_entropy_chart_two_events.probability_labels, run_time=5)
        )
        self.wait(2)

        # Explain the entropy of Q
        self.camera.frame.save_state()
        group1 = VGroup(q_entropy_text, q_entropy_formula, q_entropy_chart_two_events)
        group2 = VGroup(qp_cross_entropy_text, qp_cross_entropy_formula, qp_cross_entropy_chart_two_events)
        group3 = VGroup(p_entropy_text, p_entropy_formula, p_entropy_chart_two_events)
        group4 = VGroup(pq_cross_entropy_text, pq_cross_entropy_formula, pq_cross_entropy_chart_two_events)
        self.play(self.camera.frame.animate.scale(0.5).move_to(group1).shift(RIGHT * 0.4), run_time=2)
        information_1 = Tex(
            R"-\log_2 0.5 = 1", font_size=30
        ).set_color(PURE_MAGENTA).next_to(q_entropy_chart_two_events.bars[0], UP, buff=0.1)
        information_2 = Tex(
            R"-\log_2 0.5 = 1", font_size=30
        ).set_color(LIGHT_PINK).next_to(q_entropy_chart_two_events.bars[1], UP, buff=0.1)
        self.play(Write(information_1), Write(information_2))
        self.wait(2)

        # Explain the entropy of P
        v = group3.get_center() - group1.get_center()
        v_perp = [-v[1], v[0], 0]
        self.play(
            self.camera.frame.animate(path_arc=PI * 0.8, path_arc_axis=v_perp).move_to(
                group3
            ), run_time=2.5)
        information_3 = Tex(
            R"-\log_2 0.9 \approx 0.15", font_size=30
        ).set_color(GREEN_B).next_to(p_entropy_chart_two_events.bars[0], UP, buff=0.1)
        information_4 = Tex(
            R"-\log_2 0.1 \approx 3.32", font_size=30
        ).set_color(GREEN_D).next_to(p_entropy_chart_two_events.bars[1], UP, buff=0.1).align_to(p_entropy_chart_two_events.bars[1], RIGHT)
        self.play(Write(information_3))
        self.wait(2)
        self.play(Write(information_4))

        # Prepare for calculation
        self.play(FadeOut(VGroup(information_1, information_2, information_3, information_4)), self.camera.frame.animate.restore(), run_time=2)
        dividing_line = Line(self.camera.frame.get_left(), self.camera.frame.get_right())
        self.play(FadeOut(VGroup(group1, group3)), ShowCreation(dividing_line))

        # Calculate cross entropy of Q relative to P
        calculation_1 = Tex(
            R"0.9(-\log_2 0.5) \\ +\ 0.1(-\log_2 0.5) \\ \approx " +
            str(round(sum([p * -math.log2(q) for q, p in zip(distribution_1, distribution_2)]), 2)),
            font_size=80,
            tex_to_color_map={"0.9": GREEN, "0.1": GREEN, "0.5": PINK}
        ).match_y(VGroup(qp_cross_entropy_text, qp_cross_entropy_chart)).match_x(pq_cross_entropy_chart).shift(RIGHT * 2)
        calculation_1[28:].set_color(TEAL)
        self.play(Write(calculation_1), run_time=3)
        self.wait(0.5)
        self.play(FancyCircumscribe(VGroup(calculation_1["0.9"], calculation_1["0.1"]), run_time=5))

        # Calculate cross entropy of P relative to Q
        calculation_2 = Tex(
            R"0.5(-\log_2 0.9) \\ +\ 0.5(-\log_2 0.1) \\ \approx " +
            str(round(sum([q * -math.log2(p) for q, p in zip(distribution_1, distribution_2)]), 2)),
            font_size=80,
            tex_to_color_map={"0.9": GREEN, "0.1": GREEN, "0.5": PINK}
        ).match_y(VGroup(pq_cross_entropy_text, pq_cross_entropy_chart)).match_x(qp_cross_entropy_chart).shift(LEFT * 2)
        calculation_2[28:].set_color(TEAL)
        self.play(Write(calculation_2), run_time=3)

        # Compare the results
        comparision = Tex(
            R"1.0 \neq 1.74", font_size=80
        ).set_color(
            TEAL
        ).set_color_by_tex(
            R"\neq", PURE_RED
        )
        background = VGroup(group2, group4, calculation_1, calculation_2)
        background.save_state()
        self.play(
            dividing_line.animate.set_opacity(0.15),
            background.animate.fade(0.8),
            AnimationGroup(
                AnimationGroup(
                    TransformFromCopy(calculation_1["1.0"], comparision["1.0"], path_arc=-PI * 0.2),
                    TransformFromCopy(calculation_2["1.74"], comparision["1.74"], path_arc=PI * 0.2)
                ),
                FadeIn(comparision[R"\neq"]), lag_ratio=0.8)
        )
        self.wait(1)
        self.play(
            FadeOut(dividing_line, run_time=1),
            FadeOut(comparision, run_time=1),
            FadeIn(group1, run_time=2),
            FadeIn(group3, run_time=2),
            background.animate(run_time=2).restore(),
            FadeOut(calculation_1, run_time=1.5),
            FadeOut(calculation_2, run_time=1.5)
        )
        self.wait(2)

        # Generalize the two-event distributions
        q_entropy_chart_two_events_general = EntropyChart(
            distribution_1,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(F"q_{str(i + 1)}", font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).move_to(q_entropy_chart)

        qp_cross_entropy_chart_two_events_general = EntropyChart(
            distribution_2,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(F"p_{str(i + 1)}", font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            bar_heights=[-math.log2(q) for q in distribution_1],
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 q_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).move_to(qp_cross_entropy_chart)

        p_entropy_chart_two_events_general = EntropyChart(
            distribution_2,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(F"p_{str(i + 1)}", font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            width=second_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[GREEN_B, GREEN_D],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(p_entropy_chart)

        pq_cross_entropy_chart_two_events_general = EntropyChart(
            distribution_1,
            event_labels=VGroup(*[
                Tex("s_" + str(i + 1), font_size=35).set_color(BLACK)
                for i in range(2)
            ]),
            probability_labels=VGroup(*[
                Tex(F"q_{str(i + 1)}", font_size=42)
                for i in range(2)
            ]),
            bar_labels=None,
            bar_heights=[-math.log2(p) for p in distribution_2],
            width=first_distribution_chart.get_width(),
            height=2.3,
            include_vertical_axis=True,
            vertical_axis_label_text=R"\begin{gathered}-\log_2 p_i \\ \ (\text{bits})\end{gathered}",
            vertical_axis_font_size=30,
            segments_height=0.4,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK],
            bar_fill_colors=[GREEN_B, GREEN_D]
        ).move_to(pq_cross_entropy_chart)
        q_entropy_chart_two_events_general.add_updater(lambda m: m.set_stroke(width=0.5))
        qp_cross_entropy_chart_two_events_general.add_updater(lambda m: m.set_stroke(width=0.5))
        p_entropy_chart_two_events_general.add_updater(lambda m: m.set_stroke(width=0.5))
        pq_cross_entropy_chart_two_events_general.add_updater(lambda m: m.set_stroke(width=0.5))

        self.play(
            AnimationGroup(
                FadeIn(
                    VGroup(
                        q_entropy_chart_two_events_general,
                        qp_cross_entropy_chart_two_events_general,
                        p_entropy_chart_two_events_general,
                        pq_cross_entropy_chart_two_events_general
                    ), suspend_mobject_updating=True),
                FadeOut(
                    VGroup(
                        q_entropy_chart_two_events,
                        qp_cross_entropy_chart_two_events,
                        p_entropy_chart_two_events,
                        pq_cross_entropy_chart_two_events
                    )
                ), lag_ratio=0.2)
        )
        q_entropy_chart = q_entropy_chart_two_events_general
        qp_cross_entropy_chart = qp_cross_entropy_chart_two_events_general
        p_entropy_chart = p_entropy_chart_two_events_general
        pq_cross_entropy_chart = pq_cross_entropy_chart_two_events_general

        # Play around with the distrbutions
        for i in range(20):
            new_distribution_1 = random_distribution(2, thresh=1 / 8) if i % 2 == 1 else [t.get_value() for t in q_entropy_chart.distribution_trackers]
            new_distribution_2 = random_distribution(2, thresh=1 / 8) if i % 2 == 0 else [t.get_value() for t in p_entropy_chart.distribution_trackers]
            anims = [
                AnimationGroup(
                    q_entropy_chart.set_distribution(new_distribution_1),
                    qp_cross_entropy_chart.set_distribution(new_distribution_2),
                    p_entropy_chart.set_distribution(new_distribution_2),
                    pq_cross_entropy_chart.set_distribution(new_distribution_1),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(q))
                        for h, q in zip(qp_cross_entropy_chart.bar_heights, new_distribution_1)
                    ]),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(p))
                        for h, p in zip(pq_cross_entropy_chart.bar_heights, new_distribution_2)
                    ]), run_time=2)
            ]

            if i == 3:
                # Highlight q_1 and add the number line
                circ_opacity_tracker_1 = ValueTracker(0)
                circ1 = always_redraw(
                    lambda: Circle(
                        stroke_width=2,
                        stroke_color=YELLOW,
                        stroke_opacity=circ_opacity_tracker_1.get_value()
                    ).surround(
                        q_entropy_chart.probability_labels[0],
                        buff=0.2
                    )
                )
                circ2 = always_redraw(
                    lambda: Circle(
                        stroke_width=2,
                        stroke_color=YELLOW,
                        stroke_opacity=circ_opacity_tracker_1.get_value()
                    ).surround(
                        pq_cross_entropy_chart.probability_labels[0],
                        buff=0.2
                    )
                )
                self.add(circ1, circ2)
                anims.append(circ_opacity_tracker_1.animate.set_value(1))

                number_line_q = NumberLine(
                    [0, 1, 0.1],
                    include_numbers=True,
                    numbers_to_exclude=[0.1 * i for i in range(1, 10)],
                    width=q_entropy_chart.segments.get_width()
                ).next_to(q_entropy_chart.bars, DOWN, buff=1.6)
                self.add(number_line_q)
                q1_dot = Group(TrueDot(), GlowDot()).set_color(PURE_MAGENTA)
                q1_dot.add_updater(lambda m: m.move_to(number_line_q.n2p(q_entropy_chart.distribution_trackers[0].get_value())))
                q1_triangle = Triangle(fill_opacity=0.7, fill_color=PURE_MAGENTA, stroke_width=0).stretch(1.5, 1).set_width(0.15)
                q1_triangle.add_updater(
                    lambda m: m.next_to(number_line_q.n2p(q_entropy_chart.distribution_trackers[0].get_value()), DOWN, buff=0)
                )
                q1_label = Tex("q_1", font_size=42).set_color(PURE_MAGENTA)
                q1_label.add_updater(lambda m: m.next_to(q1_triangle, DOWN, buff=0.1))
                number_line_q_group = Group(number_line_q, q1_dot, q1_triangle, q1_label)
                number_line_q_opacity_tracker = ValueTracker(0)
                number_line_q_group.add_updater(lambda m: m.set_opacity(number_line_q_opacity_tracker.get_value()))
                self.add(number_line_q_group)
                anims.append(number_line_q_opacity_tracker.animate.set_value(1))
            if i == 4:
                # Highlight q_2
                anims.append(circ_opacity_tracker_1.animate.set_value(0))

                circ_opacity_tracker_2 = ValueTracker(0)
                circ3 = always_redraw(
                    lambda: Circle(
                        stroke_width=2,
                        stroke_color=YELLOW,
                        stroke_opacity=circ_opacity_tracker_2.get_value()
                    ).surround(
                        q_entropy_chart.probability_labels[1],
                        buff=0.2
                    )
                )
                circ4 = always_redraw(
                    lambda: Circle(
                        stroke_width=2,
                        stroke_color=YELLOW,
                        stroke_opacity=circ_opacity_tracker_2.get_value()
                    ).surround(
                        pq_cross_entropy_chart.probability_labels[1],
                        buff=0.2
                    )
                )
                self.add(circ3, circ4)
                anims.append(circ_opacity_tracker_2.animate.set_value(1))
            if i == 5:
                # Replace q_2 with 1 - q_1
                anims.append(circ_opacity_tracker_2.animate.set_value(0))

                new_q2_label_1 = always_redraw(
                    lambda: Tex(
                        "1 - q_1", font_size=42
                    ).set_color(
                        LIGHT_PINK
                    ).move_to(
                        q_entropy_chart.probability_labels[1]
                    ).set_opacity(
                        1 - circ_opacity_tracker_2.get_value()
                    )
                )
                self.add(new_q2_label_1)
                q_entropy_chart.probability_labels[1].add_updater(lambda m: m.set_opacity(circ_opacity_tracker_2.get_value()))

                new_q2_label_2 = always_redraw(
                    lambda: Tex(
                        "1 - q_1", font_size=42
                    ).set_color(
                        LIGHT_PINK
                    ).move_to(
                        pq_cross_entropy_chart.probability_labels[1]
                    ).set_opacity(
                        1 - circ_opacity_tracker_2.get_value()
                    )
                )
                self.add(new_q2_label_2)
                pq_cross_entropy_chart.probability_labels[1].add_updater(lambda m: m.set_opacity(circ_opacity_tracker_2.get_value()))
            if i == 7:
                # Highlight the p distirbution
                rect_opacity_tracker = ValueTracker(0)
                rect1 = always_redraw(
                    lambda: SurroundingRectangle(
                        qp_cross_entropy_chart.probability_labels,
                        buff=0.1,
                        stroke_width=1.5,
                        stroke_color=YELLOW,
                        stroke_opacity=rect_opacity_tracker.get_value()
                    )
                )
                rect2 = always_redraw(
                    lambda: SurroundingRectangle(
                        p_entropy_chart.probability_labels,
                        buff=0.1,
                        stroke_width=1.5,
                        stroke_color=YELLOW,
                        stroke_opacity=rect_opacity_tracker.get_value()
                    )
                )
                self.add(rect1, rect2)
                anims.append(rect_opacity_tracker.animate.set_value(1))

                number_line_p = NumberLine(
                    [0, 1, 0.1],
                    include_numbers=True,
                    numbers_to_exclude=[0.1 * i for i in range(1, 10)],
                    width=qp_cross_entropy_chart.segments.get_width()
                ).next_to(qp_cross_entropy_chart.bars, DOWN, buff=1.6)
                self.add(number_line_p)
                p1_dot = Group(TrueDot(), GlowDot()).set_color(GREEN_B)
                p1_dot.add_updater(lambda m: m.move_to(number_line_p.n2p(qp_cross_entropy_chart.distribution_trackers[0].get_value())))
                p1_triangle = Triangle(
                    fill_opacity=0.7, fill_color=GREEN_B, stroke_width=0
                ).stretch(1.5, 1).set_width(0.15).flip(axis=RIGHT)
                p1_triangle.add_updater(
                    lambda m: m.next_to(number_line_p.n2p(qp_cross_entropy_chart.distribution_trackers[0].get_value()), UP, buff=0)
                )
                p1_label = Tex("p_1", font_size=42).set_color(GREEN_B)
                p1_label.add_updater(lambda m: m.next_to(p1_triangle, UP, buff=0.1))
                number_line_p_group = Group(number_line_p, p1_dot, p1_triangle, p1_label)
                number_line_p_opacity_tracker = ValueTracker(0)
                number_line_p_group.add_updater(lambda m: m.set_opacity(number_line_p_opacity_tracker.get_value()))
                self.add(number_line_p_group)
                anims.append(number_line_p_opacity_tracker.animate.set_value(1))
            if i == 9:
                # Replace the p_2 labels with 1 - p_1
                anims.append(rect_opacity_tracker.animate.set_value(0))

                dummy_p = Tex("p", font_size=42)
                new_p2_label_1 = always_redraw(
                    lambda: Tex(
                        "1 - p_1", font_size=42
                    ).set_color(
                        GREEN_D
                    ).move_to(
                        qp_cross_entropy_chart.probability_labels[1]
                    ).set_opacity(
                        1 - rect_opacity_tracker.get_value()
                    ).scale(qp_cross_entropy_chart.probability_labels[0][0].get_height() / dummy_p.get_height())
                )
                self.add(new_p2_label_1)
                qp_cross_entropy_chart.probability_labels[1].add_updater(lambda m: m.set_opacity(rect_opacity_tracker.get_value()))

                new_p2_label_2 = always_redraw(
                    lambda: Tex(
                        "1 - p_1", font_size=42
                    ).set_color(
                        GREEN_D
                    ).move_to(
                        p_entropy_chart.probability_labels[1]
                    ).set_opacity(
                        1 - rect_opacity_tracker.get_value()
                    )
                )
                self.add(new_p2_label_2)
                p_entropy_chart.probability_labels[1].add_updater(lambda m: m.set_opacity(rect_opacity_tracker.get_value()))
            self.play(*anims)
            if i == 4:
                self.remove(circ1, circ2)
            if i == 5:
                self.remove(circ3, circ4)
            if i == 9:
                self.remove(rect1, rect2)
        self.wait(1)

        # Switch to graphs
        q1_dot.add_updater(lambda m: self.bring_to_front(m))
        p1_dot.add_updater(lambda m: self.bring_to_front(m))
        max_y = 4
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, max_y],
            width=number_line_q.get_width(),
            height=5
        )
        coordinate_labels_x = axes.add_coordinate_labels(
            x_values=[0, 1],
            y_values=[],
            excluding=[]
        ),
        coordinate_labels_y = axes.add_coordinate_labels(
            x_values=[],
            y_values=[i for i in range(max_y + 1)],
            excluding=[],
            direction=LEFT
        )
        axes.scale(1.3).align_to(number_line_q, RIGHT).shift(RIGHT * 2.3).align_to(self.camera.frame.get_bottom(), DOWN).shift(UP * 2)
        axes.get_x_axis().set_opacity(0)

        group1 = VGroup(q_entropy_text, q_entropy_formula, q_entropy_chart)
        group2 = VGroup(qp_cross_entropy_text, qp_cross_entropy_formula, qp_cross_entropy_chart)
        group3 = VGroup(p_entropy_text, p_entropy_formula, p_entropy_chart)
        group4 = VGroup(pq_cross_entropy_text, pq_cross_entropy_formula, pq_cross_entropy_chart)
        number_line_q.generate_target()
        number_line_q.target.match_width(axes.get_x_axis()).move_to(axes.get_x_axis())
        y_axis_label = qp_cross_entropy_formula.copy().scale(1.3).next_to(axes.get_y_axis(), LEFT, buff=0.3)
        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(VGroup(q_entropy_text, q_entropy_formula, q_entropy_chart, new_q2_label_1), run_time=1, suspend_mobject_updating=True),
                    FadeOut(VGroup(new_q2_label_2, new_p2_label_2, group3, group4), shift=DOWN * 4, run_time=1, suspend_mobject_updating=True),
                    AnimationGroup(
                        AnimationGroup(
                            MoveToTarget(number_line_q, run_time=2),
                            VGroup(
                                qp_cross_entropy_text, qp_cross_entropy_formula, qp_cross_entropy_chart, number_line_p, new_p2_label_1
                            ).animate(run_time=2).scale(1.3).shift(RIGHT * 0.5).align_to(axes, DOWN),
                            TransformFromCopy(qp_cross_entropy_formula, y_axis_label, run_time=1.5)
                        ),
                        FadeIn(axes, shift=DOWN * 5 + LEFT, run_time=1.5), lag_ratio=0.2)
                ), lag_ratio=0.8)
        )
        self.remove(new_q2_label_1, new_q2_label_2, new_p2_label_2)
        self.wait(2)

        # Fix P in place
        pin = SVGMobject("push_pin.svg").rotate(35 * DEG).scale(0.325).set_color(GREY).align_to(
            number_line_p.n2p(qp_cross_entropy_chart.distribution_trackers[0].get_value()), DR
        )
        pin.set_fill([GREY_D, GREY_B], 1)
        self.play(FadeIn(pin, shift=RIGHT * 0.25 + DOWN * 0.125, run_time=2))
        self.wait(2)

        # Create the graph
        # epsilon = 5.6e-17
        epsilon = 1e-2
        infinity = 10

        def f(q1):
            if q1 < epsilon:
                f_of_epsilon = f(epsilon)
                return ((f_of_epsilon - infinity) / epsilon) * (q1 - epsilon) + f_of_epsilon
            if q1 > 1 - epsilon:
                f_of_1_minus_epsilon = f(1 - epsilon)
                return ((infinity - f_of_1_minus_epsilon) / epsilon) * (q1 - (1 - epsilon)) + f_of_1_minus_epsilon
            return sum([t.get_value() * -math.log2(q) for t, q in zip(qp_cross_entropy_chart.distribution_trackers, [q1, 1 - q1])])

        min_step = 0.001
        max_step = 0.01

        def calculate_step(p):
            # return -4*max_step*(p - 0.5)**2 + max_step
            if 0 <= p < 0.5:
                return 2 * max_step * (p - 0.5) + max_step
            return -2 * max_step * (p - 0.5) + max_step

        def get_curve():
            step = clip(calculate_step(qp_cross_entropy_chart.distribution_trackers[0].get_value()), min_step, max_step)
            return axes.get_graph(
                f, x_range=[0, 1, step]
            ).set_stroke(
                width=2, color=PINK
            ).insert_n_curves(100)
        graph = always_redraw(get_curve)
        graph.suspend_updating()
        graph.insert_n_curves(10000)
        f_of_q_dot = Group(TrueDot(radius=0.1), GlowDot(glow_factor=1)).set_color(PURE_MAGENTA)
        f_of_q_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    q_entropy_chart.distribution_trackers[0].get_value(),
                    f(q_entropy_chart.distribution_trackers[0].get_value())
                )
            )
        )
        self.play(
            AnimationGroup(
                ShowCreation(graph, suspend_mobject_updating=True, run_time=3),
                FadeIn(f_of_q_dot, suspend_mobject_updating=True), lag_ratio=0.8)
        )
        f_of_q_dot.add_updater(lambda m: self.bring_to_front(m))

        # Change q_1
        for i in range(17):
            if i == 2:
                q1 = 0.2718
            elif i == 3:
                q1 = 0.123
            elif i == 4 or i == 10 or i == 16:
                q1 = qp_cross_entropy_chart.distribution_trackers[0].get_value()
            else:
                q1 = random.uniform(1 / 32, 1)
            distribution = [q1, 1 - q1]
            anims = [
                AnimationGroup(
                    q_entropy_chart.set_distribution(distribution),
                    AnimationGroup(*[
                        h.animate.set_value(-math.log2(q))
                        for h, q in zip(qp_cross_entropy_chart.bar_heights, distribution)
                    ]), run_time=2)
            ]
            if i == 1:
                min_value_arrow = Arrow(ORIGIN, DOWN * 1.8, thickness=5).next_to(
                    axes.c2p(
                        qp_cross_entropy_chart.distribution_trackers[0].get_value(),
                        f(qp_cross_entropy_chart.distribution_trackers[0].get_value())
                    ),
                    UP, buff=0
                )
                min_value_text = Tex(R"\text{min} = \displaystyle\sum_i p_i (-\log_2 p_i)", font_size=35).next_to(min_value_arrow, UP, buff=-0.1)
                min_value_text["p_i"].set_color(GREEN)
                min_text = min_value_text["min"]
                min_value_text.shift(RIGHT * (min_value_arrow.get_x() - min_text.get_x()))
                anims.append(
                    AnimationGroup(
                        FadeIn(min_value_arrow, shift=DOWN * 0.3, run_time=1.5),
                        Write(min_text, run_time=1.5), lag_ratio=0.2)
                )
            if i == 3:
                number_line_p_group_copy = Group(number_line_p, pin, p1_dot, p1_triangle, p1_label).copy().clear_updaters()
                number_line_p_copy = number_line_p_group_copy[0]
                pin_copy = number_line_p_group_copy[1]
                p1_dot_copy = number_line_p_group_copy[2]
                p1_triangle_copy = number_line_p_group_copy[3]
                p1_label_copy = number_line_p_group_copy[4]
                p1_dot_copy.add_updater(
                    lambda m: m.move_to(number_line_p_copy.n2p(qp_cross_entropy_chart.distribution_trackers[0].get_value()))
                )
                p1_triangle_copy.add_updater(
                    lambda m: m.next_to(number_line_p_copy.n2p(qp_cross_entropy_chart.distribution_trackers[0].get_value()), UP, buff=0)
                )
                p1_label_copy.add_updater(lambda m: m.next_to(p1_triangle_copy, UP, buff=0.1))
                number_line_p_group_copy.suspend_updating()

                anims.append(
                    number_line_p_group_copy.animate(
                        run_time=2, path_arc=PI * 0.2
                    ).match_width(
                        number_line_q
                    ).match_x(
                        number_line_q.align_to(number_line_q, DOWN)
                    )
                )
            if i == 4:
                anims.append(FadeOut(number_line_p_group_copy[0]))
            # if i == 16:
            #     anims.append(Write(min_value_text[len("min"):], run_time = 2))

            self.play(*anims)

        # Clean up
        epsilon_2 = 0.001

        def g(p1):
            if p1 < epsilon_2 or p1 > 1 - epsilon_2:
                return 0
            return sum([p * -math.log2(p) for p in [p1, 1 - p1]])
        min_value_dot = f_of_q_dot.copy().clear_updaters().set_color(GREEN).set_opacity(0.5)
        min_value_dot.add_updater(
            lambda m: m.move_to(
                axes.c2p(
                    qp_cross_entropy_chart.distribution_trackers[0].get_value(),
                    g(qp_cross_entropy_chart.distribution_trackers[0].get_value())
                )
            )
        )
        q1_label.clear_updaters()
        f_of_q_dot.clear_updaters()
        self.remove(q1_dot)
        self.play(
            FadeOut(Group(min_text, min_value_arrow, f_of_q_dot, q1_triangle), suspend_mobject_updating=True),
            FadeOut(Group(pin, pin_copy), shift=LEFT * 0.25 + UP * 0.125),
            q1_label.animate.next_to(axes.get_x_axis()[0], RIGHT),
            FadeIn(min_value_dot, suspend_mobject_updating=True)
        )

        # Trace the minimum value of the graph
        number_line_p_group_copy.resume_updating()
        path = TracingTail(min_value_dot, time_traced=5, stroke_color=GREEN)
        self.add(path)
        self.wait(3)
        graph.resume_updating()
        self.play(qp_cross_entropy_chart.set_distribution([1 - epsilon_2, epsilon_2]), run_time=4)
        self.play(qp_cross_entropy_chart.set_distribution([epsilon_2, 1 - epsilon_2]), run_time=4)
        graph.suspend_updating()

        # Replace the traced path with the full graph of the entropy of P
        p_entropy_graph = axes.get_graph(
            g, x_range=[0, 1, 0.01]
        ).set_stroke(
            width=2, color=GREEN
        ).insert_n_curves(100)
        # self.wait(1)
        # self.remove(path)
        self.play(FadeIn(p_entropy_graph), run_time=2)
        # self.wait(1)

        # Move around the distribution some more and write the entropy formula for p next to the new graph
        graph.resume_updating()
        for i in range(20):
            anims = [qp_cross_entropy_chart.set_distribution(random_distribution(2, thresh=1 / 8))]
            if i == 0:
                entropy_of_p = min_value_text[len("min="):].scale(0.85).next_to(
                    p_entropy_graph, RIGHT, buff=-1
                ).shift(
                    UP * 0.7
                ).set_stroke(
                    width=3, color=BLACK, behind=True
                )
                self.play(Write(entropy_of_p, stroke_color=WHITE))
            self.play(*anims, run_time=4)


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
