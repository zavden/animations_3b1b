# ==============================================================================
# Scene:      HowDoYouApproachThat
# Source:     videos/_2023/gauss_int/supplements.py (lines 835-850)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowDoYouApproachThat.py HowDoYouApproachThat -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HowDoYouApproachThat(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        self.remove(self.background)
        self.play(
            stds[0].says("How do you \n approach that?", mode="raise_left_hand"),
            stds[1].change("maybe", look_at=3 * UP),
            stds[2].change("erm", look_at=3 * UP),
            self.teacher.change("tease")
        )
        self.wait()
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("confused", "confused", "pondering", look_at=3 * UP)
        )
        self.wait(3)
