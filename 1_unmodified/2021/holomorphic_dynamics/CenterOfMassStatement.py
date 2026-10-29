# ==============================================================================
# Scene:      CenterOfMassStatement
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2413-2423)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CenterOfMassStatement.py CenterOfMassStatement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CenterOfMassStatement(Scene):
    def construct(self):
        words = OldTexText(
            "If there's an attracting cycle, the seed\\\\",
            "$z_0 = (r_1 + r_2 + r_3) / 3$ will fall into it."
        )
        words.set_stroke(BLACK, 8, background=True)
        words.to_corner(UL)

        self.play(Write(words))
        self.wait()
