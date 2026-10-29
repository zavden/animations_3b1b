# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2022/puzzles/subsets.py (lines 4726-4732)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(2, 0.5)
        rect.set_stroke(YELLOW, 2)
        self.play(ShowCreation(rect))
        self.wait()
        self.play(FadeOut(rect))
