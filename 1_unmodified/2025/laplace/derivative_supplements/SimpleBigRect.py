# ==============================================================================
# Scene:      SimpleBigRect
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 640-645)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleBigRect.py SimpleBigRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleBigRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(4, 5)
        rect.set_stroke(YELLOW, 3)
        self.play(ShowCreation(rect))
        self.wait()
