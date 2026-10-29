# ==============================================================================
# Scene:      AskAboutTopology
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 757-777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutTopology.py AskAboutTopology -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutTopology(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students

        self.play(
            stds[0].says("What is a\ntopological space?", "raise_left_hand"),
            stds[1].change("pondering", stds[0].eyes),
            stds[2].change("pondering", stds[0].eyes),
            morty.change("tease"),
        )
        self.wait(2)
        self.play(
            stds[1].animate.look_at(stds[2].eyes),
            stds[2].says("What is\ntopology?", "maybe", look_at=morty.eyes, bubble_direction=LEFT)
        )
        self.wait()
        self.play(morty.change("guilty"))
        self.play(stds[0].change('confused'))
        self.play(morty.change("hesitant"))
        self.wait(4)
