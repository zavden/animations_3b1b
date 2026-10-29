# ==============================================================================
# Scene:      PrimeDensityHistogram
# Source:     videos/_2024/antp/main.py (lines 322-367)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl PrimeDensityHistogram.py PrimeDensityHistogram -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy
from typing import TYPE_CHECKING


# ----- From _2023/clt/main.py -----

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.typing import ManimColor


class ChartBars(VGroup):
    def __init__(
        self,
        axes,
        values: Sequence[float | int],
        xs: Sequence[float] | None = None,
        width_ratio: float = 1.0,
        offset: float = 0.5,
        fill_color: ManimColor = BLUE,
        fill_opacity: float = 0.5,
        stroke_color: ManimColor = WHITE,
        stroke_width: float = 1.0
    ):
        xs = xs if xs is not None else np.arange(*axes.x_range)

        self.x_to_index = dict(zip(xs, it.count()))
        x_step = xs[1] - xs[0]
        x_unit = axes.x_axis.get_unit_size()
        y_unit = axes.y_axis.get_unit_size()

        width = width_ratio * x_unit * x_step

        # Create a list of rectangles arranged side by side,
        # one for each x value
        rects = []
        epsilon = 1e-8
        for x, y in zip(xs, values):
            rect = Rectangle(
                width=width,
                height=max(y * y_unit, epsilon),
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            rect.move_to(axes.c2p(x + offset * x_step, 0), DOWN)
            rects.append(rect)
        super().__init__(*rects)
        self.axes = axes
        self.xs = xs
        self.set_values(values)

    def set_values(self, values: Iterable[float | int]):
        y_unit = self.axes.y_axis.get_unit_size()
        for rect, value in zip(self, values):
            rect.set_height(
                y_unit * value,
                stretch=True,
                about_edge=DOWN,
            )



# ----- From _2024/antp/main.py -----

class PrimeDensityHistogram(InteractiveScene):
    def construct(self):
        # Axes
        max_x = 10000
        step = 100
        labeled_xs = list(range(1000, max_x + 1000, 1000))
        axes = Axes(
            (0, max_x, step),
            (0, 0.5, 0.1),
            width=FRAME_WIDTH - 2,
            height=6,
            x_axis_config=dict(
                tick_size=0.03,
                big_tick_numbers=labeled_xs,
                longer_tick_multiple=3,
            )
        )
        axes.x_axis.add_numbers(
            labeled_xs,
            font_size=16,
            buff=0.25,
        )
        axes.y_axis.add_numbers(
            np.arange(0, 0.6, 0.1),
            num_decimal_places=2,
        )

        y_label = Text("""
            Proportion of primes
            in ranges of length 1,000
        """, font_size=36)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.5)
        y_label.to_edge(UP)
        axes.add(y_label)

        self.add(axes)

        # Bars
        proportions = []
        for n in range(0, max_x, step):
            n_primes = len(list(sympy.primerange(n, n + step)))
            proportions.append(n_primes / step)

        bars = ChartBars(axes, proportions)

        self.add(bars)
