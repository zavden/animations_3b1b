# ==============================================================================
# Scene:      AskAboutAttention
# Source:     videos/_2024/transformers/chm.py (lines 45-56)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAttention.py AskAboutAttention -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutAttention(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher
        self.play(
            morty.change("tease"),
            stds[2].says("Can you explain what\nAttention does?", mode="raise_left_hand", bubble_direction=LEFT),
            stds[1].change("pondering", self.screen),
            stds[0].change("pondering", self.screen),
        )
        self.wait(4)
