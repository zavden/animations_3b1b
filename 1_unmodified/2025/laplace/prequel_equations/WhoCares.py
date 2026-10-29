# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2025/laplace/prequel_equations.py (lines 116-129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        # Test
        self.remove(self.background)
        stds = self.students
        morty = self.teacher

        self.play(
            stds[2].says("Who cares?", mode="angry", look_at=3 * UP),
            morty.change("guilty", stds[2].eyes),
            stds[1].change("hesitant", 3 * UP),
            stds[0].change("erm", stds[2].eyes),
        )
        self.wait(3)
