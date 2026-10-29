# ==============================================================================
# Scene:      CanWeSeeAnExample
# Source:     videos/_2023/convolutions2/supplements.py (lines 293-314)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CanWeSeeAnExample.py CanWeSeeAnExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CanWeSeeAnExample(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.remove(self.background)
        self.play(
            stds[1].says("Can we see\nan example?", mode="raise_left_hand"),
        )
        self.play(
            stds[0].change("confused", self.screen),
            stds[2].change("maybe", self.screen),
            morty.change("happy"),
        )
        self.wait(2)
        self.play(
            morty.change("raise_right_hand", 3 * UP),
            self.change_students("pondering", None, "pondering", look_at=3 * UP),
            stds[1].debubble()
        )
        self.look_at(3 * UP)
        self.wait(5)
