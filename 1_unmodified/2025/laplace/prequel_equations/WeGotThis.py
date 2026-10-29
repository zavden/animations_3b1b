# ==============================================================================
# Scene:      WeGotThis
# Source:     videos/_2025/laplace/prequel_equations.py (lines 140-152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeGotThis.py WeGotThis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WeGotThis(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        self.play(
            self.change_students("coin_flip_2", "tease", "hooray", look_at=3 * UP),
            morty.change("tease")
        )
        self.wait()
        self.play(
            self.change_students("tease", "happy", "well", look_at=morty.eyes)
        )
        self.wait(3)
