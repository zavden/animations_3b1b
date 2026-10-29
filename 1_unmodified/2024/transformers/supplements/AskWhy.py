# ==============================================================================
# Scene:      AskWhy
# Source:     videos/_2024/transformers/supplements.py (lines 1690-1705)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhy.py AskWhy -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskWhy(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)

        # Test
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)
        self.play(
            self.teacher.change("guilty"),
            self.students[2].says(Text("Um, Why?", font_size=72), mode="maybe", look_at=self.screen),
            self.students[0].change("confused", self.screen),
            self.students[1].change("erm", self.screen),
        )
        self.wait()
        self.play(self.teacher.change("tease"))
        self.wait(2)
