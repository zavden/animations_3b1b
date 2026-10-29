# ==============================================================================
# Scene:      IsItHelpful
# Source:     videos/_2022/puzzles/subsets.py (lines 4658-4679)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsItHelpful.py IsItHelpful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsItHelpful(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Is that helpful here?",
            index=2,
            added_anims=[LaggedStart(
                self.students[0].change("confused", self.screen),
                self.students[1].change("maybe", self.screen),
                lag_ratio=0.5,
            )]
        )
        self.wait(2)
        self.teacher_says(
            "Honestly...\nnot really.",
            target_mode="shruggie",
            added_anims=[self.change_students(
                "sassy", "erm",
                look_at=self.teacher.eyes,
            )]
        )
        self.play(self.students[2].change("angry"))
        self.wait(3)
