# ==============================================================================
# Scene:      AtLeastKindOf
# Source:     videos/_2024/transformers/supplements.py (lines 712-727)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AtLeastKindOf.py AtLeastKindOf -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AtLeastKindOf(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.says("...kind of", mode="hesitant"),
            self.change_students("hesitant", "sassy", "erm", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            self.change_students("sassy", "hesitant", "hesitant", look_at=morty.eyes),
            morty.change("guilty"),
        )
        self.wait(4)
