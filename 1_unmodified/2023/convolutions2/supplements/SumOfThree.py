# ==============================================================================
# Scene:      SumOfThree
# Source:     videos/_2023/convolutions2/supplements.py (lines 479-481)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SumOfThree.py SumOfThree -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SumOfThree(InteractiveScene):
    def construct(self):
        self.add(Tex("X_1 + X_2 + X_3"))
