# ==============================================================================
# Scene:      AskWhyItWorks
# Source:     videos/_2020/med_test.py (lines 4132-4143)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyItWorks.py AskWhyItWorks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskWhyItWorks(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Huh?  Why does\\\\that work?",
            target_mode="confused",
        )
        self.play_student_changes(
            "pondering", "erm", "confused",
            look_at=self.screen,
        )
        self.play(self.teacher.change, "happy")
        self.wait(3)
