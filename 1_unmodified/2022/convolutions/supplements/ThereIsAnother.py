# ==============================================================================
# Scene:      ThereIsAnother
# Source:     videos/_2022/convolutions/supplements.py (lines 130-136)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThereIsAnother.py ThereIsAnother -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThereIsAnother(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("There is another"),
            self.change_students("pondering", "thinking", "erm", look_at=self.screen)
        )
        self.wait(2)
