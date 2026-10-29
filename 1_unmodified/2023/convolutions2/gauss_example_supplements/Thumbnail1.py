# ==============================================================================
# Scene:      Thumbnail1
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1186-1219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail1.py Thumbnail1 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Thumbnail1(InteractiveScene):
    def construct(self):
        # Test
        line_style = dict(stroke_color=GREY_B, stroke_width=1)
        faded_line_style = dict(stroke_opacity=0.25, **line_style)
        plane = NumberPlane(
            (-3, 3), (0, 1, 0.5),
            height=1.5, width=4,
            background_line_style=line_style,
            faded_line_style=faded_line_style,
        )
        plane.set_width(FRAME_WIDTH)
        plane.to_edge(DOWN)

        graph = plane.get_graph(lambda x: np.exp(-x**2))
        graph.set_stroke(TEAL, 5)

        expr = Tex("e^{-x^2}", font_size=120)
        expr.next_to(plane.c2p(1.5, 1), DOWN)

        question = Text("Why this function?", font_size=90)
        question.to_edge(UP)

        arrow = Arrow(
            question["this"], expr["e"],
            stroke_width=10,
            stroke_color=YELLOW
        )

        self.add(plane)
        self.add(graph)
        self.add(question)
        self.add(arrow)
        self.add(expr)
