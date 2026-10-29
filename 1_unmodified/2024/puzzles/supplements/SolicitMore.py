# ==============================================================================
# Scene:      SolicitMore
# Source:     videos/_2024/puzzles/supplements.py (lines 300-326)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolicitMore.py SolicitMore -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SolicitMore(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        self.play(
            morty.says("Any other\nexamples?"),
            self.change_students("pondering", "pondering", "thinking")
        )
        self.wait(2)
        self.play(
            morty.debubble(mode='tease'),
            self.students[0].says("Monge's theorem!", mode="hooray"),
            self.students[1].animate.look_at(self.students[0].eyes),
            self.students[2].animate.look_at(self.students[0].eyes),
        )
        self.wait(4)

        # Point out a problem
        self.play(self.students[0].debubble(mode="pondering", look_at=self.screen))
        self.look_at(self.screen)
        self.wait(3)

        self.play(
            self.students[2].says("Hang on, that\ndoesn't work...", mode="sassy", look_at=self.screen, bubble_direction=LEFT),
            morty.change("guilty"),
        )
        self.wait(5)
