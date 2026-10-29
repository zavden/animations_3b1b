# ==============================================================================
# Scene:      AskHowItsImplemented
# Source:     videos/_2020/hamming.py (lines 4891-4899)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHowItsImplemented.py AskHowItsImplemented -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskHowItsImplemented(TeacherStudentsScene):
    def construct(self):
        self.student_says("How do you\\\\implement this?")
        self.play(
            self.teacher.change, "happy",
            self.change_students("pondering", "confused"),
        )
        self.look_at(self.screen)
        self.wait(6)
