# ==============================================================================
# Scene:      QuizTime
# Source:     videos/_2023/convolutions2/supplements.py (lines 5-12)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuizTime.py QuizTime -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class QuizTime(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(self.teacher.says("Quiz time!", mode="hooray"))
        self.play(
            self.change_students("happy", "tease", "hooray")
        )
        self.wait(2)
