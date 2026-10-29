# ==============================================================================
# Scene:      ThatsOnMe
# Source:     videos/_2025/grover/clarification.py (lines 733-742)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatsOnMe.py ThatsOnMe -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThatsOnMe(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.play(
            morty.says("That's on me", mode="guilty"),
            self.change_students("pondering", "well", "hesitant", look_at=self.screen),
        )
        self.wait(3)
