# ==============================================================================
# Scene:      AskAboutFormalStatement
# Source:     videos/_2023/clt/wordy_scenes.py (lines 818-836)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutFormalStatement.py AskAboutFormalStatement -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutFormalStatement(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        question = Text(
            "But what is the\ncentral limit\ntheorem",
            t2s={"theorem": ITALIC},
            t2c={"theorem": YELLOW},
        )

        self.play(
            stds[2].says(question, mode="sassy", bubble_direction=LEFT)
        )
        self.play(morty.change("guilty"))
        self.play(
            stds[0].change("pondering"),
            stds[1].change("erm"),
        )
        self.wait(8)
