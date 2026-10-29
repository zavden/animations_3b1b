# ==============================================================================
# Scene:      TryADifferentInterpretation
# Source:     videos/_2025/laplace/main_supplements.py (lines 536-545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TryADifferentInterpretation.py TryADifferentInterpretation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TryADifferentInterpretation(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.play(
            morty.says("Let’s try an\nalternate\ninterpretation"),
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen)
        )
        self.wait(2)
        self.play(self.change_students("maybe", "pondering", "thinking", look_at=self.screen))
        self.wait(4)
