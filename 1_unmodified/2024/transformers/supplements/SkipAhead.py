# ==============================================================================
# Scene:      SkipAhead
# Source:     videos/_2024/transformers/supplements.py (lines 522-532)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SkipAhead.py SkipAhead -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SkipAhead(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        morty = self.teacher
        self.play(
            morty.change("hesitant", self.students),
            self.change_students("confused", "pondering", "pondering", look_at=self.screen),
        )
        self.wait(2)
        self.play(self.change_students("confused", "tease", "well", look_at=morty.eyes))
        self.wait(5)
