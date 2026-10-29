# ==============================================================================
# Scene:      IsThisUsefulToShare
# Source:     videos/_2024/transformers/chm.py (lines 32-42)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsThisUsefulToShare.py IsThisUsefulToShare -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IsThisUsefulToShare(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        self.play(
            morty.says("Do you find\nthis useful?"),
            self.change_students("pondering", "hesitant", "well", look_at=self.screen)
        )
        self.wait(3)
        self.play(self.change_students("thinking", "pondering", "tease"))
        self.wait(3)
