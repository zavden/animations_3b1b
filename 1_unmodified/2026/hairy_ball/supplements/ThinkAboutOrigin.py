# ==============================================================================
# Scene:      ThinkAboutOrigin
# Source:     videos/_2026/hairy_ball/supplements.py (lines 667-674)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkAboutOrigin.py ThinkAboutOrigin -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThinkAboutOrigin(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.play(
            morty.says(Text("Think about why\ncrossing the origin\nis significant", font_size=36)),
            self.change_students('thinking', 'tease', 'pondering', look_at=self.screen)
        )
        self.wait(5)
