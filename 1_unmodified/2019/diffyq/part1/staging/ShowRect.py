# ==============================================================================
# Scene:      ShowRect
# Source:     videos/_2019/diffyq/part1/staging.py (lines 49-62)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowRect.py ShowRect -w -m --fps 15
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
