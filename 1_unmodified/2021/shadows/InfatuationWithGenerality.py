# ==============================================================================
# Scene:      InfatuationWithGenerality
# Source:     videos/_2021/shadows.py (lines 6553-6566)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InfatuationWithGenerality.py InfatuationWithGenerality -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InfatuationWithGenerality(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Why are mathematicians\\\\obsessed with abstractions?"),
            index=0,
            added_anims=[
                self.students[1].change("tease"),
                self.students[2].change("pondering"),
            ]
        )
        self.play(
            self.teacher.change("well"),
        )
        self.wait(6)
