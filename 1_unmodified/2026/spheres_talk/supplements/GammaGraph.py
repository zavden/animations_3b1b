# ==============================================================================
# Scene:      GammaGraph
# Source:     videos/_2026/spheres_talk/supplements.py (lines 563-573)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GammaGraph.py GammaGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GammaGraph(InteractiveScene):
    def construct(self):
        # Test
        axes = Axes((-1, 5), (0, 20), width=FRAME_WIDTH - 1, height=FRAME_HEIGHT - 1.5)
        axes.x_axis.add_numbers()
        self.add(axes)

        import scipy
        graph = axes.get_graph(lambda x: scipy.special.gamma(x + 1), x_range=(-0.99, 5, 0.01))
        graph.set_stroke(TEAL, 5)
        self.add(graph)
