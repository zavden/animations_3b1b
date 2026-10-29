# ==============================================================================
# Scene:      LetsSumUp
# Source:     videos/_2021/matrix_exp.py (lines 6237-6243)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsSumUp.py LetsSumUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LetsSumUp(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "Let's review",
            added_anims=[self.change_students("thinking", "pondering", "thinking")]
        )
        self.wait(3)
