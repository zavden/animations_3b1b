# ==============================================================================
# Scene:      FundamentalTheorem
# Source:     videos/_2017/eoc/chapter1.py (lines 2674-2692)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FundamentalTheorem.py FundamentalTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FundamentalTheorem(Scene):
    def construct(self):
        words = OldTexText("""
            Fundamental theorem of calculus
        """)
        words.to_edge(UP)
        arrow = DoubleArrow(LEFT, RIGHT).shift(2*RIGHT)
        deriv = OldTex(
            "{dA", "\\over \\,", "dx}", "=", "x^2"
        )
        deriv.set_color_by_tex("dA", GREEN)
        deriv.next_to(arrow, RIGHT)

        self.play(ShowCreation(arrow))
        self.wait()
        self.play(Write(deriv))
        self.wait()
        self.play(Write(words))
        self.wait()
