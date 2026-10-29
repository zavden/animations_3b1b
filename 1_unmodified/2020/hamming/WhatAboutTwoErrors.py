# ==============================================================================
# Scene:      WhatAboutTwoErrors
# Source:     videos/_2020/hamming.py (lines 3520-3529)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAboutTwoErrors.py WhatAboutTwoErrors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAboutTwoErrors(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What about\\\\2 errors?",
        )
        self.play(self.teacher.change, "guilty")
        self.look_at(self.screen)
        self.play_student_changes("erm", "confused")
        self.look_at(self.screen)
        self.wait(4)
