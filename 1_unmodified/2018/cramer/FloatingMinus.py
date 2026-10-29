# ==============================================================================
# Scene:      FloatingMinus
# Source:     videos/_2018/cramer.py (lines 624-628)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FloatingMinus.py FloatingMinus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FloatingMinus(Scene):
    def construct(self):
        minus = OldTex("-")
        self.add(minus)
        self.play(minus.shift, 2.9 * UP, run_time=1)
