# ==============================================================================
# Scene:      OldTalkAboutSignOfConstantScraps
# Source:     videos/_2023/gauss_int/herschel.py (lines 1235-1250)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OldTalkAboutSignOfConstantScraps.py OldTalkAboutSignOfConstantScraps -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The original is leftover code without context (it uses plane, graph and get_c without defining them): the minimal setup of VariableCWithF was added (axes, e^{cx^2} curve, c control), the area was added to the scene and an animation of c so the result is visible
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OldTalkAboutSignOfConstantScraps(InteractiveScene):
    def construct(self):
        # CHANGE: the original is leftover code without context (it uses plane, graph, get_c and self.func without defining them).
        # CHANGE: the minimal setup of VariableCWithF (axes, e^{cx^2} curve and c control) is added so that it runs
        plane = self.get_axes()
        self.add(plane)

        graph = plane.get_graph(lambda x: self.func(x, 1))
        graph.set_stroke(RED, 3)
        self.add(graph)

        c_tracker, c_interval, c_tip, c_label = self.get_c_group()
        get_c = c_tracker.get_value
        c_interval.move_to(plane, UR)
        c_interval.shift(0.5 * DOWN)
        self.add(c_interval, c_tip, c_label)

        plane.bind_graph_to_func(graph, lambda x: self.func(x, get_c()))
        # Area
        area = VMobject()
        area.set_fill(RED, 0.5)
        area.set_stroke(width=0)

        def update_area(area):
            area.set_points_as_corners([
                plane.c2p(-4, 0),
                *graph.get_anchors(),
                plane.c2p(4, 0)
            ])

        area.add_updater(update_area)

        # CHANGE: the original never adds the area or animates c; they are added to show the result
        self.add(area)
        for c in [1.0, 0.5, -1.0, -0.7, -0.3, 0.25, -0.9]:
            self.play(c_tracker.animate.set_value(c), run_time=2)
            self.wait()

    # CHANGE: methods copied from VariableC and VariableCWithF (sibling classes in the same file)
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
            (-4, 4), (0, 2),
            width=8, height=3,
        )
        axes.add(VectorizedPoint(axes.c2p(0, 3)))
        axes.center()
        return axes

    def func(self, x, c):
        return np.exp(c * x * x)
