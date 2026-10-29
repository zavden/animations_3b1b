# ==============================================================================
# Scene:      ShowHLine
# Source:     videos/_2019/diffyq/part2/staging.py (lines 445-449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowHLine.py ShowHLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowHLine(Scene):
    def construct(self):
        line = Line(LEFT, RIGHT)
        line.set_color(BLUE)
        self.play(ShowCreationThenFadeOut(line))
