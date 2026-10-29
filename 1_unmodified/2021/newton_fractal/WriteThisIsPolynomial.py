# ==============================================================================
# Scene:      WriteThisIsPolynomial
# Source:     videos/_2021/newton_fractal.py (lines 915-919)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteThisIsPolynomial.py WriteThisIsPolynomial -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteThisIsPolynomial(Scene):
    def construct(self):
        text = OldTexText("(Some polynomial in $t$)", font_size=24)
        self.play(Write(text))
        self.wait()
