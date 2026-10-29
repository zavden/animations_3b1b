# ==============================================================================
# Scene:      AskWhy
# Source:     videos/_2023/clt/wordy_scenes.py (lines 706-718)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhy.py AskWhy -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskWhy(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(
            stds[1].says("Why?", mode="raise_left_hand")
        )
        self.play(
            morty.change("tease"),
            self.change_students("pondering", "raise_left_hand", "confused", look_at=morty.get_top() + 3 * UP)
        )
        self.wait(8)
