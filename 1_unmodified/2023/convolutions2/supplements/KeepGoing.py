# ==============================================================================
# Scene:      KeepGoing
# Source:     videos/_2023/convolutions2/supplements.py (lines 465-476)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeepGoing.py KeepGoing -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class KeepGoing(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            stds[0].says("More\niterations!", mode="hooray", bubble_config=dict(width=4, height=2)),
            stds[1].change("tease", stds[0].eyes),
            stds[2].change("coin_flip_1", stds[0].eyes),
            morty.change("happy"),
            run_time=1
        )
        self.wait(5)
