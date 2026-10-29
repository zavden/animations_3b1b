# ==============================================================================
# Scene:      SimpleBellRHS
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 379-381)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleBellRHS.py SimpleBellRHS -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleBellRHS(InteractiveScene):
    def construct(self):
        self.add(Tex("= e^{-x^2}"))
