# ==============================================================================
# Scene:      JumpToThisPoint
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 644-665)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JumpToThisPoint.py JumpToThisPoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JumpToThisPoint(Scene):
    def construct(self):
        dot = Dot(color=YELLOW)
        dot.scale(0.5)

        arrow = Vector(DR, color=WHITE)
        arrow.next_to(dot, UL, SMALL_BUFF)
        words = OldTexText(
            "Jump directly to\\\\",
            "this point?",
        )
        words.add_background_rectangle_to_submobjects()
        words.next_to(arrow.get_start(), UP, SMALL_BUFF)

        self.play(
            FadeInFromLarge(dot, 20),
            rate_func=rush_into,
        )
        self.play(
            GrowArrow(arrow),
            FadeInFromDown(words),
        )
