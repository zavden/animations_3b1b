# ==============================================================================
# Scene:      XXLabel
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 350-355)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XXLabel.py XXLabel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class XXLabel(InteractiveScene):
    def construct(self):
        tex = TexText(R"``Pairs'' of the form (X, X)", font_size=60)
        tex["X"].set_color(YELLOW)
        tex.to_edge(UP)
        self.play(Write(tex))
