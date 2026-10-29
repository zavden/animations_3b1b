# ==============================================================================
# Scene:      ReferenceStraightforwardValueMatrix
# Source:     videos/_2024/transformers/supplements.py (lines 1143-1156)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceStraightforwardValueMatrix.py ReferenceStraightforwardValueMatrix -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReferenceStraightforwardValueMatrix(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        morty.body.insert_n_curves(100)
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("happy", "well", "tease", look_at=3 * UR)
        )
        self.wait(3)
        self.play(
            morty.change("hesitant"),
            self.change_students("erm", "hesitant", "guilty", look_at=3 * UR)
        )
        self.wait(5)
