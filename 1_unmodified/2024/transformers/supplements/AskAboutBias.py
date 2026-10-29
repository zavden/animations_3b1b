# ==============================================================================
# Scene:      AskAboutBias
# Source:     videos/_2024/transformers/supplements.py (lines 1773-1789)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutBias.py AskAboutBias -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutBias(TeacherStudentsScene):
    def construct(self):
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        self.play(
            self.students[0].change("erm", look_at=self.screen),
            self.students[1].change("confused", look_at=self.screen),
            self.students[2].says("What's that\nbias doing?", look_at=self.screen, bubble_direction=LEFT),
        )
        self.play(
            self.teacher.change("maybe")
        )
        self.wait(4)
        self.play(
            self.change_students("sassy", "maybe", "pondering", look_at=self.screen)
        )
        self.wait(4)
