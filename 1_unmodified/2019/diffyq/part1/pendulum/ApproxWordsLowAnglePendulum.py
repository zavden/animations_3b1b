# ==============================================================================
# Scene:      ApproxWordsLowAnglePendulum
# Source:     videos/_2019/diffyq/part1/pendulum.py (lines 815-827)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ApproxWordsLowAnglePendulum.py ApproxWordsLowAnglePendulum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

Lg_formula_config = {
    "tex_to_color_map": {
        "\\theta_0": WHITE,
        "{L}": BLUE,
        "{g}": YELLOW,
    },
}



# ----- From _2019/diffyq/part1/pendulum.py -----

class ApproxWordsLowAnglePendulum(Scene):
    def construct(self):
        period = OldTex(
            "\\text{Period}", "\\approx",
            "2\\pi \\sqrt{\\,{L} / {g}}",
            **Lg_formula_config
        )
        checkmark = OldTex("\\checkmark")
        checkmark.set_color(GREEN)
        checkmark.scale(2)
        checkmark.next_to(period, RIGHT, MED_LARGE_BUFF)

        self.add(period, checkmark)
