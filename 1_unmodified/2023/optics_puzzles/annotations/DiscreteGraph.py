# ==============================================================================
# Scene:      DiscreteGraph
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 813-825)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiscreteGraph.py DiscreteGraph -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DiscreteGraph(InteractiveScene):
    def construct(self):
        # Test
        axes = Axes((0, 5), (0, 5), width=4, height=4)
        graph = axes.get_graph(
            lambda x: np.floor(x) + 0.5,
            discontinuities=np.arange(0, 8),
            x_range=(0, 4.99),
        )
        graph.set_stroke(RED, 5)
        self.add(axes)
        self.play(ShowCreation(graph))
        self.wait()
