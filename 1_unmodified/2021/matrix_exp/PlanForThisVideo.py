# ==============================================================================
# Scene:      PlanForThisVideo
# Source:     videos/_2021/matrix_exp.py (lines 281-299)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PlanForThisVideo.py PlanForThisVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PlanForThisVideo(TeacherStudentsScene):
    def construct(self):
        s0, s1, s2 = self.students
        self.play(
            PiCreatureSays(s0, OldTexText("But what\\\\is $e^{M}$?"), target_mode="raise_left_hand"),
            s1.change("erm", UL),
            s2.change("pondering", UL),
        )
        self.wait()
        s0.bubble = None
        self.play(
            PiCreatureSays(
                s2, OldTexText("And who cares?"), target_mode="sassy",
                bubble_config={"direction": LEFT},
            ),
            s1.change("hesitant", UL),
            self.teacher.change("guilty")
        )
        self.wait(3)
