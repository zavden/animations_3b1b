# ==============================================================================
# Scene:      OhLookAtTheTime
# Source:     videos/_2025/laplace/main_supplements.py (lines 765-783)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OhLookAtTheTime.py OhLookAtTheTime -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OhLookAtTheTime(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        morty.body.insert_n_curves(500)
        # Test
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("dejected", "tired", "pondering", look_at=3 * UP)
        )
        self.wait(3)
        self.play(
            morty.change("hesitant", 5 * UR),
        )
        self.play(self.change_students("tease", "well", "happy"))
        self.wait(3)
        self.play(morty.change("raise_left_hand", 5 * UR))
        self.wait(3)
