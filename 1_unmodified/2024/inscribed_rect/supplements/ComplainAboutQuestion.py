# ==============================================================================
# Scene:      ComplainAboutQuestion
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 241-253)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutQuestion.py ComplainAboutQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ComplainAboutQuestion(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("guilty"),
            stds[1].says("That's just a pretentious\nway to ask the same thing", "angry", look_at=self.screen),
            stds[0].change("hesitant", stds[1].eyes),
            stds[2].change("erm", stds[1].eyes),
        )
        self.wait(5)
