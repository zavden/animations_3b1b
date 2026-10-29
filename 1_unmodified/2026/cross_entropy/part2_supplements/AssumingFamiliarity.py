# ==============================================================================
# Scene:      AssumingFamiliarity
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 79-96)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AssumingFamiliarity.py AssumingFamiliarity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AssumingFamiliarity(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        morty.body.insert_n_curves(500)

        self.play(
            morty.change("raise_right_hand", 3 * UP),
            self.change_students("tease", "well", "happy", look_at=3 * UP)
        )
        self.wait()
        self.play(self.change_students("tease", "well", "thinking", look_at=3 * UP), run_time=2)
        self.wait(2)
        self.play(
            morty.says("Quick recaps\nnever hurt"),
            self.change_students("hesitant", "tease", "well")
        )
        self.wait(3)
