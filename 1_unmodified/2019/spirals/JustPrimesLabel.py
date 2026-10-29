# ==============================================================================
# Scene:      JustPrimesLabel
# Source:     videos/_2019/spirals.py (lines 1206-1213)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JustPrimesLabel.py JustPrimesLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JustPrimesLabel(Scene):
    def construct(self):
        text = OldTexText("Just the primes")
        text.scale(2)
        text.to_corner(UL)
        self.play(Write(text))
        self.wait(3)
        self.play(FadeOut(text, DOWN))
