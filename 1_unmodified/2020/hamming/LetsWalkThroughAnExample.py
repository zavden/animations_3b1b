# ==============================================================================
# Scene:      LetsWalkThroughAnExample
# Source:     videos/_2020/hamming.py (lines 4233-4247)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsWalkThroughAnExample.py LetsWalkThroughAnExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LetsWalkThroughAnExample(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Can we walk through\\\\a full example?",
            index=1,
            added_anims=[self.teacher.change, "happy"]
        )
        self.play_student_changes("hooray", None, "hooray")
        self.wait(5)
        self.teacher_says(
            "But of\\\\course!",
            target_mode="tease"
        )
        self.play_student_changes("happy", "coin_flip_1", "happy")
        self.wait(4)
