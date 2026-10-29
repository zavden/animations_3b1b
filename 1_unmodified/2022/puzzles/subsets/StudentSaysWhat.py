# ==============================================================================
# Scene:      StudentSaysWhat
# Source:     videos/_2022/puzzles/subsets.py (lines 5022-5033)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StudentSaysWhat.py StudentSaysWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StudentSaysWhat(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "I'm sorry, what?!",
            target_mode="angry"
        )
        self.play(
            self.teacher.change("happy"),
            self.change_students("confused", "sassy", "angry")
        )
        self.look_at(self.screen)
        self.wait(4)
