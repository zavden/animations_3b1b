# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2025/laplace/main_supplements.py (lines 643-649)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(4.5, 2)
        rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(rect))
        self.wait()
