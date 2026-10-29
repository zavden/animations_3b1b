# ==============================================================================
# Scene:      AskIfItsTheArea
# Source:     videos/_2023/convolutions2/supplements.py (lines 543-565)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskIfItsTheArea.py AskIfItsTheArea -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskIfItsTheArea(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        # Test
        self.play(
            stds[0].says(
                TexText("Is $[f*g](s)$ the\narea of this slice?"),
                mode="raise_left_hand",
                look_at=self.screen,
            ),
            stds[1].change("pondering", self.screen),
            stds[2].change("pondering", self.screen),
            morty.change("tease", stds[0].eyes),
        )
        self.wait(3)
        self.play(morty.says("Almost!", mode="coin_flip_2"))
        self.play(
            self.change_students("confused", "erm", "hesitant", look_at=morty.eyes)
        )
        self.wait(5)
