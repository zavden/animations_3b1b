# ==============================================================================
# Scene:      WeDontHaveThat
# Source:     videos/_2020/sir.py (lines 2170-2181)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeDontHaveThat.py WeDontHaveThat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WeDontHaveThat(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But we don't\\\\have that!",
            target_mode="angry",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_all_student_changes(
            "angry",
            look_at=self.teacher.eyes
        )
        self.wait(5)
