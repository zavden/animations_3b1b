# ==============================================================================
# Scene:      ReferenceHomework
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 418-429)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceHomework.py ReferenceHomework -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReferenceHomework(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("tease", "pondering", "thinking", look_at=self.screen)
        )
        self.wait(3)
        self.play(morty.change("tease"))
        self.play(self.change_students("pondering", "hesitant", "pondering", look_at=self.screen))
        self.wait(4)
