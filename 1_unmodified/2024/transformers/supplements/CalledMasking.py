# ==============================================================================
# Scene:      CalledMasking
# Source:     videos/_2024/transformers/supplements.py (lines 1059-1067)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CalledMasking.py CalledMasking -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CalledMasking(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says(TexText(R"This is called\\``masking''")),
            self.change_students(
                "pondering", "confused", "erm", look_at=self.screen,
            )
        )
        self.wait(5)
