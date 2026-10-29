# ==============================================================================
# Scene:      ImSorryWhat
# Source:     videos/_2020/monster.py (lines 4097-4107)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImSorryWhat.py ImSorryWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ImSorryWhat(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "I'm sorry, what?!",
            target_mode="sassy",
            look_at=self.screen,
        )
        self.play_student_changes("angry", "maybe", "sassy", look_at=self.screen)
        self.wait(3)
        self.play_student_changes("pleading", "confused", "erm", look_at=self.screen)
        self.wait(5)
