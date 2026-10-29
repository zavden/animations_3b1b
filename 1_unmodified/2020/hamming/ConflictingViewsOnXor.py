# ==============================================================================
# Scene:      ConflictingViewsOnXor
# Source:     videos/_2020/hamming.py (lines 5834-5852)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConflictingViewsOnXor.py ConflictingViewsOnXor -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConflictingViewsOnXor(TeacherStudentsScene):
    def construct(self):
        self.clear()
        self.add(self.pi_creatures)
        self.student_says(
            "Um...can you\\\\say that again?",
            target_mode="confused",
            index=2,
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("pondering", "pondering", look_at=self.screen)
        self.wait(2)
        self.student_says(
            "Why didn't you\\\\just use xors\\\\from the start?",
            target_mode="sassy",
            index=1,
        )
        self.look_at(self.students[1].bubble)
        self.wait(5)
