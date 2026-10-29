# ==============================================================================
# Scene:      MakeSomeAssumptions
# Source:     videos/_2024/transformers/supplements.py (lines 1593-1601)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MakeSomeAssumptions.py MakeSomeAssumptions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MakeSomeAssumptions(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("We need a\nfew assumptions"),
            self.change_students("pondering", "sassy", "tease", look_at=self.screen)
        )
        self.play(self.teacher.change("raise_right_hand"))
        self.wait(6)
