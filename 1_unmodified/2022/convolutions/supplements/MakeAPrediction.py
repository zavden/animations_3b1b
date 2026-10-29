# ==============================================================================
# Scene:      MakeAPrediction
# Source:     videos/_2022/convolutions/supplements.py (lines 306-313)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MakeAPrediction.py MakeAPrediction -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MakeAPrediction(TeacherStudentsScene):
    def construct(self):
        # Blah
        self.teacher_says("Try thinking\nthrough what\nwill happen")
        self.play(self.change_students("pondering", "confused", "thinking", look_at=self.screen))
        self.wait()
        self.play(self.teacher.change("tease"))
        self.wait(4)
