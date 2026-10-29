# ==============================================================================
# Scene:      SimpleCross
# Source:     videos/_2021/shadows.py (lines 5896-5903)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleCross.py SimpleCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleCross(Scene):
    def construct(self):
        lines = VGroup(
            Line(UP, DOWN).set_height(FRAME_HEIGHT),
            Line(LEFT, RIGHT).set_width(FRAME_WIDTH),
        )
        self.play(ShowCreation(lines, lag_ratio=0.5))
        self.wait()
