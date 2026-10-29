# ==============================================================================
# Scene:      VariableCWithF
# Source:     videos/_2023/gauss_int/herschel.py (lines 1157-1173)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VariableCWithF.py VariableCWithF -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VariableC(InteractiveScene):
    c_values = [1.0, 0.5, -1.0, -0.7, -0.5, 0.25, -0.2, -0.4, -0.9, -0.1, 0.5, 0.3, 0.1]

    def construct(self):
        axes = self.get_axes()
        self.add(axes)

        curve = axes.get_graph(lambda x: self.func(x, 1))
        curve.set_stroke(RED, 3)
        self.add(curve)

        label = self.get_label(axes)
        self.add(label)

        c_tracker, c_interval, c_tip, c_label = self.get_c_group()
        get_c = c_tracker.get_value

        c_interval.move_to(axes, UR)
        c_interval.shift(0.5 * DOWN)
        self.add(c_interval, c_tip, c_label)

        axes.bind_graph_to_func(curve, lambda x: self.func(x, get_c()))

        # Animate
        for c in self.c_values:
            self.play(c_tracker.animate.set_value(c), run_time=2)
            self.wait()

    def get_c_group(self):
        c_tracker = ValueTracker(1)
        get_c = c_tracker.get_value

        c_interval = NumberLine(
            (-1, 1, 0.25), width=3, tick_size=0.05, big_tick_numbers=[-1, 0, 1],
        )
        c_interval.set_stroke(WHITE, 1)
        c_interval.add_numbers([-1, 0, 1], num_decimal_places=1, font_size=16)
        c_tip = ArrowTip(angle=-90 * DEGREES)
        c_tip.scale(0.5)
        c_tip.set_fill(RED)
        c_tip.add_updater(lambda m: m.move_to(c_interval.n2p(get_c()), DOWN))

        c_label = Tex("c = 1.00", t2c={"c": RED}, font_size=36)
        c_label.make_number_changeable("1.00")
        c_label[-1].scale(0.8, about_edge=LEFT)
        c_label.add_updater(lambda m: m[-1].set_value(get_c()))
        c_label.add_updater(lambda m: m.next_to(c_tip, UP, aligned_edge=LEFT))

        return [c_tracker, c_interval, c_tip, c_label]

    def get_axes(self):
        axes = Axes(
            (-1, 5), (0, 4),
            width=6, height=4,
        )
        return axes

    def func(self, x, c):
        return np.exp(c * x)

    def get_label(self, axes):
        label = Tex("e^{cx}", t2c={"c": RED})
        label.next_to(axes.c2p(0, 2.7), RIGHT)
        return label


class VariableCWithF(VariableC):
    def get_axes(self):
        axes = Axes(
            (-4, 4), (0, 2),
            width=8, height=3,
        )
        axes.add(VectorizedPoint(axes.c2p(0, 3)))
        axes.center()
        return axes

    def func(self, x, c):
        return np.exp(c * x * x)

    def get_label(self, axes):
        label = Tex("e^{cx^2}", t2c={"c": RED})
        label.next_to(axes.c2p(0, 2), LEFT)
        return label
