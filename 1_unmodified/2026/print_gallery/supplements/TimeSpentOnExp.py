# ==============================================================================
# Scene:      TimeSpentOnExp
# Source:     videos/_2026/print_gallery/supplements.py (lines 479-493)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TimeSpentOnExp.py TimeSpentOnExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TimeSpentOnExp(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "confused", "erm", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            morty.change("raise_left_hand", 3 * UR),
            self.change_students("hesitant", "pondering", "sassy", look_at=3 * UR)
        )
        self.wait(3)
