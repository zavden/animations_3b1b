# ==============================================================================
# Scene:      AskWhy
# Source:     videos/_2020/beta/beta1.py (lines 922-943)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhy.py AskWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhy(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Wait...why?",
            look_at=self.screen,
        )
        self.play(
            self.students[0].change, "confused", self.screen,
            self.students[1].change, "confused", self.screen,
            self.teacher.change, "tease", self.students[2].eyes,
        )
        self.wait(3)

        self.student_says(
            "Is that really\\\\the answer?",
            target_mode="raise_right_hand",
            added_anims=[self.teacher.change, "thinking"],
        )
        self.wait(2)
        self.teacher_says("Let's dive in!", target_mode="hooray")
        self.play_all_student_changes("hooray")
        self.wait(3)
