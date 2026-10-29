# ==============================================================================
# Scene:      GoalWrapper
# Source:     videos/_2018/div_curl.py (lines 4402-4413)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalWrapper.py GoalWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GoalWrapper(Scene):
    def construct(self):
        goal = OldTexText(
            "Goal: Teach/remind people \\\\ that they love math"
        )
        goal.to_edge(UP)
        self.add(goal)

        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(goal, DOWN)
        self.play(ShowCreation(screen_rect))
        self.wait()
