# ==============================================================================
# Scene:      OneFinalPoint
# Source:     videos/_2021/matrix_exp.py (lines 3329-3339)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneFinalPoint.py OneFinalPoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OneFinalPoint(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("One final point\\\\about one-dimension"),
            bubble_config={"height": 3, "width": 4},
        )
        self.play_student_changes(
            "happy", "hesitant", "tease",
            added_anims=[self.teacher.animate.look_at(self.students[2])]
        )
        self.wait(3)
