# ==============================================================================
# Scene:      ThinkDifferently
# Source:     videos/_2022/convolutions/supplements.py (lines 316-325)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkDifferently.py ThinkDifferently -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThinkDifferently(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("pondering", "confused", "thinking", look_at=self.screen),
        )
        self.wait()
        self.play(self.teacher.change("tease"))
        self.play(self.change_students("thinking", "pondering", "tease", look_at=self.screen))
        self.wait(4)
