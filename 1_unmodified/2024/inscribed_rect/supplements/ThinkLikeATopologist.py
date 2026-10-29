# ==============================================================================
# Scene:      ThinkLikeATopologist
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 415-421)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkLikeATopologist.py ThinkLikeATopologist -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThinkLikeATopologist(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("Think like a\n topologist"),
            self.change_students("erm", "tease", "thinking", look_at=self.screen),
        )
        self.wait(5)
