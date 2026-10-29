# ==============================================================================
# Scene:      LouisPasteurQuote
# Source:     videos/_2020/hamming.py (lines 6048-6054)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LouisPasteurQuote.py LouisPasteurQuote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LouisPasteurQuote(Scene):
    def construct(self):
        quote = OldTexText("``Luck favors a\\\\prepared mind''")
        quote.scale(2)
        quote.set_stroke(BLACK, 8, background=True)
        self.play(Write(quote))
        self.wait()
