# ==============================================================================
# Scene:      AimingForRediscovery
# Source:     videos/_2026/hairy_ball/supplements.py (lines 329-350)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AimingForRediscovery.py AimingForRediscovery -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AimingForRediscovery(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        goal = Text("Goal: A feeling\nof rediscovery")
        goal.move_to(self.hold_up_spot, DOWN)

        self.play(
            morty.change("tease"),
            self.change_students("pondering", "happy", "hooray", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            FadeIn(goal, shift=UP),
            morty.change("raise_right_hand"),
            self.change_students("pondering", "pondering", "pondering", look_at=goal)
        )
        self.wait(2)
        self.play(self.change_students("thinking", "tease", "erm", look_at=self.screen))
        self.wait()
