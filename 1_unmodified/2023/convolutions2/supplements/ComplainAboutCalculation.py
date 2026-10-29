# ==============================================================================
# Scene:      ComplainAboutCalculation
# Source:     videos/_2023/convolutions2/supplements.py (lines 707-759)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplainAboutCalculation.py ComplainAboutCalculation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ComplainAboutCalculation(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        # Complain
        self.play(
            stds[2].says("But do these help\nwith actual computations?", mode="sassy"),
            morty.change("guilty")
        )
        self.play(self.change_students("erm", "frustrated", look_at=self.screen))
        self.wait(3)

        # Opening quiz
        self.play(
            stds[1].says("Like, the opening quiz?", mode="raise_right_hand"),
            stds[2].debubble(mode="hesitant", look_at=self.screen),
            stds[0].change("pondering"),
        )
        self.play(morty.change("well"))
        self.look_at(self.screen)
        self.wait(3)

        # React to ordinary approach
        self.play(
            morty.change("raise_left_hand", 4 * UR),
            stds[0].animate.look_at(3 * UR),
            stds[1].debubble(mode="pondering", look_at=3 * UR),
            stds[2].change("pondering", 3 * UR),
            self.frame.animate.set_height(12, about_edge=DOWN)
        )
        self.wait(4)
        self.play(
            morty.change("raise_right_hand", look_at=self.screen),
            self.change_students("hesitant", "pondering", "guilty", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            self.change_students("horrified", "pleading", "concentrating", look_at=2 * UR)
        )
        self.play(morty.change("tease"))
        self.wait(4)
        self.play(
            morty.change("coin_flip_2"),
            self.change_students("guilty", "guilty", "sick", look_at=2 * UR)
        )
        self.wait()
        self.play(
            morty.change("hooray"),
            self.change_students("well", "tease", "happy", look_at=morty.eyes)
        )
        self.wait(4)
