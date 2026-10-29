# ==============================================================================
# Scene:      CramersYEvaluation
# Source:     videos/_2018/cramer.py (lines 2125-2139)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CramersYEvaluation.py CramersYEvaluation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CramersYEvaluation(Scene):
    def construct(self):
        frac = OldTex("{(2)(2) - (4)(0) \\over (2)(1) - (-1)(0)}")[0]
        VGroup(frac[1], frac[11], frac[15], frac[26]).set_color(GREEN)
        VGroup(frac[4], frac[8]).set_color(MAROON_B)
        VGroup(frac[18], frac[22], frac[23]).set_color(RED)

        group = VGroup(
            OldTex("="), frac,
            OldTex("= \\frac{4}{2}"), OldTex("=2")
        )
        group.arrange(RIGHT)

        self.add(group)
        self.wait(1)
