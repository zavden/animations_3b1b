# ==============================================================================
# Scene:      ThatSeemsIrrelevant
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1240-1254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatSeemsIrrelevant.py ThatSeemsIrrelevant -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThatSeemsIrrelevant(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(
            stds[0].says("That seems irrelevant", mode="sassy"),
            self.change_students(None, "erm", "hesitant", look_at=stds[0].eyes),
            morty.change("guilty"),
        )
        self.wait(2)
        self.play(
            stds[0].debubble(mode="raise_left_hand", look_at=self.screen),
            self.change_students(None, "pondering", "pondering", look_at=self.screen),
        )
        self.wait(5)
