# ==============================================================================
# Scene:      PerfectEncodingsAndEntropyDefinitionV2
# Source:     videos/_2026/cross_entropy/robot.py (lines 2921-3345)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl PerfectEncodingsAndEntropyDefinitionV2.py PerfectEncodingsAndEntropyDefinitionV2 -w -m --fps 15
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


class PerfectEncodingsAndEntropyDefinitionV2(InteractiveScene):
    def construct(self):
        # Bring back the huffman chart to show that it's a perfect encoding
        distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        encoding = ["0", "10", "110", "111"]
        full_huffman_chart = EntropyChart(
            distribution,
            event_labels=VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)]).set_color(PINK),
            probability_labels=[
                Tex(R"\frac{1}{" + ["2", "4", "8", "8"][i] + "}", font_size=40)
                for i in range(4)
            ],
            bar_labels=[
                Tex(encoding[i], font_size=40)
                for i in range(4)
            ],
            bar_heights=[1, 2, 3, 3],
            width=9,
            height=3,
            segments_height=1,
            fill_colors=[PURE_MAGENTA, LIGHT_PINK]
        ).center().shift(DOWN * 0.7)
        full_huffman_chart.bar_labels.set_color(WHITE)
        full_huffman_chart.vertical_axis.set_opacity(0)
        full_huffman_chart.vertical_axis_label.set_opacity(0)
        full_huffman_chart.reference_lines.set_opacity(0)
        self.camera.frame.match_x(full_huffman_chart.bars)
        self.add(full_huffman_chart)
        self.wait(1.5)

        # Calculate the entropy
        weighted_sum_lines = VGroup(
            Tex(R"\frac{1}{2} \cdot 1", font_size=36).next_to(full_huffman_chart.bars[0], UP),
            Tex(R"\frac{1}{4} \cdot 2", font_size=36).next_to(full_huffman_chart.bars[1], UP),
            Tex(R"\frac{1}{8} \cdot 3", font_size=36).next_to(full_huffman_chart.bars[2], UP),
            Tex(R"\frac{1}{8} \cdot 3", font_size=36).next_to(full_huffman_chart.bars[3], UP)
        )
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    TransformFromCopy(label, line[:-2]),
                    FadeIn(line[-2:], shift=UP * 0.1), run_time=1.5)
                for label, line in zip(full_huffman_chart.probability_labels, weighted_sum_lines)
            ], lag_ratio=0.3)
        )
        self.wait(0.35)

        # Show the weighted sum result
        sum_result = Tex(
            R"\frac{1}{2} \cdot 1 + \frac{1}{4} \cdot 2 + \frac{1}{8} \cdot 3 + \frac{1}{8} \cdot 3 = 1.75 \text{ bits}",
            font_size=45
        ).to_edge(UP, buff=1.5).fix_in_frame()

        self.play(TransformMatchingShapes(weighted_sum_lines, sum_result[:-9], path_arc=PI * 0.2, run_time=1.5))
        self.play(FadeIn(sum_result[R"= 1.75 \text{ bits}"]))
        self.wait(2)

        # Compare the message length to the information
        information_labels = VGroup(*[
            Tex(
                str(num_bits) + R"\text{ bit" + ("s" if num_bits > 1 else "") + "}",
                font_size=40
            ).set_stroke(
                width=3, color=BLACK, behind=True
            ).next_to(full_huffman_chart.bars[i], UP)
            for i, num_bits in enumerate([1, 2, 3, 3])
        ])
        self.play(
            AnimationGroup(*[
                AnimationGroup(
                    Indicate(VGroup(bar, label), scale_factor=1.1, suspend_mobject_updating=True),
                    FadeIn(info_label, shift=UP * 0.1)
                )
                for bar, label, info_label in zip(full_huffman_chart.bars, full_huffman_chart.bar_labels, information_labels)
            ], lag_ratio=0.2),
            full_huffman_chart.bar_labels.animate.shift(0), run_time=1.3)

        refernce_lines_opacity_tracker = ValueTracker(0)
        full_huffman_chart.reference_lines.add_updater(lambda m: self.bring_to_back(m.set_opacity(refernce_lines_opacity_tracker.get_value())))
        self.play(
            sum_result.animate.scale(0.8).to_edge(UP, buff=0.7).match_x(full_huffman_chart.reference_lines),
            VGroup(
                full_huffman_chart.vertical_axis,
                full_huffman_chart.vertical_axis_label
            ).animate.set_opacity(1),
            refernce_lines_opacity_tracker.animate.set_value(1),
            self.camera.frame.animate.match_x(full_huffman_chart),
            VGroup(
                full_huffman_chart.bars,
                full_huffman_chart.bar_labels
            ).animate.shift(0), run_time=1)

        full_huffman_chart.suspend_updating()
        full_huffman_chart.save_state()
        information_labels.save_state()
        reference_lines_order = [1, 2, 3, 3]
        for i in range(4):
            self.play(
                VGroup(
                    information_labels[i],
                    full_huffman_chart.bars[i],
                    full_huffman_chart.bar_labels[i],
                    full_huffman_chart.segments.bars[i],
                    full_huffman_chart.event_labels[i],
                    full_huffman_chart.probability_labels[i],
                ).animate.set_opacity(1),
                full_huffman_chart.reference_lines[reference_lines_order[i]].animate.set_opacity(1).set_color(YELLOW),
                VGroup(
                    information_labels[:i],
                    full_huffman_chart.bars[:i],
                    full_huffman_chart.bar_labels[:i],
                    full_huffman_chart.segments.bars[:i],
                    full_huffman_chart.event_labels[:i],
                    full_huffman_chart.probability_labels[:i],
                    information_labels[i + 1:],
                    full_huffman_chart.bars[i + 1:],
                    full_huffman_chart.bar_labels[i + 1:],
                    full_huffman_chart.segments.bars[i + 1:],
                    full_huffman_chart.event_labels[i + 1:],
                    full_huffman_chart.probability_labels[i + 1:]
                ).animate.set_opacity(0.1),
                full_huffman_chart.reference_lines[:reference_lines_order[i]].animate.set_opacity(0.1).set_color(WHITE),
                full_huffman_chart.reference_lines[reference_lines_order[i] + 1:].animate.set_opacity(0.1).set_color(WHITE), run_time=0.8)
        self.play(
            full_huffman_chart.animate.restore(),
            information_labels.animate.restore()
        )
        full_huffman_chart.resume_updating()

        # Generalize
        distribution = random_distribution(7)
        general_chart = EntropyChart(
            random_distribution(7),
            event_labels=VGroup(*[
                Tex(
                    (("s_" + str(i)) if i < len(distribution) - 2 else R"\ldots" if i == len(distribution) - 2 else "s_n")
                ).scale(0.8).set_color(BLACK)
                for i in range(len(distribution))
            ]),
            probability_labels=VGroup(*[
                Tex(
                    (("p_" + str(i)) if i < len(distribution) - 2 else R"\ldots" if i == len(distribution) - 2 else "p_n")
                )
                for i in range(len(distribution))
            ]),
            width=9,
            height=3,
            segments_height=0.4,
            fit_event_labels_to_height=False,
            fill_colors=[YELLOW_B, YELLOW_D]
        ).match_width(full_huffman_chart).match_x(full_huffman_chart).align_to(full_huffman_chart, UP)
        general_chart.bars.add_updater(lambda m: m.set_stroke(width=1))
        general_chart.segments.bars.set_stroke(width=1)
        self.camera.frame.save_state()
        full_huffman_chart.suspend_updating()
        self.play(
            # self.camera.frame.animate(run_time = 5).match_x(general_chart.segments),
            AnimationGroup(
                FadeOut(
                    VGroup(
                        sum_result,
                        information_labels,
                        full_huffman_chart.bars,
                        full_huffman_chart.bar_labels,
                        full_huffman_chart.segments.bars,
                        full_huffman_chart.event_labels,
                        full_huffman_chart.probability_labels
                    ), suspend_mobject_updating=True),
                AnimationGroup(*[
                    AnimationGroup(GrowFromCenter(segment), GrowFromEdge(bar, DOWN), FadeIn(p_label))
                    for segment, bar, p_label in zip(
                        general_chart.segments.bars, general_chart.bars, general_chart.probability_labels
                    )
                ], lag_ratio=0.2, suspend_mobject_updating=True),
                AnimationGroup(
                    FadeOut(VGroup(full_huffman_chart.vertical_axis, full_huffman_chart.vertical_axis_label, full_huffman_chart.reference_lines)),
                    FadeIn(VGroup(general_chart.vertical_axis, general_chart.vertical_axis_label, general_chart.reference_lines))
                ),
                AnimationGroup(*[
                    FadeIn(symbol)
                    for symbol in general_chart.event_labels
                ], lag_ratio=0.3), lag_ratio=0.5, run_time=6)
        )

        # Move around the probabilities and write the definition of entropy
        self.add(general_chart)
        general_chart.save_state()
        bars_opacity_tracker = ValueTracker(0.8)
        general_chart.bars.add_updater(lambda m: m.set_opacity(bars_opacity_tracker.get_value()))
        general_chart.bars.add_updater(lambda m: self.bring_to_front(m))
        for i in range(20):
            anims = [general_chart.set_distribution(random_distribution(7))]
            if i == 1:
                weighted_sum_formula = Tex(
                    R"\text{Avg. information} = \sum_i p_i (-\log_2 p_i)"
                ).next_to(general_chart.reference_lines, UP)
                anims.append(Write(weighted_sum_formula, run_time=9))
            if i == 5:
                anims.append(bars_opacity_tracker.animate.set_value(0.1))
            if i == 7:
                brace = Brace(general_chart.segments, UP)
                total_width_text = brace.get_tex(R"\text{Total width} = 1")
                anims.append(
                    AnimationGroup(
                        GrowFromEdge(brace, DOWN),
                        Write(total_width_text), run_time=2)
                )
            if i == 8:
                anims.append(
                    AnimationGroup(
                        FadeOut(VGroup(brace, total_width_text)),
                        bars_opacity_tracker.animate.set_value(1)
                    )
                )
            if i == 10:
                anims.append(FancyCircumscribe(general_chart.vertical_axis_label, run_time=5))
            if i == 13:
                # Add the area formula
                weighted_sum_formula_area = Tex(
                    R"\text{Avg. information} = \sum_i p_i (-\log_2 p_i) = \text{Area}()"
                ).move_to(weighted_sum_formula)
                bars_copy = general_chart.bars.copy()
                bars_copy.clear_updaters().set_opacity(1)
                bars_copy.generate_target()
                bars_copy_height = bars_copy.get_height()
                scale_factor = weighted_sum_formula_area[-2].get_height() / bars_copy_height
                bars_copy.target.stretch(0.5, 0).scale(scale_factor).next_to(weighted_sum_formula_area[-2], RIGHT)
                weighted_sum_formula_area[-1].next_to(bars_copy.target, RIGHT)
                weighted_sum_formula_area[-1].shift(DOWN * (weighted_sum_formula_area[-1].get_y() - weighted_sum_formula_area[-2].get_y()))
                VGroup(weighted_sum_formula_area, bars_copy.target).set_x(0)
                self.play(
                    AnimationGroup(
                        AnimationGroup(
                            ReplacementTransform(weighted_sum_formula, weighted_sum_formula_area[:-len("=Area()")], run_time=1.5),
                            Write(weighted_sum_formula_area[-len("=Area()"):], run_time=2), lag_ratio=0.6),
                        MoveToTarget(bars_copy, run_time=3)
                    )
                )

                def update_area_bars(m):
                    m.become(
                        general_chart.bars.copy()
                        .clear_updaters()
                        .set_opacity(1)
                        .stretch(0.5, 0)
                        .scale(scale_factor)
                        .next_to(weighted_sum_formula_area[-2], RIGHT)
                        .align_to(m, DOWN)
                    )
                bars_copy.add_updater(update_area_bars)
            if i == 18:
                # Write it as H(P)
                weighted_sum_formula_h = Tex(
                    R"H(P) = \sum_i p_i (-\log_2 p_i) = \text{Area}()"
                ).move_to(weighted_sum_formula_area).align_to(weighted_sum_formula_area, RIGHT)
                weighted_sum_formula_h[:-1].align_to(weighted_sum_formula_area[:-1], RIGHT)
                weighted_sum_formula_h[-1].next_to(bars_copy.target, RIGHT)
                weighted_sum_formula_h[-1].shift(DOWN * (weighted_sum_formula_h[-1].get_y() - weighted_sum_formula_h[-2].get_y()))
                weighted_sum_formula_h.match_x(general_chart.reference_lines)
                entropy_text = TexText("``Entropy''", font_size=25).next_to(weighted_sum_formula_h["H(P)"], DOWN)
                anims.append(
                    AnimationGroup(
                        AnimationGroup(
                            weighted_sum_formula_area[len("Avg.information"):].animate.align_to(weighted_sum_formula_h["="][0], LEFT),
                            ReplacementTransform(weighted_sum_formula_area["Avg. information"], weighted_sum_formula_h["H(P)"]), run_time=2),
                        FadeIn(entropy_text, run_time=2), lag_ratio=0.4)
                )
            if i == 19:
                entropy_display = Tex(
                    R"= 0.00 \text{ bits}", font_size=32
                ).next_to(
                    weighted_sum_formula_h[-2:], DOWN, buff=0.17
                )
                entropy_display_opacity_tracker = ValueTracker(0)
                entropy_display.add_updater(lambda m: m.set_opacity(entropy_display_opacity_tracker.get_value()))
                entropy_value = entropy_display.make_number_changeable("0.00")
                entropy_value.add_updater(
                    lambda m: m.set_value(
                        sum([t.get_value() * -math.log2(t.get_value()) for t in general_chart.distribution_trackers])
                    )
                )
                entropy_display.add_updater(lambda m: self.bring_to_front(m))
                self.add(entropy_display)
                anims.append(entropy_display_opacity_tracker.animate.set_value(1))

            self.play(*anims, run_time=3)
        self.remove(weighted_sum_formula_area)
        self.add(weighted_sum_formula_h)

        # Show a uniform distribution
        event_labels_opacity_tracker = ValueTracker(1)
        general_chart.segments.add_updater(lambda m: m.labels.set_opacity(event_labels_opacity_tracker.get_value()))
        self.play(
            general_chart.probability_labels.animate.set_opacity(0),
            event_labels_opacity_tracker.animate.set_value(0),
            general_chart.set_distribution([1 / 7 for _ in range(7)]), run_time=3)
        self.wait(2)

        # Show a squished distribution
        big_prob = 0.789
        leftover = 1 - big_prob
        leftover_distibution = random_distribution(6, thresh=(2**-7) / leftover)
        leftover_distibution = [p * leftover for p in leftover_distibution]
        distribution = [big_prob] + leftover_distibution
        self.play(general_chart.set_distribution(distribution), run_time=6)
        self.wait(4)

        # Indicate the most probable event with little information
        general_chart.save_state()
        entropy_display.save_state()
        bars_copy.save_state()
        weighted_sum_formula_h.save_state()
        entropy_text.save_state()
        general_chart.suspend_updating()
        entropy_display.suspend_updating()
        bars_copy.suspend_updating()
        weighted_sum_formula.suspend_updating()
        self.play(
            VGroup(
                general_chart.bars[1:],
                general_chart.segments.bars[1:],
                general_chart.reference_lines,
                general_chart.vertical_axis,
                general_chart.vertical_axis_label,
                entropy_display,
                bars_copy,
                weighted_sum_formula_h,
                entropy_text
            ).animate.fade(0.8), run_time=2)
        arrow = Arrow(ORIGIN, DOWN).set_color(TEAL).next_to(general_chart.bars[0], UP)
        label = TexText(
            R"high probability $\Longleftrightarrow$ low information",
            font_size=40
        ).set_color(TEAL).next_to(arrow, UP, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(label, run_time=1.2))
        self.wait(2)
        self.play(
            general_chart.animate.restore(),
            entropy_display.animate.restore(),
            bars_copy.animate.restore(),
            weighted_sum_formula_h.animate.restore(),
            entropy_text.animate.restore(),
            FadeOut(VGroup(arrow, label)), run_time=2)
        general_chart.resume_updating()
        entropy_display.resume_updating()
        bars_copy.resume_updating()
        weighted_sum_formula_area.resume_updating()
        self.wait(2)

        # Divide the probability space into more chunks
        entropy_value.clear_updaters()
        entropy_display.add_updater(lambda m: self.bring_to_front(m))
        prev_chart = general_chart
        for i in range(1, 3):
            new_distribution = []
            for p in distribution:
                new_distribution += [p / 2**i for _ in range(2**i)]
            new_chart = EntropyChart(
                new_distribution,
                event_labels=None,
                probability_labels=None,
                width=9,
                height=3,
                segments_height=0.4,
                fit_event_labels_to_height=False,
                fill_colors=[YELLOW_B, YELLOW_D]
            ).match_width(general_chart).match_x(general_chart).align_to(general_chart, UP)
            new_chart.bars.add_updater(lambda m: m.set_stroke(width=0.3 / 2**i))
            new_chart.segments.bars.set_stroke(width=0.5 / 2**i)
            general_chart.clear_updaters()
            bars_copy.clear_updaters()
            self.play(
                FadeOut(prev_chart, suspend_mobject_updating=True, run_time=3),
                FadeIn(new_chart, suspend_mobject_updating=True, run_time=3),
                bars_copy.animate(run_time=3).become(
                    new_chart.bars.copy()
                    .clear_updaters()
                    .set_opacity(1)
                    .stretch(0.5, 0)
                    .scale(scale_factor)
                    .next_to(weighted_sum_formula_area[-2], RIGHT)
                    .align_to(bars_copy, DOWN)
                ),
                entropy_value.animate(run_time=1.3).set_value(
                    sum([t.get_value() * -math.log2(t.get_value()) for t in new_chart.distribution_trackers])
                )
            )
            self.wait(2)
            prev_chart = new_chart

        def update_area_bars(m):
            m.become(
                new_chart.bars.copy()
                .clear_updaters()
                .set_opacity(1)
                .stretch(0.5, 0)
                .scale(scale_factor)
                .next_to(weighted_sum_formula_area[-2], RIGHT)
                .align_to(m, DOWN)
            )
        bars_copy.add_updater(update_area_bars)

        # Squish and then spread out the new distribution
        entropy_value.add_updater(
            lambda m: m.set_value(
                sum([t.get_value() * -math.log2(t.get_value()) for t in new_chart.distribution_trackers])
            )
        )
        big_prob_1 = 0.42
        big_prob_2 = 0.178
        big_prob_3 = 0.32
        leftover = 1 - big_prob_1 - big_prob_2 - big_prob_3
        leftover_distibution = random_distribution(25, thresh=(2**-10) / leftover)
        leftover_distibution = [p * leftover for p in leftover_distibution]
        distribution = [big_prob_1, big_prob_2, big_prob_3] + leftover_distibution
        self.play(new_chart.set_distribution(distribution), run_time=6)
        self.wait(1)

        uniform_distribution = [1 / 28 for _ in range(28)]
        self.play(new_chart.set_distribution(uniform_distribution), run_time=6)
        self.wait(1)

        # Show some more random distributions
        for _ in range(10):
            self.play(new_chart.set_distribution(random_distribution(28, thresh=2**-8)), run_time=3)


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
