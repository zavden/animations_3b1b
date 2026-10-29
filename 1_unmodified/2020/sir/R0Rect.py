# ==============================================================================
# Scene:      R0Rect
# Source:     videos/_2020/sir.py (lines 2693-2698)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl R0Rect.py R0Rect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class R0Rect(Scene):
    def construct(self):
        rect = SurroundingRectangle(OldTexText("R0 = 2.20"))
        rect.set_stroke(YELLOW, 4)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
