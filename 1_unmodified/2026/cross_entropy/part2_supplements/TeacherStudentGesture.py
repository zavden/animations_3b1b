# ==============================================================================
# Scene:      TeacherStudentGesture
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 221-233)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TeacherStudentGesture.py TeacherStudentGesture -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TeacherStudentGesture(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        morty.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand", 3 * UP),
            self.change_students("pondering", "thinking", "pondering", look_at=3 * UP)
        )
        self.wait()
        self.play(morty.change("tease"))
        self.wait(5)
