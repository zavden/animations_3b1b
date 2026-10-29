# ==============================================================================
# Scene:      EGraph
# Source:     videos/outside_videos/misc_thumbnails.py (lines 272-295)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EGraph.py EGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EGraph(InteractiveScene):
    def construct(self):
        # Test
        axes = Axes((-4, 4), (0, 20, 2), width=14, height=5.5)
        axes.center().to_edge(DOWN)
        axes.set_stroke(width=3)
        graph = axes.get_graph(np.exp)
        graph.set_stroke(YELLOW, 10)
        self.add(axes, graph)

        equation = Tex("e = 2.71828...", t2c={"e": BLUE})
        equation["e"].match_height(equation, about_edge=DR)
        equation.set_width(10)
        equation.to_edge(UP)
        self.add(equation)

        qmarks = Text("??", font_size=200)
        qmarks.move_to(DOWN).to_edge(LEFT, buff=1.0)
        arrow = Arrow(
            qmarks.get_corner(UR), equation["2."].get_corner(DL),
            stroke_width=10, stroke_color=WHITE
        )
        VGroup(qmarks, arrow).set_color(TEAL)
        self.add(qmarks, arrow)
