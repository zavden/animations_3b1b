# ==============================================================================
# Scene:      PauseAndPonder
# Source:     videos/_2021/newton_fractal.py (lines 1973-1977)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PauseAndPonder.py PauseAndPonder -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PauseAndPonder(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("Pause and\nponder", target_mode="hooray")
        self.play_all_student_changes("thinking", look_at=self.screen)
        self.wait(4)
