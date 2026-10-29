# ==============================================================================
# Scene:      AddTwoMatrixSizes
# Source:     videos/_2024/transformers/supplements.py (lines 1809-1822)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddTwoMatrixSizes.py AddTwoMatrixSizes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AddTwoMatrixSizes(InteractiveScene):
    def construct(self):
        # Test
        rect = Rectangle(3.0, 1.0)
        rect.set_stroke(BLUE, 3)
        total = Integer(2 * 4 * (12288**2))
        total.set_color(BLUE)
        total.next_to(rect, UP)

        self.play(
            ShowCreation(rect),
            Write(total)
        )
        self.wait()
