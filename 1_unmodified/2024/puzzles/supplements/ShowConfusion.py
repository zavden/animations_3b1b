# ==============================================================================
# Scene:      ShowConfusion
# Source:     videos/_2024/puzzles/supplements.py (lines 549-564)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowConfusion.py ShowConfusion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowConfusion(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        self.play(
            morty.change("guilty"),
            self.change_students("concentrating", "droopy", "sad", look_at=self.screen)
        )
        self.wait(3)
        self.play(self.change_students("maybe", "tired", "concentrating", look_at=self.screen))
        self.wait(3)
        self.play(
            morty.says("A little mental gymnastics\nkeeps your mind flexible", mode="tease"),
            self.change_students("hesitant", "erm", "thinking", look_at=morty.eyes)
        )
        self.wait(5)
