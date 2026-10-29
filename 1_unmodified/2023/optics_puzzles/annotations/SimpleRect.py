# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 408-417)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    def construct(self):
        rad = Text("rad")
        rect = SurroundingRectangle(rad)
        rect.set_stroke(YELLOW, 3)
        arrow = Vector(UP)
        arrow.set_stroke(YELLOW)
        arrow.next_to(rect, DOWN)
        self.play(ShowCreation(arrow), ShowCreation(rect))
        self.wait()
