# ==============================================================================
# Scene:      Lame
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 408-415)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Lame.py Lame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Lame(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.play(
            morty.says("Lame!", mode="angry"),
            self.change_students("guilty", "confused", "erm", look_at=self.screen)
        )
        self.wait(5)
