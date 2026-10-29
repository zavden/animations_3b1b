# ==============================================================================
# Scene:      RefreshersNeverHurt
# Source:     videos/_2024/transformers/supplements.py (lines 1452-1463)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RefreshersNeverHurt.py RefreshersNeverHurt -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RefreshersNeverHurt(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.change_students("confused", "horrified", "sad", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            self.teacher.says(TexText(R"Let's do a\\quick refresher"), mode="tease"),
            self.change_students("pondering", "hesitant", "erm", look_at=self.teacher.eyes)
        )
        self.wait(3)
