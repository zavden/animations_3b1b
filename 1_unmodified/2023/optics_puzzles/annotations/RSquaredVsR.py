# ==============================================================================
# Scene:      RSquaredVsR
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 381-405)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RSquaredVsR.py RSquaredVsR -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RSquaredVsR(InteractiveScene):
    def construct(self):
        # Axes
        axes = Axes((0, 10), (0, 1, 0.25), height=5, width=12)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(num_decimal_places=2)
        self.add(axes)

        # Add graphs
        graph1 = axes.get_graph(lambda x: 1 / x**2, x_range=(0.1, 10)).set_stroke(YELLOW, 5)
        graph2 = axes.get_graph(lambda x: 1 / x, x_range=(0.1, 10)).set_stroke(BLUE, 5)
        graphs = VGroup(graph1, graph2)
        labels = VGroup(
            Tex(R"f(r) = \frac{1}{r^2}").set_color(YELLOW),
            Tex(R"f(r) = \frac{1}{r}").set_color(BLUE),
        )
        labels.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        labels.move_to(axes, UR)

        for graph, label in zip(graphs, labels):
            self.play(
                ShowCreation(graph, run_time=3),
                FadeIn(label, 0.5 * UP),
            )
        self.wait(3)
