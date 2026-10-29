# ==============================================================================
# Scene:      IsThisUseful
# Source:     videos/_2025/grover/clarification.py (lines 1317-1334)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsThisUseful.py IsThisUseful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsThisUseful(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("hesitant", self.screen),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen)
        )
        self.wait(4)
        self.play(
            stds[1].says("Is this...useful?", mode="confused"),
            stds[0].change("hesitant", look_at=stds[1].eyes),
            stds[2].change("well", look_at=stds[1].eyes),
            morty.change("guilty", look_at=stds[1].eyes),
        )
        self.wait(4)
