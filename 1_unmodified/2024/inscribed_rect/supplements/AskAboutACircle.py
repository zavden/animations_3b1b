# ==============================================================================
# Scene:      AskAboutACircle
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 265-275)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutACircle.py AskAboutACircle -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutACircle(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            stds[2].says("What does it look\nlike for a circle?", "maybe"),
            morty.change("tease", stds[2].eyes),
            stds[1].change("pondering", 4 * UR),
            stds[0].change("confused", 4 * UR),
        )
        self.wait(4)
