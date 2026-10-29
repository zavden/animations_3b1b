# ==============================================================================
# Scene:      WellAlmost
# Source:     videos/_2020/hamming.py (lines 3704-3708)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WellAlmost.py WellAlmost -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WellAlmost(TeacherStudentsScene):
    def construct(self):
        self.teacher_says("Well...\\\\almost", target_mode="hesitant")
        self.play_student_changes("angry", "sassy", "confused")
        self.wait(3)
