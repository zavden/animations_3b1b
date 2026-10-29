# ==============================================================================
# Scene:      RobotNewOptimalCode
# Source:     videos/_2026/cross_entropy/robot.py (lines 8392-8417)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl RobotNewOptimalCode.py RobotNewOptimalCode -w -m --fps 15
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


class RobotNewOptimalCode(InteractiveScene):
    def construct(self):
        # Add the chart
        encoding = ["111", "110", "10", "0"]
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
            width=12 * 1.12,
            height=4.5 * 1.12,
            include_vertical_axis=False,
            segments_height=1,
            fill_colors=[GREEN_B, GREEN_D]
        ).scale(0.3)
        second_distribution_chart.update()
        second_distribution_chart.clear_updaters()
        second_distribution_chart.bar_labels.set_color(WHITE)
        self.play(second_distribution_chart.create())
