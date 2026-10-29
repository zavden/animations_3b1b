# ==============================================================================
# Scene:      ReactToMHSA
# Source:     videos/_2024/transformers/supplements.py (lines 1252-1262)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToMHSA.py ReactToMHSA -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReactToMHSA(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change("hesitant"),
            self.change_students("sad", "confused", "dejected", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            self.change_students("guilty", "maybe", "erm")
        )
        self.wait(3)
