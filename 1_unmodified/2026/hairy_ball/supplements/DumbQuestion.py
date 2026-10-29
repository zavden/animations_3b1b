# ==============================================================================
# Scene:      DumbQuestion
# Source:     videos/_2026/hairy_ball/supplements.py (lines 477-495)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DumbQuestion.py DumbQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DumbQuestion(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[2].says("Isn’t it\nobvious?", mode="confused", look_at=self.screen, bubble_direction=LEFT),
            stds[1].change("angry", look_at=morty.eyes),
            stds[0].change("erm", look_at=morty.eyes),
            morty.change("guilty"),
        )
        self.wait(2)
        self.play(
            stds[0].change("confused", self.screen),
            stds[1].change("sassy", self.screen),
            stds[2].change("maybe", morty.eyes),
        )
        self.wait(4)
