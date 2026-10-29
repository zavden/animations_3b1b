# ==============================================================================
# Scene:      EtoILimit
# Source:     videos/_2020/ldm.py (lines 781-796)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EtoILimit.py EtoILimit -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EtoILimit(Scene):
    def construct(self):
        tex = OldTex(
            "\\lim_{n \\to \\infty} \\left(1 + \\frac{it}{n}\\right)^n",
        )[0]
        VGroup(tex[3], tex[12], tex[14]).set_color(YELLOW)
        tex[9].set_color(BLUE)
        tex.scale(1.5)
        tex.set_stroke(BLACK, 5, background=True)
        # self.add(tex)

        text = OldTexText("Interest rate\\\\of ", "$\\sqrt{-1}$")
        text[1].set_color(BLUE) 
        text.scale(1.5)
        text.set_stroke(BLACK, 5, background=True)
        self.add(text)
