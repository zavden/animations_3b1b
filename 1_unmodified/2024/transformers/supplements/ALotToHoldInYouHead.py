# ==============================================================================
# Scene:      ALotToHoldInYouHead
# Source:     videos/_2024/transformers/supplements.py (lines 1243-1249)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ALotToHoldInYouHead.py ALotToHoldInYouHead -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ALotToHoldInYouHead(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("It's a lot to\nhold in your head!", mode="surprised"),
            self.change_students("confused", "erm", "dejected", look_at=self.screen),
        )
        self.wait(5)
