# ==============================================================================
# Scene:      DopplerFormulaInsert
# Source:     videos/_2018/uncertainty.py (lines 2046-2069)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DopplerFormulaInsert.py DopplerFormulaInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class DopplerFormulaInsert(Scene):
    def construct(self):
        formula = OldTex(
            "f_{\\text{echo}", "=",
            "\\left(1 + \\frac{v}{c}\\right)",
            "f_{\\text{pulse}}"
        )
        formula[0].set_color(BLUE)
        formula[3].set_color(YELLOW)

        randy = Randolph(color = BLUE_C)
        formula.scale(1.5)
        formula.next_to(randy, UP+LEFT)
        formula.shift_onto_screen()

        self.add(randy)
        self.play(
            LaggedStartMap(FadeIn, formula),
            randy.change, "pondering", randy.get_bottom(),
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.wait()
