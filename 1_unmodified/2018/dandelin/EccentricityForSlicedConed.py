# ==============================================================================
# Scene:      EccentricityForSlicedConed
# Source:     videos/_2018/dandelin.py (lines 717-727)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EccentricityForSlicedConed.py EccentricityForSlicedConed -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EccentricityForSlicedConed(Scene):
    def construct(self):
        equation = OldTex(
            "\\text{Eccentricity} = ",
            "{\\sin(", "\\text{angle of plane}", ")", "\\over",
            "\\sin(", "\\text{angle of cone slant}", ")}"
        )
        equation.set_color_by_tex("plane", YELLOW)
        equation.set_color_by_tex("cone", BLUE)
        equation.to_edge(LEFT)
        self.play(FadeInFromDown(equation))
