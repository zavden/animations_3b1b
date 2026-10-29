# ==============================================================================
# Scene:      HowManyIntotal
# Source:     videos/_2022/puzzles/subsets.py (lines 4539-4550)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowManyIntotal.py HowManyIntotal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowManyIntotal(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("How many total\\\\subsets are there?"),
            bubble_config=dict(width=4, height=3),
            added_anims=[self.change_students(
                "happy", "pondering", "tease",
                look_at=self.screen,
            )],
            run_time=2,
        )
        self.wait(4)
