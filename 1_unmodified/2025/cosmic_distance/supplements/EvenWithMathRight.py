# ==============================================================================
# Scene:      EvenWithMathRight
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1069-1075)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EvenWithMathRight.py EvenWithMathRight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EvenWithMathRight(InteractiveScene):
    def construct(self):
        # Test
        words = TexText(R"Even when you have the math right\\you don't necessarily get to the truth", font_size=36)
        words.to_corner(UL)
        self.play(Write(words, lag_ratio=0.1, run_time=2))
        self.wait()
