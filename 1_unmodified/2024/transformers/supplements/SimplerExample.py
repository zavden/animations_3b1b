# ==============================================================================
# Scene:      SimplerExample
# Source:     videos/_2024/transformers/supplements.py (lines 965-975)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplerExample.py SimplerExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimplerExample(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.change_students("pondering", "thinking", "pondering", look_at=self.screen)
        )
        self.play(
            self.teacher.says("Take a simpler\nexample"),
            self.change_students("pondering", look_at=self.teacher.eyes)
        )
        self.play(self.change_students("thinking", "well", "tease"))
        self.wait(6)
