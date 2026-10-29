# ==============================================================================
# Scene:      AskForExample
# Source:     videos/_2022/convolutions/supplements.py (lines 205-215)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskForExample.py AskForExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskForExample(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change("raise_right_hand", self.screen),
            self.change_students("pondering", "thinking", "confused", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            self.students[2].says("Can we go do\na concrete example?", mode="raise_left_hand", bubble_direction=LEFT)
        )
        self.wait(3)
