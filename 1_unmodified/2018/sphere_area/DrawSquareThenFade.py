# ==============================================================================
# Scene:      DrawSquareThenFade
# Source:     videos/_2018/sphere_area.py (lines 1943-1947)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawSquareThenFade.py DrawSquareThenFade -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DrawSquareThenFade(Scene):
    def construct(self):
        square = Square(color=YELLOW, stroke_width=5)
        self.play(ShowCreation(square))
        self.play(FadeOut(square))
