# ==============================================================================
# Scene:      PauseAndPonder
# Source:     videos/_2023/convolutions2/supplements.py (lines 172-183)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PauseAndPonder.py PauseAndPonder -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PauseAndPonder(TeacherStudentsScene):
    def construct(self):
        self.play(self.teacher.says("Pause and\nponder!", mode="hooray", run_time=1))
        self.play(self.change_students("thinking", "pondering", "pondering", look_at=self.screen))
        self.wait(5)

        # State goal
        self.play(
            self.teacher.debubble(mode="raise_right_hand", look_at=3 * UP),
            self.change_students("tease", "thinking", "awe", look_at=3 * UP)
        )
        self.wait(8)
