# ==============================================================================
# Scene:      AskAboutPi
# Source:     videos/_2023/clt/wordy_scenes.py (lines 726-748)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutPi.py AskAboutPi -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutPi(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(LaggedStart(
            morty.change("happy"),
            stds[1].says("Wait, what?!", mode="surprised"),
            stds[0].change("confused", self.screen),
            stds[2].change("hesitant", self.screen),
        ))
        self.wait()
        self.play(
            stds[2].says("Where's the\ncircle?", mode="raise_left_hand")
        )
        self.wait(3)
        self.play(
            stds[1].debubble(),
            stds[2].debubble(),
            morty.says(TexText(R"We'll cover \\ that later"))
        )
        self.wait(2)
