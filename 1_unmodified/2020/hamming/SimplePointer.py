# ==============================================================================
# Scene:      SimplePointer
# Source:     videos/_2020/hamming.py (lines 5470-5476)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplePointer.py SimplePointer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimplePointer(Scene):
    def construct(self):
        arrow = Arrow(ORIGIN, [-4, 1.5, 0])
        arrow.center()
        arrow.set_fill(GREY_B)
        self.play(DrawBorderThenFill(arrow))
        self.wait()
