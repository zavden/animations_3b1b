# ==============================================================================
# Scene:      DownByTheRiverHeader
# Source:     videos/_2024/transformers/chm.py (lines 445-452)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DownByTheRiverHeader.py DownByTheRiverHeader -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DownByTheRiverHeader(InteractiveScene):
    def construct(self):
        words = Text("Down by the river bank ...")
        rect = SurroundingRectangle(words["bank"])
        rect.set_fill(BLUE, 0.5)
        rect.set_stroke(BLUE, 3)
        brace = Brace(rect, DOWN, buff=SMALL_BUFF)
        self.add(rect, words, brace)
