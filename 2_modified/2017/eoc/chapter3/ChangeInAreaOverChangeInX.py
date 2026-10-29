# ==============================================================================
# Scene:      ChangeInAreaOverChangeInX
# Source:     videos/_2017/eoc/chapter3.py (lines 777-797)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ChangeInAreaOverChangeInX.py ChangeInAreaOverChangeInX -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
# ==============================================================================

from manim_imports_ext import *

class ChangeInAreaOverChangeInX(Scene):
    def construct(self):
        fractions = []
        for pair in ("Change in area", "Change in $x$"), ("$d(x^2)$", "$dx$"):
            # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTexText
            top, bottom = list(map(OldTexText, pair))
            top.set_color(YELLOW)
            bottom.set_color(BLUE_B)
            frac_line = OldTex("-")
            frac_line.stretch_to_fit_width(top.get_width())
            top.next_to(frac_line, UP, SMALL_BUFF)
            bottom.next_to(frac_line, DOWN, SMALL_BUFF)
            fractions.append(VGroup(
                top, frac_line, bottom
            ))
        words, symbols = fractions

        self.play(Write(words[0], run_time = 1))
        self.play(*list(map(Write, words[1:])), run_time = 1)
        self.wait()
        self.play(Transform(words, symbols))
        self.wait()
