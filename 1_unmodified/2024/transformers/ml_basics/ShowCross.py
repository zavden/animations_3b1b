# ==============================================================================
# Scene:      ShowCross
# Source:     videos/_2024/transformers/ml_basics.py (lines 298-304)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowCross.py ShowCross -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ShowCross(InteractiveScene):
    def construct(self):
        # Test
        cross = Cross(Square(side_length=5))
        cross.set_stroke(width=[0, 30, 0])
        self.play(ShowCreation(cross))
        self.wait()
