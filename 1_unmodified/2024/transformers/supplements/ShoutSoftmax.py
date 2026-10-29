# ==============================================================================
# Scene:      ShoutSoftmax
# Source:     videos/_2024/transformers/supplements.py (lines 1024-1032)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShoutSoftmax.py ShoutSoftmax -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ShoutSoftmax(TeacherStudentsScene):
    def construct(self):
        self.play(LaggedStart(
            self.students[0].change("happy"),
            self.students[1].change("hooray"),
            self.students[2].says("Softmax!", mode="surprised", bubble_config=dict(buff=0.5, direction=LEFT)),
            self.teacher.change("well")
        ))
        self.wait(5)
