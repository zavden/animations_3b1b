# ==============================================================================
# Scene:      CosGraphs
# Source:     videos/_2020/ldm.py (lines 107-153)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CosGraphs.py CosGraphs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CosGraphs(Scene):
    def construct(self):
        axes = Axes(
            x_min=-0.75 * TAU,
            x_max=0.75 * TAU,
            y_min=-1.5,
            y_max=1.5,
            x_axis_config={
                "tick_frequency": PI / 4,
                "include_tip": False,
            },
            y_axis_config={
                "tick_frequency": 0.5,
                "include_tip": False,
                "unit_size": 1.5,
            }
        )

        graph1 = axes.get_graph(np.cos)
        graph2 = axes.get_graph(lambda x: np.cos(x)**2)

        graph1.set_stroke(YELLOW, 5)
        graph2.set_stroke(BLUE, 5)

        label1 = OldTex("\\cos(x)")
        label2 = OldTex("\\cos^2(x)")

        label1.match_color(graph1)
        label1.set_height(0.75)
        label1.next_to(axes.input_to_graph_point(-PI, graph1), DOWN)

        label2.match_color(graph2)
        label2.set_height(0.75)
        label2.next_to(axes.input_to_graph_point(PI, graph2), UP)

        for mob in [graph1, graph2, label1, label2]:
            mc = mob.copy()
            mc.set_stroke(BLACK, 10, background=True)
            self.add(mc)

        self.add(axes)
        self.add(graph1)
        self.add(graph2)
        self.add(label1)
        self.add(label2)

        self.embed()
