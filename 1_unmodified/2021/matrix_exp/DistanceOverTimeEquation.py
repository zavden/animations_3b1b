# ==============================================================================
# Scene:      DistanceOverTimeEquation
# Source:     videos/_2021/matrix_exp.py (lines 4732-4741)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DistanceOverTimeEquation.py DistanceOverTimeEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DistanceOverTimeEquation(Scene):
    def construct(self):
        equation = OldTex(
            "{\\text{Distance}", " \\over", " \\text{Time} }", "=", "\\text{Radius}",
        )
        # equation[:3].set_color(RED_B)
        equation.add(SurroundingRectangle(equation[:3], color=RED, stroke_width=1))
        equation[4].set_color(BLUE)
        self.play(FadeIn(equation, UP))
        self.wait()
