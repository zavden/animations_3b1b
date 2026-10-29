# ==============================================================================
# Scene:      FailedPromises
# Source:     videos/_2020/med_test.py (lines 5484-5508)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FailedPromises.py FailedPromises -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FailedPromises(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Are you still doing\\\\``Probabilities\\\\of probabilities''?",
            bubble_config={
                "height": 3.5,
                "width": 4.5,
            },
            index=0,
            target_mode="sassy",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.students[0].bubble = None
        self.student_says(
            "And what about\\\\Differential equations?",
            bubble_config={
                "height": 3,
                "width": 4,
                "direction": LEFT,
            },
            index=2,
            target_mode="angry",
            added_anims=[self.students[1].change, "hesitant"],
        )
        self.wait(3)
