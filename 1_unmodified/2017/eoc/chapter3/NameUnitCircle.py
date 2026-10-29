# ==============================================================================
# Scene:      NameUnitCircle
# Source:     videos/_2017/eoc/chapter3.py (lines 2133-2139)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameUnitCircle.py NameUnitCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NameUnitCircle(Scene):
    def construct(self):
        words = OldTexText("Unit circle")
        words.scale(2)
        words.set_color(BLUE)
        self.play(Write(words))
        self.wait()
