# ==============================================================================
# Scene:      AskWhoCares
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 16-41)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhoCares.py AskWhoCares -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskWhoCares(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[0].change("guilty", stds[1].eyes),
            stds[1].says("Who cares?!", mode="angry", look_at=self.screen),
            stds[2].change("erm", stds[1].eyes),
            morty.change("guilty", stds[1].eyes),
        )
        self.wait(3)
        self.play(
            FadeOut(stds[1].bubble),
            stds[0].change("hesitant"),
            stds[1].says("What practial use\ndoes this have?", "sassy"),
        )
        self.wait(4)
        self.play(
            stds[0].change("thinking", morty.eyes),
            stds[1].debubble(),
            stds[2].change("pondering", morty.eyes),
            morty.says("Here's why\nI love it")
        )
        self.wait()
