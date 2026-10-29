# ==============================================================================
# Scene:      WhatWasTheBug
# Source:     videos/_2022/wordle/footnote.py (lines 108-115)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatWasTheBug.py WhatWasTheBug -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatWasTheBug(TeacherStudentsScene):
    def construct(self):
        self.student_says("What as the bug?")
        self.play(
            self.change_students("raise_left_hand", "pondering", "raise_right_hand"),
            self.teacher.change("tired")
        )
        self.wait(3)
