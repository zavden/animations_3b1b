# ==============================================================================
# Scene:      SetThemToZero
# Source:     videos/_2024/transformers/supplements.py (lines 1043-1056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SetThemToZero.py SetThemToZero -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SetThemToZero(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.students[0].says("Set them to 0?", mode="maybe"),
            self.students[1].change("pondering", look_at=self.screen),
            self.students[1].change("pondering", look_at=self.screen),

        )
        self.wait()
        self.play(
            self.teacher.says("Then they wouldn't\nbe normalized", mode="tease"),
        )
        self.wait(3)
