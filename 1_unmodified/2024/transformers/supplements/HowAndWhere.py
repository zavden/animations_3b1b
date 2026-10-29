# ==============================================================================
# Scene:      HowAndWhere
# Source:     videos/_2024/transformers/supplements.py (lines 1345-1357)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowAndWhere.py HowAndWhere -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HowAndWhere(TeacherStudentsScene):
    def construct(self):
        # Test
        self.remove(self.background)
        self.play(
            self.students[1].says("How?", mode="raise_left_hand", look_at=self.screen),
            self.teacher.change("tease"),
            self.students[2].change("pondering", look_at=self.screen),
        )
        self.play(
            self.students[0].says("Where?", mode="maybe", look_at=self.screen),
        )
        self.wait(3)
