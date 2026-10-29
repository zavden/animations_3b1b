# ==============================================================================
# Scene:      SimpleBellRHS2
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 384-386)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleBellRHS2.py SimpleBellRHS2 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleBellRHS2(InteractiveScene):
    def construct(self):
        self.add(Tex("= e^{-(s - x)^2}"))
