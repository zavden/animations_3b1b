# ==============================================================================
# Scene:      ReferenceSAP
# Source:     videos/_2024/transformers/supplements.py (lines 2095-2121)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceSAP.py ReferenceSAP -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReferenceSAP(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.background.scale(2)
        self.frame.scale(1.25, about_edge=DR)

        # Test
        bubble = stds[0].get_bubble("How would you\ntest this?", bubble_type=SpeechBubble)
        bubble.shift(0.5 * LEFT)
        self.play(LaggedStart(
            FadeIn(bubble, lag_ratio=0.1),
            stds[0].change("raise_left_hand"),
            stds[1].change("confused"),
            stds[2].change("maybe"),
            morty.change("tease")
        ))
        self.wait(2)
        self.play(
            morty.says(TexText(R"There's nice\\research using\\Sparse Autoencoders"), mode="hooray")
        )
        self.play(
            self.change_students(None, "pondering", "erm", look_at=morty.bubble),
        )
        self.wait()
        self.look_at(self.screen)
        self.wait(5)
