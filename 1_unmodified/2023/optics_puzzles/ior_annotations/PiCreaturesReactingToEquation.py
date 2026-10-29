# ==============================================================================
# Scene:      PiCreaturesReactingToEquation
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1031-1049)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCreaturesReactingToEquation.py PiCreaturesReactingToEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiCreaturesReactingToEquation(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students
        self.remove(self.background)
        point = morty.get_corner(UL) + 2 * UP + LEFT
        self.play(
            morty.change("raise_left_hand", point),
            self.change_students("pondering", "thinking", "erm", look_at=point)
        )
        self.wait(3)
        self.play(self.change_students("thinking", "pondering", "pondering", look_at=point))
        self.wait(3)
        self.play(
            morty.says("Oh hey, it depends\non the frequency!", mode="hooray"),
            self.change_students("happy", "tease", "thinking", look_at=point)
        )
        self.wait(4)
