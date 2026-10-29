# ==============================================================================
# Scene:      ShowSquare
# Source:     videos/_2019/diffyq/part1/staging.py (lines 65-69)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSquare.py ShowSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowRect(Scene):
    CONFIG = {
        "height": 1,
        "width": 3,
    }

    def construct(self):
        rect = Rectangle(
            height=self.height,
            width=self.width,
        )
        rect.set_stroke(YELLOW)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))


class ShowSquare(ShowRect):
    CONFIG = {
        "height": 3,
        "width": 3,
    }
