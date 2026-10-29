# ==============================================================================
# Scene:      SimpleRect
# Source:     videos/_2020/chess.py (lines 3846-3853)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect.py SimpleRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleRect(Scene):
    def construct(self):
        rect = SurroundingRectangle(
            VGroup(Integer(4), Integer(16), Integer(0)).arrange(RIGHT, MED_LARGE_BUFF),
        )
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(FadeOut(rect))
