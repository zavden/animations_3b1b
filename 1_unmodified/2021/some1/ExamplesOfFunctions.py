# ==============================================================================
# Scene:      ExamplesOfFunctions
# Source:     videos/_2021/some1.py (lines 684-721)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplesOfFunctions.py ExamplesOfFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExamplesOfFunctions(Scene):
    def construct(self):
        plane = NumberPlane((-15, 15, 5), (-10, 10, 5))
        plane.scale(0.5)
        self.add(plane)

        graphs = VGroup(
            plane.get_graph(lambda x: -x * (x - 4)),
            plane.get_graph(lambda x: x / 3),
            plane.get_graph(lambda x: (1 / 3) * x**3 - 2 * x + 1),
            plane.get_graph(lambda x: -5 * x * np.exp(-x**2 / 2)),
        )
        graph_labels = VGroup(
            OldTex("f(x) = ", "-x^2 - 4x"),
            OldTex("f(x) = ", "x / 3"),
            OldTex("f(x) = ", "x^3 / 3- 2x + 1"),
            OldTex("f(x) = ", "-(5x) e^{-{1 \\over 2} x^2}"),
        )
        colors = [YELLOW, RED, TEAL, PINK]
        for graph, color, label in zip(graphs, colors, graph_labels):
            graph.set_stroke(color)
            label.scale(1.5)
            label[1].set_color(color)
            label.next_to(plane.c2p(0, 5), UR, SMALL_BUFF)
            label.set_stroke(BLACK, 3, background=True)

        self.play(
            FadeIn(graph_labels[0]), ShowCreation(graphs[0]),
            run_time=1.5
        )
        self.wait()
        for i in range(1, len(graphs)):
            self.play(
                ReplacementTransform(graphs[i - 1], graphs[i]),
                FadeTransform(graph_labels[i - 1], graph_labels[i]),
                run_time=0.5
            )
            self.wait(1.5)
