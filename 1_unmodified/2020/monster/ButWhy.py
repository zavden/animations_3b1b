# ==============================================================================
# Scene:      ButWhy
# Source:     videos/_2020/monster.py (lines 2458-2470)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButWhy.py ButWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButWhy(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "But, why?",
            target_mode="maybe",
            added_anims=[LaggedStart(
                ApplyMethod(self.teacher.change, "guilty"),
                ApplyMethod(self.students[0].change, "confused"),
                ApplyMethod(self.students[1].change, "sassy"),
                lag_ratio=0.5,
            )]
        )
        self.wait(3)
