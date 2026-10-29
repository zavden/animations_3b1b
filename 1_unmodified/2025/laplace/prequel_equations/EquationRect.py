# ==============================================================================
# Scene:      EquationRect
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1093-1102)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EquationRect.py EquationRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EquationRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(5.25, 1)
        rect.set_stroke(YELLOW, 3)

        # Test
        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.stretch(0.5, 0).shift(4 * RIGHT).set_opacity(0))
        self.wait()
