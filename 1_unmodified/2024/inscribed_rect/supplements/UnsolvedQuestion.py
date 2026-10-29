# ==============================================================================
# Scene:      UnsolvedQuestion
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 5-13)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnsolvedQuestion.py UnsolvedQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UnsolvedQuestion(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("Here is an\nunsolved problem", mode="tease"),
            self.change_students("pondering", "sassy", "pondering"),
        )
        self.look_at(self.screen)
        self.wait(5)
