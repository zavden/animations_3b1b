# ==============================================================================
# Scene:      ShowCross
# Source:     videos/_2019/diffyq/part2/staging.py (lines 452-457)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowCross.py ShowCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowCross(Scene):
    def construct(self):
        cross = Cross(Square())
        cross.set_width(3)
        cross.set_height(1, stretch=True)
        self.play(ShowCreation(cross))
