# ==============================================================================
# Scene:      ReadFormula
# Source:     videos/_2017/efvgt.py (lines 3207-3224)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReadFormula.py ReadFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MULTIPLIER_COLOR = YELLOW


class ReadFormula(Scene):
    def construct(self):
        formula = OldTex("e^", "{\\pi i}", "=", "-1")
        formula[1].set_color(GREEN_B)
        formula[3].set_color(MULTIPLIER_COLOR)
        formula.scale(2)

        randy = Randolph()
        randy.shift(2*LEFT)
        formula.next_to(randy, RIGHT, aligned_edge = UP)
        randy.look_at(formula)

        self.add(randy, formula)
        self.wait()
        self.play(randy.change_mode, "thinking")
        self.wait()
        self.play(Blink(randy))
        self.wait(3)
