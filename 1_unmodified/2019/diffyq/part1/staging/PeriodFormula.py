# ==============================================================================
# Scene:      PeriodFormula
# Source:     videos/_2019/diffyq/part1/staging.py (lines 86-93)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl PeriodFormula.py PeriodFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_period_formula():
    return OldTex(
        "2\\pi", "\\sqrt{\\,", "L", "/", "g", "}",
        tex_to_color_map={
            "L": BLUE,
            "g": YELLOW,
        }
    )



# ----- From _2019/diffyq/part1/staging.py -----

class PeriodFormula(Scene):
    def construct(self):
        formula = get_period_formula()
        formula.scale(2)
        q_mark = OldTex("?")
        q_mark.scale(3)
        q_mark.next_to(formula, RIGHT)
        self.add(formula, q_mark)
