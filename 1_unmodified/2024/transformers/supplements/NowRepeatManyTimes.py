# ==============================================================================
# Scene:      NowRepeatManyTimes
# Source:     videos/_2024/transformers/supplements.py (lines 1229-1240)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NowRepeatManyTimes.py NowRepeatManyTimes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NowRepeatManyTimes(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.change_students("pondering", "pondering", "pondering", look_at=self.screen),
        )
        self.wait()
        self.play(
            self.teacher.says("Now do that about\n10,000 times"),
            self.change_students("droopy", "erm", "well", look_at=self.teacher.eyes)
        )
        self.wait(5)
