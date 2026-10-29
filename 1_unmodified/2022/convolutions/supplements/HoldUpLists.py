# ==============================================================================
# Scene:      HoldUpLists
# Source:     videos/_2022/convolutions/supplements.py (lines 5-18)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpLists.py HoldUpLists -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HoldUpLists(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.play(
            self.teacher.change("raise_right_hand", look_at=self.screen),
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen),
        )
        self.wait()
        self.play(
            self.change_students("thinking", "thinking", "pondering", look_at=3 * UR),
            self.teacher.change("raise_left_hand", look_at=3 * UR)
        )
        self.wait(2)
        self.play(LaggedStartMap(FadeOut, self.pi_creatures, shift=2 * DOWN))
