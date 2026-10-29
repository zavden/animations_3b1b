# ==============================================================================
# Scene:      ConfusionAtPresmises
# Source:     videos/_2025/grover/qc_supplements.py (lines 537-550)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusionAtPresmises.py ConfusionAtPresmises -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfusionAtPresmises(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            morty.change('guilty'),
            stds[2].says("Okay...\nbut why?", mode="sassy", bubble_direction=LEFT),
            stds[1].change("confused", self.screen),
            stds[0].change("maybe", self.screen),
        )
        self.wait(2)
        self.play(self.change_students("confused", "erm", "maybe", look_at=self.screen))
        self.wait(3)
