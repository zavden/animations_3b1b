# ==============================================================================
# Scene:      ButSpringsAreReal
# Source:     videos/_2025/laplace/prequel_equations.py (lines 903-914)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ButSpringsAreReal.py ButSpringsAreReal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ButSpringsAreReal(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            stds[0].change("maybe", self.screen),
            stds[1].says("But...springs are real", mode="confused", look_at=self.screen),
            stds[2].change("erm", self.screen),
            morty.change("tease", stds[2].eyes)
        )
        self.wait(4)
