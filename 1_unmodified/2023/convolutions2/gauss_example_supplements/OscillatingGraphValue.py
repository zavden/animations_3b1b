# ==============================================================================
# Scene:      OscillatingGraphValue
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 692-725)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OscillatingGraphValue.py OscillatingGraphValue -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OscillatingGraphValue(InteractiveScene):
    def construct(self):
        # Add graph
        axes = Axes((-3, 3), (0, 2), width=8, height=1.5)
        axes.move_to(1.5 * UP)
        graph = axes.get_graph(lambda x: np.exp(-x**2 / 2) * math.sqrt(PI))
        graph.set_stroke(TEAL, 2)
        axes.add(Tex("s").set_color(RED).next_to(axes.x_axis.get_end(), UR, SMALL_BUFF))

        self.add(axes, graph)

        # Add s tracker
        s_tracker = ValueTracker(-3)
        get_s = s_tracker.get_value
        v_line = always_redraw(lambda: axes.get_v_line_to_graph(get_s(), graph, line_func=Line).set_stroke(WHITE, 1))
        dot = GlowDot(radius=0.2, color=WHITE)
        dot.add_updater(lambda m: m.move_to(axes.i2gp(get_s(), graph)))
        tri = Triangle(start_angle=PI / 2)
        tri.set_height(0.05)
        tri.set_fill(TEAL, 1)
        tri.set_stroke(width=0)
        tri.add_updater(lambda m: m.move_to(axes.c2p(get_s(), 0), UP))
        label = DecimalNumber(0, font_size=24)
        label.add_updater(lambda m: m.set_value(get_s()))
        label.add_updater(lambda m: m.next_to(tri, DOWN, SMALL_BUFF))

        self.add(v_line, dot, label, tri)

        for _ in range(2):
            self.play(
                s_tracker.animate.set_value(3),
                rate_func=there_and_back,
                run_time=24
            )
