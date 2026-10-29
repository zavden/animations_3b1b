# ==============================================================================
# Scene:      StareAtPicture
# Source:     videos/_2025/grover/qc_supplements.py (lines 881-897)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StareAtPicture.py StareAtPicture -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StareAtPicture(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand", self.screen),
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen),
        )
        self.wait()
        self.play(
            morty.change("speaking", look_at=self.students),
            self.change_students("tease", "well", "coin_flip_2")
        )
        self.wait(5)
