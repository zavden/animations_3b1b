# ==============================================================================
# Scene:      SorryWhat
# Source:     videos/_2023/gauss_int/supplements.py (lines 480-492)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SorryWhat.py SorryWhat -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SorryWhat(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.remove(self.background)
        self.play(LaggedStart(
            stds[1].says("Sorry, what?!", mode="angry"),
            stds[0].change("sassy", look_at=morty),
            stds[2].change("hesitant", look_at=morty),
            morty.change("tease"),
            lag_ratio=0.2,
        ))
        self.wait(3)
