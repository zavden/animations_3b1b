# ==============================================================================
# Scene:      ShowHorizontalDashedLine
# Source:     videos/_2019/diffyq/part1/staging.py (lines 283-287)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowHorizontalDashedLine.py ShowHorizontalDashedLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowHorizontalDashedLine(Scene):
    def construct(self):
        line = DashedLine(LEFT_SIDE, RIGHT_SIDE)
        self.play(ShowCreation(line))
        self.wait()
