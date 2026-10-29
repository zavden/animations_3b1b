# ==============================================================================
# Scene:      HighlightRect
# Source:     videos/_2024/transformers/supplements.py (lines 1681-1687)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighlightRect.py HighlightRect -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HighlightRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(1, 3)
        rect.scale(0.5)
        rect.set_stroke(MAROON_B, 3)
        self.play(ShowCreation(rect))
        self.wait()
