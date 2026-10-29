# ==============================================================================
# Scene:      WeCanBeMoreElegant
# Source:     videos/_2023/clt/wordy_scenes.py (lines 782-790)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeCanBeMoreElegant.py WeCanBeMoreElegant -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WeCanBeMoreElegant(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("We can be\nmore elegant"),
            self.change_students("pondering", "confused", "sassy", look_at=self.screen)
        )
        self.wait()
        self.play(self.students[2].change("tease", look_at=self.teacher.eyes))
        self.wait(3)
