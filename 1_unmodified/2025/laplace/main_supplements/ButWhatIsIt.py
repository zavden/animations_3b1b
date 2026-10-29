# ==============================================================================
# Scene:      ButWhatIsIt
# Source:     videos/_2025/laplace/main_supplements.py (lines 180-199)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButWhatIsIt.py ButWhatIsIt -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButWhatIsIt(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[0].change("erm", self.screen),
            stds[1].says("But, what is it?", mode="maybe", bubble_direction=LEFT),
            stds[2].change("sassy", self.screen),
            morty.change("guilty"),
        )
        self.wait(2)
        self.play(
            morty.change("raise_right_hand", 2 * UR),
            stds[0].change("pondering", 2 * UR),
            stds[1].debubble(mode="pondering", look_at=2 * UR),
            stds[2].change("pondering", 2 * UR),
        )
        self.wait(3)
