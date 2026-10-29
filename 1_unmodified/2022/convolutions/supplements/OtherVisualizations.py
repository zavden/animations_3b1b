# ==============================================================================
# Scene:      OtherVisualizations
# Source:     videos/_2022/convolutions/supplements.py (lines 173-189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OtherVisualizations.py OtherVisualizations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OtherVisualizations(TeacherStudentsScene):
    def construct(self):
        self.play(self.change_students("happy", "thinking", "tease", look_at=self.screen))
        self.play(
            self.teacher.says("Can you think of\nother visualizations?"),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            self.change_students("confused", "erm", "thinking")
        )
        self.wait(4)
        self.play(
            self.students[2].change("raise_right_hand", self.teacher.eyes),
            self.teacher.change("tease"),
        )
        self.wait(2)
