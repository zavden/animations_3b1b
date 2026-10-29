# ==============================================================================
# Scene:      ThinkAboutMovingAverages
# Source:     videos/_2022/borwein/supplements.py (lines 350-362)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkAboutMovingAverages.py ThinkAboutMovingAverages -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThinkAboutMovingAverages(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        self.play(
            morty.change("raise_right_hand", self.screen),
            self.change_students("pondering", "thinking", "happy", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            morty.says("Think about\nmoving averages"),
        )
        self.play(self.change_students(*3 * ["pondering"]))
        self.wait(3)
