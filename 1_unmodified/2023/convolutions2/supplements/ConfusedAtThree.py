# ==============================================================================
# Scene:      ConfusedAtThree
# Source:     videos/_2023/convolutions2/supplements.py (lines 439-450)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusedAtThree.py ConfusedAtThree -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ConfusedAtThree(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("maybe", "confused", "sassy", look_at=self.screen)
        )
        self.wait(2)
        self.look_at(morty.get_corner(UL))
        self.play(self.change_students("hesitant", "maybe", "pondering", look_at=self.screen))
        self.wait(5)
