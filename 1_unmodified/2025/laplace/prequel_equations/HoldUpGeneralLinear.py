# ==============================================================================
# Scene:      HoldUpGeneralLinear
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1396-1411)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpGeneralLinear.py HoldUpGeneralLinear -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldUpGeneralLinear(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(500)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("pondering", "thinking", "tease", look_at=3 * UR)
        )
        self.wait()
        self.play(
            morty.change("sassy", look_at=3 * UR),
            self.change_students("hesitant", "erm", "maybe")
        )
        self.wait(5)
