# ==============================================================================
# Scene:      Usually
# Source:     videos/_2023/gauss_int/supplements.py (lines 471-477)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Usually.py Usually -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Usually(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.play(self.change_students("pondering", "pondering", "pondering", look_at=self.screen))
        self.play(self.teacher.says("At least, usually"))
        self.play(self.change_students("erm", "confused", "sassy"))
        self.wait(3)
