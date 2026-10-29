# ==============================================================================
# Scene:      TryWithCos
# Source:     videos/_2017/eoc/chapter3.py (lines 2684-2689)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryWithCos.py TryWithCos -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryWithCos(Scene):
    def construct(self):
        words = OldTexText("What about $\\cos(\\theta)$?")
        words.set_color(YELLOW)
        self.play(Write(words))
        self.wait()
