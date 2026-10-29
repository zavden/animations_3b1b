# ==============================================================================
# Scene:      Boring
# Source:     videos/_2022/convolutions/supplements.py (lines 192-202)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Boring.py Boring -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Boring(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(LaggedStart(
            self.students[2].says("Boring!", mode="dejected", look_at=self.teacher.eyes, bubble_direction=LEFT),
            self.teacher.change("hesitant"),
            self.students[0].change("hesitant", self.screen),
            self.students[1].change("guilty", self.screen),
            lag_ratio=0.25,
        ))
        self.wait(3)
