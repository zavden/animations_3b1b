# ==============================================================================
# Scene:      CramersXEvaluation
# Source:     videos/_2018/cramer.py (lines 2142-2159)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CramersXEvaluation.py CramersXEvaluation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

# Largely copy-pasted.  Not great, but what are you gonna do.
class CramersXEvaluation(Scene):
    def construct(self):
        frac = OldTex("{(4)(1) - (-1)(2) \\over (2)(1) - (-1)(0)}")[0]
        VGroup(frac[1], frac[12]).set_color(MAROON_B)
        VGroup(frac[4], frac[8], frac[9]).set_color(RED)
        VGroup(frac[16], frac[27]).set_color(GREEN)
        VGroup(frac[19], frac[23], frac[24]).set_color(RED)

        group = VGroup(
            OldTex("="), frac,
            OldTex("= \\frac{6}{2}"), OldTex("=3")
        )
        group.arrange(RIGHT)
        group.add_to_back(BackgroundRectangle(group))

        self.add(group)
        self.wait(1)
