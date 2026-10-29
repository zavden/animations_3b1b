# ==============================================================================
# Scene:      RepeatedDiscreteConvolutions
# Source:     videos/_2023/convolutions2/dice.py (lines 1365-1537)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl RepeatedDiscreteConvolutions.py RepeatedDiscreteConvolutions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2023/clt/main.py -----

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.typing import ManimColor


EXP_DISTRIBUTION = [0.41, 0.25, 0.15, 0.10, 0.06, 0.03]


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



# ----- From _2023/convolutions2/dice.py -----

class RepeatedDiscreteConvolutions(InteractiveScene):
    distribution = EXP_DISTRIBUTION

    def construct(self):
        # Divide up space
        h_lines = Line(LEFT, RIGHT).set_width(FRAME_WIDTH).replicate(4)
        h_lines.arrange(DOWN, buff=FRAME_HEIGHT / 3).center()
        h_lines.set_stroke(WHITE, 1)
        self.add(h_lines[1:3])

        # Initial distributions
        dist = self.distribution
        top_bars = self.get_bar_group(dist, colors=(BLUE, TEAL))
        top_bars.next_to(h_lines[1], UP, SMALL_BUFF)

        low_bars = top_bars.copy()
        low_bars.set_y(-top_bars.get_y())
        low_bars.next_to(h_lines[2], UP, SMALL_BUFF)

        VGroup(top_bars, low_bars).shift(2 * LEFT)

        self.add(top_bars)
        self.add(low_bars)

        # Add labels

        # Repeated convolution
        self.flip_bar_group(low_bars)
        low_bars.save_state()
        for n in range(5):
            new_bars = self.show_convolution(top_bars, low_bars)
            self.wait()
            self.play(
                new_bars.animate.move_to(top_bars, DL).set_anim_args(path_arc=-120 * DEGREES),
                FadeOut(top_bars, UP),
                Restore(low_bars),
            )
            # TODO, things with labels

            top_bars = new_bars

    def get_bar_group(
        self, 
        dist, 
        colors=(BLUE, TEAL), 
        y_unit=4,
        bar_width=0.35,
        num_decimal_places=2,
        min_value=1,
    ):
        bars = self.get_bars(dist, colors, y_unit, bar_width)
        result = VGroup(
            bars,
            self.get_bar_value_labels(bars, min_value),
            self.get_bar_prob_labels(bars, dist, num_decimal_places),
        )
        result.dist = dist
        return result

    def get_bars(self, dist, colors=(BLUE, TEAL), y_unit=4, bar_width=0.35):
        axes = Axes(
            (0, len(dist)), (0, 1),
            height=y_unit,
            width=bar_width * len(dist)
        )
        bars = ChartBars(axes, dist, fill_opacity=0.75)
        bars.set_submobject_colors_by_gradient(*colors)
        return bars

    def get_bar_value_labels(self, bars, min_value=1):
        values = VGroup(*(
            Integer(x + min_value, font_size=16)
            for x in range(len(bars))
        ))
        for bar, value in zip(bars, values):
            value.next_to(bar, DOWN, SMALL_BUFF)

        return values

    def get_bar_prob_labels(self, bars, dist, num_decimal_places=2):
        probs = VGroup(*(
            DecimalNumber(p, font_size=16, num_decimal_places=num_decimal_places)
            for p in dist
        ))
        for bar, prob in zip(bars, probs):
            prob.set_max_width(0.75 * bar.get_width())
            prob.next_to(bar, UP, SMALL_BUFF)

        return probs

    def get_dist_label(self, indices):
        index_strs = [f"X_{{{i}}}" for i in indices]
        if len(indices) > 3:
            index_strs = [index_strs[0], R"\cdots", index_strs[-1]]
        sub_tex = "+".join(index_strs)
        return Tex(f"P_{{{sub_tex}}}")

    def flip_bar_group(self, bar_group):
        bars = bar_group[0]
        bars.target = bars.generate_target()
        bars.target.arrange(LEFT, buff=0, aligned_edge=DOWN)
        bars.target.align_to(bars[0], DR)
        self.play(
            MoveToTarget(bars, lag_ratio=0.05, path_arc=0.5),
            *(
                MaintainPositionRelativeTo(
                    VGroup(value, prob), bar
                )
                for bar, value, prob in zip(*bar_group)
            ),
        )
        self.add(bar_group)

    def show_convolution(self, top_bars, low_bars):
        # New bars
        new_dist = np.convolve(top_bars.dist, low_bars.dist)
        new_bars = self.get_bar_group(
            new_dist,
            y_unit=8,
            num_decimal_places=3,
            min_value=top_bars[1][0].get_value() + low_bars[1][0].get_value(),
        )
        new_bars.next_to(BOTTOM, UP)
        new_bars.align_to(top_bars, LEFT)

        # March!
        for n in range(len(new_bars[0])):
            x_diff = top_bars[0][0].get_x() - low_bars[0][0].get_x()
            x_diff += low_bars[0][0].get_width() * n
            self.play(
                low_bars.animate.shift(x_diff * RIGHT),
                run_time=0.5
            )
            index_pairs = [
                (k, n - k) for k in range(n + 1)
                if 0 <= n - k < len(low_bars[0])
                if 0 <= k < len(top_bars[0])
            ]
            highlights = VGroup(*(
                VGroup(top_bars[0][i].copy(), low_bars[0][j].copy())
                for i, j in index_pairs
            ))
            highlights.set_color(YELLOW)

            conv_rect, value_label, prob_label = (group[n] for group in new_bars)
            partial_rects = VGroup()
            partial_labels = VGroup()

            products = [top_bars.dist[i] * low_bars.dist[j] for i, j in index_pairs]
            for partial_value in np.cumsum(products):
                rect = conv_rect.copy()
                rect.stretch(
                    partial_value / new_bars.dist[n],
                    dim=1,
                    about_edge=DOWN,
                )
                label = prob_label.copy()
                label.set_value(partial_value)
                label.next_to(rect, UP, SMALL_BUFF)
                partial_rects.add(rect)
                partial_labels.add(label)

            self.add(value_label)
            self.play(
                ShowSubmobjectsOneByOne(highlights, remover=True),
                ShowSubmobjectsOneByOne(partial_rects, remover=True),
                ShowSubmobjectsOneByOne(partial_labels, remover=True),
                run_time=0.15 * len(products)
            )
            self.add(*(group[:n + 1] for group in new_bars))
            self.wait(0.5)

        return new_bars
