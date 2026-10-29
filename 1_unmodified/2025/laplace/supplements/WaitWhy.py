# ==============================================================================
# Scene:      WaitWhy
# Source:     videos/_2025/laplace/supplements.py (lines 463-471)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaitWhy.py WaitWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WaitWhy(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.students[0].change("erm", self.screen),
            self.students[1].change("tease", self.screen),
            self.students[2].says("Wait, why?", "confused", look_at=self.screen, bubble_direction=LEFT),
        )
        self.wait(4)
