# ==============================================================================
# Scene:      HoldUpImageProcessing
# Source:     videos/_2022/convolutions/supplements.py (lines 162-170)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpImageProcessing.py HoldUpImageProcessing -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HoldUpImageProcessing(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("pleading", "hesitant", "horrified", look_at=2 * UP)
        )
        self.wait(2)
        self.play(self.change_students("pondering", "thinking", "pondering", look_at=2 * UP))
        self.wait(6)
