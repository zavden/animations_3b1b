# ==============================================================================
# Scene:      XXOnEdge
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 454-458)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XXOnEdge.py XXOnEdge -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class XXOnEdge(InteractiveScene):
    def construct(self):
        tex = TexText(R"``Pairs'' of the form $(X, X)$\\live on the edge")
        tex.to_corner(UL)
        self.add(tex)
