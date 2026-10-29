# ==============================================================================
# Scene:      Distributions
# Source:     videos/_2026/spheres_talk/random_puzzles.py (lines 647-668)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Distributions.py Distributions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Distributions(InteractiveScene):
    def construct(self):
        # Test
        axes = Axes(
            (-1, 1, 0.2),
            (0, 1),
            width=6,
            height=4
        )
        axes.add_coordinate_labels(num_decimal_places=1, font_size=16)
        axes.y_axis.set_opacity(0)

        # graph = axes.get_graph(lambda x: np.exp(-5 * x**2))
        # graph = axes.get_graph(lambda x: np.sqrt(1 - x**2))
        # graph = axes.get_graph(lambda x: 0.3 * x**2 + 0.5)
        graph = axes.get_graph(lambda x: 0.5)

        rects = axes.get_riemann_rectangles(graph, dx=0.1)
        rects.set_fill(opacity=0.5)
        rects.set_stroke(WHITE, 1, 0.5)

        self.add(axes, rects)
