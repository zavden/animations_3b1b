# ==============================================================================
# Scene:      HoldUpExample
# Source:     videos/_2024/transformers/supplements.py (lines 638-646)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpExample.py HoldUpExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HoldUpExample(TeacherStudentsScene):
    def construct(self):
        self.background.set_fill(opacity=0.0)
        self.teacher.body.insert_n_curves(100)
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("happy", "hooray", "well", look_at=4 * UR)
        )
        self.wait(5)
