# ==============================================================================
# Scene:      QuestionTheFormula
# Source:     videos/_2023/convolutions2/supplements.py (lines 247-259)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuestionTheFormula.py QuestionTheFormula -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class QuestionTheFormula(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(morty.change("raise_right_hand", 3 * UR))
        self.play(
            stds[0].change("erm", 3 * UR),
            stds[1].says("Hang on...", mode="hesitant"),
            stds[2].change("confused", 3 * UR),
        )
        self.wait(3)
