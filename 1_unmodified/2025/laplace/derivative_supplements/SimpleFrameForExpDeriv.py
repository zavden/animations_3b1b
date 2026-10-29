# ==============================================================================
# Scene:      SimpleFrameForExpDeriv
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 286-292)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleFrameForExpDeriv.py SimpleFrameForExpDeriv -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleFrameForExpDeriv(InteractiveScene):
    def construct(self):
        rect = Rectangle(6, 4)
        rect.set_stroke(BLUE, 3)

        self.play(ShowCreation(rect))
        self.wait()
