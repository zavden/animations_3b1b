# ==============================================================================
# Scene:      FractalDimensionWords
# Source:     videos/_2021/newton_fractal.py (lines 4281-4286)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FractalDimensionWords.py FractalDimensionWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FractalDimensionWords(Scene):
    def construct(self):
        text = OldTexText("Fractal dimension $\\approx$ 1.44", font_size=60)
        text.to_corner(UL)
        self.play(Write(text))
        self.wait()
