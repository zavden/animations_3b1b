# ==============================================================================
# Scene:      AskIfThisIsReal
# Source:     videos/_2024/transformers/supplements.py (lines 1917-1938)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskIfThisIsReal.py AskIfThisIsReal -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskIfThisIsReal(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        # Test
        self.play(
            stds[0].says("Is this how ChatGPT stores facts?"),
            morty.change("well"),
        )
        self.look_at(self.screen)
        self.wait()
        self.play(
            self.change_students("speaking", "pondering", "skeptical", look_at=self.screen)
        )
        self.wait(2)
        self.play(
            morty.says("Almost certainly\nnot quite...", mode="guilty", bubble_direction=RIGHT),
            stds[1].change("angry"),
            stds[2].change("erm"),
        )
        self.wait(4)
