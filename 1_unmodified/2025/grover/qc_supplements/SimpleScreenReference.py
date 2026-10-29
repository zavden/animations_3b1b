# ==============================================================================
# Scene:      SimpleScreenReference
# Source:     videos/_2025/grover/qc_supplements.py (lines 211-219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleScreenReference.py SimpleScreenReference -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleScreenReference(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher

        self.play(
            morty.change("hesitant"),
            self.change_students("erm", "concentrating", "sassy", look_at=self.screen)
        )
        self.wait(5)
