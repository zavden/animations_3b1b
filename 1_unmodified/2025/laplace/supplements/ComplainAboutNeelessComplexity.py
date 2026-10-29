# ==============================================================================
# Scene:      ComplainAboutNeelessComplexity
# Source:     videos/_2025/laplace/supplements.py (lines 1119-1144)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutNeelessComplexity.py ComplainAboutNeelessComplexity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutNeelessComplexity(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        # Complain
        self.play(
            stds[0].change("confused", self.screen),
            stds[1].says("That’s needlessly\ncomplicated!", mode="angry", look_at=self.screen),
            stds[2].change("maybe", self.screen),
            morty.change("guilty"),
        )
        self.wait(3)
        self.play(
            stds[0].change("erm", self.screen),
            stds[1].debubble(mode="raise_left_hand", look_at=self.screen),
            stds[2].change("sassy", self.screen),
            morty.change("tease"),
        )
        self.wait()
        self.play(
            stds[1].change("raise_right_hand", ORIGIN),
            stds[0].change("pondering", ORIGIN),
            stds[2].change("pondering", ORIGIN),
        )
        self.wait(5)
