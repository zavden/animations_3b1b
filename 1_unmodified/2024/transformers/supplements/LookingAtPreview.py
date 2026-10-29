# ==============================================================================
# Scene:      LookingAtPreview
# Source:     videos/_2024/transformers/supplements.py (lines 1434-1449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookingAtPreview.py LookingAtPreview -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LookingAtPreview(TeacherStudentsScene):
    def construct(self):
        # Test
        bubble = ThoughtBubble(filler_shape=(5, 2.5))
        bubble.flip()
        bubble.pin_to(self.students[2])
        bubble.to_edge(LEFT)
        self.play(
            self.teacher.change("raise_right_hand"),
            self.change_students("pondering", "confused", "pondering", look_at=bubble),
        )
        self.play(FadeIn(bubble, lag_ratio=0.1))
        self.play(self.teacher.change("tease"))
        self.wait(2)
        self.play(self.change_students("erm", "pondering", "thinking", look_at=bubble))
        self.wait(3)
