# ==============================================================================
# Scene:      XYtoYX
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 447-451)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XYtoYX.py XYtoYX -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class XYtoYX(InteractiveScene):
    def construct(self):
        tex = Tex(R"(x, y) \leftrightarrow (y, x)")
        tex.to_edge(UP)
        self.add(tex)
