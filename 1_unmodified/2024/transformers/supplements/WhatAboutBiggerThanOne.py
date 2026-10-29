# ==============================================================================
# Scene:      WhatAboutBiggerThanOne
# Source:     videos/_2024/transformers/supplements.py (lines 1660-1678)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAboutBiggerThanOne.py WhatAboutBiggerThanOne -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhatAboutBiggerThanOne(TeacherStudentsScene):
    def construct(self):
        # Test
        self.screen.set_x(0)
        self.play(
            self.students[0].change("pondering", self.screen),
            self.students[1].says("And if it's\nbigger than 1?", mode="sassy", bubble_direction=RIGHT),
            self.students[2].change("erm", self.screen),
            self.teacher.change("guilty"),
        )
        self.wait(2)
        self.play(
            # self.teacher.says("Don't worry\nabout it", mode="maybe")
            self.teacher.change("maybe")
        )
        self.play(
            self.change_students("hesitant", "sassy", "angry")
        )
        self.wait(3)
