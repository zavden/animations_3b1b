# ==============================================================================
# Scene:      FunPartWords
# Source:     videos/_2021/newton_fractal.py (lines 2814-2817)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FunPartWords.py FunPartWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FunPartWords(Scene):
    def construct(self):
        text = OldTexText("Now here's \\\\ the fun part", font_size=72)
        self.add(text)
