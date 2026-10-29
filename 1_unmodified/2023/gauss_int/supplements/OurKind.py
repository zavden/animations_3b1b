# ==============================================================================
# Scene:      OurKind
# Source:     videos/_2023/gauss_int/supplements.py (lines 563-573)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OurKind.py OurKind -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OurKind(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.play(self.change_students("pondering", "thinking", "pondering", look_at=self.screen))
        self.play(
            self.teacher.says("Where there is\ncircular symmetry,\nour kind thrives", mode="hooray")
        )
        self.play(self.change_students("happy", "thinking", "tease"))
        self.play(self.teacher.change("tease"))
        self.look_at(self.screen)
        self.wait(6)
