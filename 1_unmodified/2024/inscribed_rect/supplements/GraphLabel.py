# ==============================================================================
# Scene:      GraphLabel
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 307-316)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraphLabel.py GraphLabel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GraphLabel(InteractiveScene):
    def construct(self):
        group = VGroup(
            Text("Graph of"),
            Tex(R"f(x, y) = e^{-x^2 - y^2}"),
        )
        group.arrange(DOWN)
        group.to_edge(UP)
        self.play(Write(group))
        self.wait()
