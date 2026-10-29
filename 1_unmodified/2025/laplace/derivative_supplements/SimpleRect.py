# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 342-349)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(1.5, 1)
        rect.set_stroke(YELLOW, 3)
        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.stretch(0.5, 1, about_edge=DOWN))
        self.wait()
