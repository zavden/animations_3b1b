# ==============================================================================
# Scene:      WhatAboutTwoBitDetection
# Source:     videos/_2020/hamming.py (lines 5818-5831)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatAboutTwoBitDetection.py WhatAboutTwoBitDetection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatAboutTwoBitDetection(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "What about\\\\detecting\\\\two bit errors?"
        )
        self.play(
            self.change_students("angry", "maybe", "raise_left_hand"),
            self.teacher.change, "guilty",
        )
        self.look_at(self.screen)
        self.wait(4)
        self.play(self.teacher.change, "happy")
        self.play_student_changes("confused", "erm", "pondering")
        self.wait(3)
