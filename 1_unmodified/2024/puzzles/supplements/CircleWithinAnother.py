# ==============================================================================
# Scene:      CircleWithinAnother
# Source:     videos/_2024/puzzles/supplements.py (lines 274-284)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleWithinAnother.py CircleWithinAnother -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleWithinAnother(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(
            stds[2].says("What if one circle\nis inside another?", look_at=morty.eyes, bubble_direction=LEFT),
            morty.change("tease"),
            stds[1].change("pondering", self.screen),
            stds[0].change("pondering", self.screen),
        )
        self.wait(4)
