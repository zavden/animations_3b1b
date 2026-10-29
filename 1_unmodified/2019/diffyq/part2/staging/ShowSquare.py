# ==============================================================================
# Scene:      ShowSquare
# Source:     videos/_2019/diffyq/part2/staging.py (lines 438-442)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/staging.py
#
# Run from this folder:
#     manimgl ShowSquare.py ShowSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/staging.py -----

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



# ----- From _2019/diffyq/part2/staging.py -----

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
        rect.set_color(YELLOW)
        self.play(ShowCreationThenFadeOut(rect))


class ShowSquare(ShowRect):
    CONFIG = {
        "height": 1,
        "width": 1,
    }
