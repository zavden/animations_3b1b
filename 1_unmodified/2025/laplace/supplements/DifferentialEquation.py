# ==============================================================================
# Scene:      DifferentialEquation
# Source:     videos/_2025/laplace/supplements.py (lines 1487-1503)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DifferentialEquation.py DifferentialEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DifferentialEquation(InteractiveScene):
    def construct(self):
        # ode to x
        x_term = Tex(R"x(t)", font_size=90)
        arrow = Vector(DOWN, thickness=5)
        arrow.move_to(ORIGIN, DOWN)
        words = Text("Differential Equation", font_size=72)
        words.next_to(arrow, UP)

        self.play(Write(x_term))
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(words),
            x_term.animate.next_to(arrow, DOWN),
        )
        self.wait()
