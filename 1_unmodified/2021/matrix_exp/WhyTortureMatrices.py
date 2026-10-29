# ==============================================================================
# Scene:      WhyTortureMatrices
# Source:     videos/_2021/matrix_exp.py (lines 1326-1350)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyTortureMatrices.py WhyTortureMatrices -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyTortureMatrices(TeacherStudentsScene):
    def construct(self):
        self.play_student_changes(
            "maybe", "confused", "erm",
            look_at=self.screen,
        )
        q_marks = VGroup()
        for student in self.students:
            marks = OldTex("???")
            marks.next_to(student, UP)
            q_marks.add(marks)
        self.play(FadeIn(q_marks, 0.25 * UP, lag_ratio=0.1, run_time=2))
        self.wait(2)
        self.student_says(
            OldTexText("Why...would you\\\\ever want\\\\to do that?"),
            index=2,
            added_anims=[FadeOut(q_marks)],
        )
        self.play(
            self.change_students("confused", "pondering", "raise_left_hand", look_at=self.screen),
            self.teacher.change("tease", self.screen)
        )
        self.wait(2)
        self.play(self.students[0].change("erm"))
        self.wait(7)
