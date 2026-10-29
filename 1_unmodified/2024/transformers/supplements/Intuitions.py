# ==============================================================================
# Scene:      Intuitions
# Source:     videos/_2024/transformers/supplements.py (lines 787-819)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Intuitions.py Intuitions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Intuitions(TeacherStudentsScene):
    def construct(self):
        # Add words
        words = VGroup(
            Text("Structure of Deep Learning"),
            Text("Word embeddings"),
            Text("Dot products"),
            Text("Softmax"),
        )
        words.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        words.move_to(self.hold_up_spot, DOWN)
        checks = VGroup(
            Checkmark(font_size=72).next_to(word, LEFT)
            for word in words
        )
        checks.set_color(GREEN)

        morty = self.teacher
        self.play(
            LaggedStartMap(FadeIn, words, shift=UP, lag_ratio=0.1),
            morty.change("raise_right_hand"),
            self.change_students("thinking", "pondering", "well", look_at=words),
            run_time=1,
        )
        self.play(
            LaggedStartMap(Write, checks, lag_ratio=0.25, stroke_color=GREEN),
        )
        for pi in self.students:
            pi.body.insert_n_curves(100)
        self.play(
            self.change_students("tease", "thinking", "well")
        )
        self.wait(4)
