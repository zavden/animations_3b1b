# ==============================================================================
# Scene:      AirResistanceBrace
# Source:     videos/_2019/diffyq/part1/staging.py (lines 77-83)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AirResistanceBrace.py AirResistanceBrace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AirResistanceBrace(Scene):
    def construct(self):
        brace = Brace(Line(ORIGIN, RIGHT), DOWN)
        word = OldTexText("Air resistance")
        word.next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), FadeIn(word, UP))
        self.wait()
