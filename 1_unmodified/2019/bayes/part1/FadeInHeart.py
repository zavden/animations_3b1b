# ==============================================================================
# Scene:      FadeInHeart
# Source:     videos/_2019/bayes/part1.py (lines 4413-4418)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FadeInHeart.py FadeInHeart -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FadeInHeart(Scene):
    def construct(self):
        heart = SuitSymbol("hearts")

        self.play(FadeInFromDown(heart))
        self.play(FadeOut(heart))
