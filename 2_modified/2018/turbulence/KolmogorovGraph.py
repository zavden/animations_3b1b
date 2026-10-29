# ==============================================================================
# Scene:      KolmogorovGraph
# Source:     videos/_2018/turbulence.py (lines 1423-1478)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl KolmogorovGraph.py KolmogorovGraph -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the piecewise function returned None at exactly x=0.5 / x=5 (GL samples exactly those values); the pieces are continuous there
# ==============================================================================

from manim_imports_ext import *

class KolmogorovGraph(Scene):
    def construct(self):
        axes = Axes(
            x_min=-1,
            y_min=-1,
            x_max=7,
            y_max=9,
            y_axis_config={
                "unit_size": 0.7,
            }
        )
        axes.center().shift(1.5 * RIGHT)
        x_label = OldTex("\\log(D)")
        x_label.next_to(axes.x_axis.get_right(), UP)
        y_label = OldTex("\\log(\\text{K.E. at length scale D})")
        y_label.scale(0.8)
        y_label.next_to(axes.y_axis.get_top(), LEFT)
        y_label.shift_onto_screen()
        axes.add(x_label, y_label)

        v_lines = VGroup(*[
            DashedLine(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, 9),
                color=YELLOW,
                stroke_width=1
            )
            for x in [0.5, 5]
        ])
        inertial_subrange = OldTexText("``Inertial subrange''")
        inertial_subrange.scale(0.7)
        inertial_subrange.next_to(v_lines.get_bottom(), UP)

        def func(x):
            # CHANGE: the piecewise function returned None at exactly x=0.5 / x=5 (GL samples exactly those values); the pieces are continuous there
            if 0.5 <= x <= 5:
                return (5 / 3) * x
            elif x < 0.5:
                return 5 * (x - 0.5) + 0.5 * (5 / 3)
            elif x > 5:
                return np.log(x) + (5 / 3) * 5 - np.log(5)

        graph = axes.get_graph(func, x_min=0.3, x_max=7)

        prop_label = OldTex("\\text{K.E.} \\propto D^{5/3}")
        prop_label.next_to(
            graph.point_from_proportion(0.5), UL,
            buff=0
        )

        self.add(axes)
        self.play(ShowCreation(graph))
        self.play(FadeInFromDown(prop_label))
        self.wait()
        self.add(v_lines)
        self.play(Write(inertial_subrange))
        self.wait()
