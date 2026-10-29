# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2018/pi_day.py (lines 1063-1078)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        pi, eq, num = formula = OldTex(
            "\\pi", "=", "6.283185\\dots"
        )
        formula.scale(2)
        pi.scale(1.5, about_edge = RIGHT)
        formula.set_stroke(BLUE, 1)
        formula.set_width(FRAME_WIDTH - 2)
        # formula.shift(0.5*RIGHT)
        self.add(formula)

        words = OldTexText("...according to Euler.")
        words.scale(1.5)
        words.next_to(formula, DOWN, MED_LARGE_BUFF)
        self.add(words)
