# ==============================================================================
# Scene:      RememberThat
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 256-262)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RememberThat.py RememberThat -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RememberThat(TeacherStudentsScene):
    def construct(self):
        self.play(self.teacher.says("Remember that"))
        self.play(
            self.change_students("pondering", "pondering", "thinking", look_at=self.screen)
        )
        self.wait(3)
