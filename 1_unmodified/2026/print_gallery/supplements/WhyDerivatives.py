# ==============================================================================
# Scene:      WhyDerivatives
# Source:     videos/_2026/print_gallery/supplements.py (lines 403-412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyDerivatives.py WhyDerivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyDerivatives(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(
            morty.change("well"),
            self.change_students("pondering", "hesitant", "guilty", look_at=self.screen)
        )
        self.wait(5)
