# ==============================================================================
# Scene:      ZEqualsVDotK
# Source:     videos/_2018/cramer.py (lines 2027-2042)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZEqualsVDotK.py ZEqualsVDotK -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

X_COLOR = GREEN


Y_COLOR = RED


Z_COLOR = BLUE


class ZEqualsVDotK(Scene):
    def construct(self):
        equation = VGroup(
            OldTex("z"),
            OldTex("="),
            Matrix(["x", "y", "z"]),
            OldTex("\\cdot"),
            IntegerMatrix([0, 0, 1]),
        )
        equation[2].elements.set_color_by_gradient(X_COLOR, Y_COLOR, Z_COLOR)
        equation[4].elements.set_color(BLUE)
        equation.arrange(RIGHT, buff=MED_SMALL_BUFF)
        equation.to_edge(LEFT)

        self.play(Write(equation))
        self.wait()
