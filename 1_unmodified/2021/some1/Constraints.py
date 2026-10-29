# ==============================================================================
# Scene:      Constraints
# Source:     videos/_2021/some1.py (lines 147-153)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Constraints.py Constraints -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Constraints(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("What are the\\\\constraints?"),
            added_anims=[self.teacher.change("tease")]
        )
        self.wait(3)
