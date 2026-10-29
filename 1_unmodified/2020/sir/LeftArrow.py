# ==============================================================================
# Scene:      LeftArrow
# Source:     videos/_2020/sir.py (lines 2464-2469)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeftArrow.py LeftArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LeftArrow(Scene):
    def construct(self):
        arrow = Vector(2 * LEFT)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(FadeOut(arrow))
