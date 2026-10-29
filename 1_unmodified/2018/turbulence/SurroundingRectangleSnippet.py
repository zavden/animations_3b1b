# ==============================================================================
# Scene:      SurroundingRectangleSnippet
# Source:     videos/_2018/turbulence.py (lines 944-950)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SurroundingRectangleSnippet.py SurroundingRectangleSnippet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SurroundingRectangleSnippet(Scene):
    def construct(self):
        rect = Rectangle()
        rect.set_color(YELLOW)
        rect.set_stroke(width=5)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
