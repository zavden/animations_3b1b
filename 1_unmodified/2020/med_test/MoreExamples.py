# ==============================================================================
# Scene:      MoreExamples
# Source:     videos/_2020/med_test.py (lines 2433-2439)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreExamples.py MoreExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreExamples(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "More examples!", target_mode="hooray",
            added_anims=[self.change_students("tired", "erm", "happy", run_time=2)]
        )
        self.wait(3)
