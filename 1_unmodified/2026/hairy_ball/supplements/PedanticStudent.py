# ==============================================================================
# Scene:      PedanticStudent
# Source:     videos/_2026/hairy_ball/supplements.py (lines 195-214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PedanticStudent.py PedanticStudent -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PedanticStudent(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change('raise_right_hand'),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen)
        )
        self.wait()
        self.play(LaggedStart(
            stds[2].says("But atmosphere\nis 3D!", mode="angry", look_at=morty.eyes, bubble_direction=LEFT),
            morty.change("guilty"),
            stds[0].change("hesitant", look_at=stds[2].eyes),
            stds[1].change("hesitant", look_at=stds[2].eyes),
        ))
        self.wait(2)
        self.look_at(self.screen)
        self.wait(3)
