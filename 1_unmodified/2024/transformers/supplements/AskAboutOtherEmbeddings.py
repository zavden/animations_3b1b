# ==============================================================================
# Scene:      AskAboutOtherEmbeddings
# Source:     videos/_2024/transformers/supplements.py (lines 1003-1021)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutOtherEmbeddings.py AskAboutOtherEmbeddings -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutOtherEmbeddings(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.students[1].says(
                TexText(R"What does $W_Q$ do \\ to the non-nouns?"),
                mode="raise_left_hand"
            ),
            self.teacher.change("guilty"),
        )
        self.play(
            self.change_students("confused", None, "pondering", look_at=self.screen)
        )
        self.wait()
        self.play(self.teacher.change("shruggie"))
        self.play(
            self.change_students("sassy", "maybe", "sassy"),
        )
        self.wait(3)
