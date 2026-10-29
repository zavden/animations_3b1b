# ==============================================================================
# Scene:      AskAboutCrossAttention
# Source:     videos/_2024/transformers/supplements.py (lines 1096-1105)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutCrossAttention.py AskAboutCrossAttention -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutCrossAttention(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        self.play(
            stds[0].change("hesitant", look_at=stds[1].eyes),
            stds[1].says("What about\ncross-attention?", bubble_config=dict(buff=0.5), mode="raise_left_hand"),
            stds[2].change("pondering", look_at=stds[1].eyes),
            self.teacher.change("well", look_at=stds[1].eyes)
        )
        self.wait(5)
