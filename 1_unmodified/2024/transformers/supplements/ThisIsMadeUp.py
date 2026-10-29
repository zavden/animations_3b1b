# ==============================================================================
# Scene:      ThisIsMadeUp
# Source:     videos/_2024/transformers/supplements.py (lines 991-1000)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsMadeUp.py ThisIsMadeUp -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThisIsMadeUp(TeacherStudentsScene):
    def construct(self):
        for pi in self.students:
            pi.change_mode("pondering").look_at(self.screen)
        self.play(
            self.teacher.says("This is a made-up\nmotivating example"),
            self.change_students("pondering", look_at=self.teacher.eyes)
        )
        self.play(self.change_students("well", "sassy", "guilty", look_at=self.teacher.eyes))
        self.wait(4)
