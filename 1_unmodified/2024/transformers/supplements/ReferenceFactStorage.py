# ==============================================================================
# Scene:      ReferenceFactStorage
# Source:     videos/_2024/transformers/supplements.py (lines 1401-1431)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceFactStorage.py ReferenceFactStorage -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReferenceFactStorage(TeacherStudentsScene):
    def construct(self):
        # Look at screen
        morty = self.teacher
        screen = self.screen
        self.play(
            morty.change("raise_right_hand", screen),
            self.change_students("pondering", "confused", "pondering", look_at=screen),
        )
        self.wait(4)

        # Hold up words
        words = Text("Store a fact", font_size=72)
        words.next_to(morty, UP, LARGE_BUFF).shift_onto_screen()

        self.play(
            morty.change("raise_left_hand"),
            FadeIn(words, UP),
            self.change_students("erm", "maybe", "sassy", look_at=morty.eyes),
        )
        self.look_at(self.screen)
        self.wait(3)
        self.play(morty.change("tease"))
        self.wait(2)

        # Relax
        self.play(
            FadeOut(words, DOWN),
            self.change_students("pondering", "tease", "happy", look_at=self.screen),
        )
        self.wait(3)
