# ==============================================================================
# Scene:      ThisIsTheCoolPart
# Source:     videos/_2022/convolutions/supplements.py (lines 328-340)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsTheCoolPart.py ThisIsTheCoolPart -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThisIsTheCoolPart(TeacherStudentsScene):
    def construct(self):
        # Blah
        self.play(
            self.teacher.says("Now for the\ncool part!", mode="hooray"),
            self.change_students("happy", "tease", "well")
        )
        self.wait(2)
        self.play(
            self.change_students("thinking", "thinking", "happy", look_at=self.screen),
            self.teacher.change("tease")
        )
        self.wait(3)
