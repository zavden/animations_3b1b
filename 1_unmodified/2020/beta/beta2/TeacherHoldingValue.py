# ==============================================================================
# Scene:      TeacherHoldingValue
# Source:     videos/_2020/beta/beta2.py (lines 702-709)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TeacherHoldingValue.py TeacherHoldingValue -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TeacherHoldingValue(TeacherStudentsScene):
    def construct(self):
        self.play(self.teacher.change, "raise_right_hand", self.screen)
        self.play_all_student_changes(
            "pondering",
            look_at=self.screen,
        )
        self.wait(8)
