# ==============================================================================
# Scene:      UseNewton
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1546-1568)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UseNewton.py UseNewton -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UseNewton(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText(
                "You could solve\\\\ $A(z) - z\\cdot B(z) = 0$ \\\\",
                "using Newton's method"
            ),
            bubble_config={
                "width": 4,
                "height": 3,
            },
            target_mode="hooray",
            added_anims=[
                self.change_students("confused", "erm", "maybe")
            ]
        )
        self.wait(2)
        self.student_says(
            Text("Too meta..."),
            target_mode="sassy",
            index=2,
        )
        self.wait(3)
