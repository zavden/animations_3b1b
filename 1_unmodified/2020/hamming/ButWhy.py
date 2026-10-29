# ==============================================================================
# Scene:      ButWhy
# Source:     videos/_2020/hamming.py (lines 5429-5439)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButWhy.py ButWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButWhy(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Hang on...\\\\why?", target_mode="confused",
            added_anims=[self.teacher.change, "tease"]
        )
        self.play_student_changes(
            "maybe", "erm", "confused",
            look_at=self.screen,
        )
        self.wait(6)
