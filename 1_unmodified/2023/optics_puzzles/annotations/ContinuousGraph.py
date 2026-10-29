# ==============================================================================
# Scene:      ContinuousGraph
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 803-810)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContinuousGraph.py ContinuousGraph -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ContinuousGraph(InteractiveScene):
    def construct(self):
        axes = Axes((0, 5), (0, 5), width=4, height=4)
        graph = axes.get_graph(lambda x: (x**2) / 5)
        graph.set_stroke(YELLOW, 3)
        self.add(axes)
        self.play(ShowCreation(graph))
        self.wait()
