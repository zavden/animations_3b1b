# ==============================================================================
# Scene:      AskAboutGeneralTheory
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1081-1098)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutGeneralTheory.py AskAboutGeneralTheory -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutGeneralTheory(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            OldTexText("Think about constructing\\\\a general theory"),
            added_anims=[self.change_students(
                "pondering", "thinking", "pondering",
                look_at=UP,
            )]
        )
        self.wait(3)
        self.teacher_says(
            OldTexText("What questions would\\\\you ask?"),
            target_mode="tease",
        )
        self.play_student_changes("thinking", "pondering")
        self.wait(3)

        self.embed()
