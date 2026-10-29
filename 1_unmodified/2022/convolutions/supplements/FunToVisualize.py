# ==============================================================================
# Scene:      FunToVisualize
# Source:     videos/_2022/convolutions/supplements.py (lines 21-28)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FunToVisualize.py FunToVisualize -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FunToVisualize(TeacherStudentsScene):
    def construct(self):
        # Test
        self.play(
            self.teacher.says("Boy are they fun\nto visualize!", mode="hooray"),
            self.change_students("tease", "happy", "well")
        )
        self.wait(3)
