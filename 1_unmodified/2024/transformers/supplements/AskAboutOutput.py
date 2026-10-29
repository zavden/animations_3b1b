# ==============================================================================
# Scene:      AskAboutOutput
# Source:     videos/_2024/transformers/supplements.py (lines 1265-1279)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutOutput.py AskAboutOutput -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutOutput(TeacherStudentsScene):
    random_seed = 3
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            stds[0].change("hesitant", look_at=stds[1].eyes),
            stds[1].says("What about the\nOutput matrix?", mode="raise_left_hand"),
            stds[2].change("hesitant", look_at=stds[1].eyes),
        )
        self.play(
            morty.change("concentrating")
        )
        self.play(Blink(morty))
        self.wait(5)
