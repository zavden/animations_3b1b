# ==============================================================================
# Scene:      ConfusionAtScreen
# Source:     videos/_2024/transformers/supplements.py (lines 624-635)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConfusionAtScreen.py ConfusionAtScreen -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ConfusionAtScreen(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.change("well"),
            self.change_students("maybe", "confused", "concentrating", look_at=self.screen)
        )
        self.wait(2)
        self.play(
            self.teacher.change("tease"),
            self.change_students("hesitant", "plain", "erm", look_at=self.teacher.eyes)
        )
        self.wait(3)
