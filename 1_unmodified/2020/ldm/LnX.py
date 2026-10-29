# ==============================================================================
# Scene:      LnX
# Source:     videos/_2020/ldm.py (lines 917-931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LnX.py LnX -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LnX(Scene):
    def construct(self):
        sym = OldTex("\\ln(x)")
        sym.scale(3)
        sym.shift(UP)
        sym.set_stroke(BLACK, 5, background=True)

        word = OldTexText("Natural?")
        word.scale(1.5)
        word.set_color(YELLOW)
        word.set_stroke(BLACK, 5, background=True)
        word.next_to(sym, DOWN, buff=0.5)
        arrow = Arrow(word.get_top(), sym[0][1].get_bottom())

        self.add(sym, word, arrow)
