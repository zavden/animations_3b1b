# ==============================================================================
# Scene:      ThatsNotHowIBehave
# Source:     videos/_2020/sir.py (lines 2316-2328)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatsNotHowIBehave.py ThatsNotHowIBehave -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThatsNotHowIBehave(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "That's...not\\\\how I behave.",
            target_mode="sassy",
            look_at=self.screen,
        )
        self.play(
            self.teacher.change, "guilty",
            self.change_students("erm", "erm", "sassy")
        )
        self.look_at(self.screen)
        self.wait(20)
