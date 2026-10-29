# ==============================================================================
# Scene:      SeaOfNumbersUnderlay
# Source:     videos/_2024/transformers/supplements.py (lines 535-570)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeaOfNumbersUnderlay.py SeaOfNumbersUnderlay -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SeaOfNumbersUnderlay(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        self.play(
            morty.change("pleading"),
            self.change_students("surprised", "horrified", "droopy")
        )
        self.look_at(3 * LEFT + 2 *  UP)
        self.look_at(3 * RIGHT + 2 * UP)
        self.look_at(3 * LEFT + 2 * UP)

        self.play(
            morty.change("raise_right_hand", self.screen),
            self.change_students("hesitant", "pondering", "maybe", look_at=self.screen)
        )
        self.wait(2)
        self.play(self.change_students("erm", "pondering", "confused", look_at=self.screen))
        self.wait(2)

        self.look_at(5 * RIGHT + 2 * UP)
        self.play(self.change_students("hesitant", "pondering", "hesitant", look_at=5 * RIGHT + 2 * UP))
        self.wait(3)
        self.play(
            morty.change("well"),
            self.change_students("pondering", "pondering", "erm", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            morty.change("raise_left_hand", look_at=5 * RIGHT + 3 * UP),
            self.change_students("tease", "thinking", "pondering", look_at=5 * RIGHT + 3 * UP)
        )
        self.wait(8)
