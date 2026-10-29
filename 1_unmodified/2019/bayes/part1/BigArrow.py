# ==============================================================================
# Scene:      BigArrow
# Source:     videos/_2019/bayes/part1.py (lines 3169-3178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigArrow.py BigArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BigArrow(Scene):
    def construct(self):
        arrow = Arrow(
            3 * DOWN + 4 * LEFT,
            3 * RIGHT + DOWN,
            path_arc=50 * DEGREES,
        )

        self.play(ShowCreation(arrow))
        self.wait()
