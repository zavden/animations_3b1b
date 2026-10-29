# ==============================================================================
# Scene:      ThumbnailMaterial
# Source:     videos/_2023/convolutions2/supplements.py (lines 892-913)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/convolutions2/continuous.py
#
# Run from this folder:
#     manimgl ThumbnailMaterial.py ThumbnailMaterial -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/convolutions2/continuous.py -----

def wedge_func(x):
    return np.clip(-np.abs(x) + 1, 0, 1)



# ----- From _2023/convolutions2/supplements.py -----

class ThumbnailMaterial(InteractiveScene):
    def construct(self):
        # Graphs
        axes = Axes((-2, 2), (0, 1, 0.25), width=7, height=3)

        exp_graph = axes.get_graph(lambda x: np.exp(-2 - x))
        exp_graph.set_stroke(BLUE, 5)
        exp_label = Tex("p_X(x)", font_size=72)
        exp_label.next_to(exp_graph.pfp(0.2), UR, SMALL_BUFF)

        wedge_graph = axes.get_graph(wedge_func, use_smoothing=False)
        wedge_graph.set_stroke(YELLOW, 5)
        wedge_label = Tex("p_Y(y)", font_size=72)
        wedge_label.next_to(wedge_graph.pfp(0.4), UL, SMALL_BUFF)

        # conv_label = Tex("[f * g](-1.5)", font_size=72)
        # self.add(conv_label)
        # return

        self.add(axes)
        self.add(exp_graph)
        self.add(exp_label)
