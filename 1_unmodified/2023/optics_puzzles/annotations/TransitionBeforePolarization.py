# ==============================================================================
# Scene:      TransitionBeforePolarization
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 636-646)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransitionBeforePolarization.py TransitionBeforePolarization -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TransitionBeforePolarization(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.change_students("pondering", "thinking", "happy", look_at=self.screen),
        )
        self.wait(3)
        self.play(
            self.teacher.change("raise_left_hand", look_at=3 * UR),
            self.change_students("well", "tease", "happy", look_at=3 * UR),
        )
        self.wait(4)
