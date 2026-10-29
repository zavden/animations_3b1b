# ==============================================================================
# Scene:      HalfAsPowerful
# Source:     videos/_2020/hamming.py (lines 3505-3517)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HalfAsPowerful.py HalfAsPowerful -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HalfAsPowerful(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Shouldn't that be\\\\only half as good?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "happy"]
        )
        self.play_student_changes(
            "pondering", "pondering", look_at=self.screen,
            added_anims=[self.teacher.change, "tease"]
        )
        self.look_at(self.screen)
        self.wait(8)
