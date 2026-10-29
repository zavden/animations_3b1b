# ==============================================================================
# Scene:      UnevenDistribution
# Source:     videos/_2026/cross_entropy/supplements.py (lines 538-564)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py, _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl UnevenDistribution.py UnevenDistribution -w -m --fps 15
#
# Notes:
#   arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


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



# ----- From _2026/cross_entropy/entropy.py -----

class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, width=0.5, *args, **kwargs):
        super().__init__("arrow.svg", *args, **kwargs)
        self.set_width(width)
        self.rotate(angle_of_vector(direction))
        self.direction = direction


class ArrowGroup(VGroup):
    def __init__(self):
        super().__init__(InstructionArrow(v) for v in [UP, DOWN, LEFT, RIGHT])



# ----- From _2026/cross_entropy/supplements.py -----

class UnevenDistribution(InteractiveScene):
    def construct(self):
        # Test
        dists = [
            [0.25] * 4,
            [0.5, 0.25, 0.125, 0.125]
        ]
        full_width = 6
        stacks = VGroup(
            StackedProbDistribution(dist, width=full_width, height=0.5, labels=ArrowGroup())
            for dist in dists
        )
        decs = VGroup(
            self.get_bar_dec(bar, full_width)
            for bar in stacks[0].bars
        )

        self.add(stacks[0], decs)
        self.wait()
        self.play(Transform(*stacks), run_time=2)
        self.wait()

    def get_bar_dec(self, bar, full_width):
        dec = DecimalNumber(0, font_size=24, num_decimal_places=3)
        dec.add_updater(lambda m: m.set_value(bar.get_width() / full_width))
        dec.add_updater(lambda m: m.next_to(bar, DOWN, SMALL_BUFF))
        return dec
