# ==============================================================================
# Scene:      NothingWrongWithThat
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 357-376)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NothingWrongWithThat.py NothingWrongWithThat -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NothingWrongWithThat(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.remove(self.background)

        self.play(
            morty.says("There's nothing\nwrong with that!", mode="hooray"),
            self.change_students("awe", "horrified", "confused", look_at=self.screen),
        )
        self.wait(3)
        self.play(
            morty.debubble(mode="tease"),
            self.change_students("pondering", "plain", "well")
        )
        self.wait()
        self.play(
            morty.change("raise_right_hand", look_at=3 * UP),
            self.change_students("well", "pondering", "tease", look_at=3 * UR)
        )
        self.wait(10)
