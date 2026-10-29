# ==============================================================================
# Scene:      ComplainAboutProgress
# Source:     videos/_2021/shadows.py (lines 5222-5233)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutProgress.py ComplainAboutProgress -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplainAboutProgress(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            OldTexText("Wait, is that all\\\\we've accomplished?"),
            target_mode="angry",
        )
        self.play_student_changes(
            "guilty", "erm",
            look_at=self.students[2].eyes,
            added_anims=[self.teacher.change("guilty")],
        )
        self.wait(4)
