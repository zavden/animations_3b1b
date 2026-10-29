# ==============================================================================
# Scene:      WhoOrderedMoreDimensions
# Source:     videos/_2023/gauss_int/supplements.py (lines 495-525)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoOrderedMoreDimensions.py WhoOrderedMoreDimensions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhoOrderedMoreDimensions(TeacherStudentsScene):
    def construct(self):
        # Ask
        stds = self.students
        morty = self.teacher
        self.remove(self.background)
        self.play(LaggedStart(
            stds[0].says("Why", mode="raise_left_hand"),
            stds[2].change("hesitant", look_at=morty),
            morty.change("tease"),
            stds[1].says(
                "Who ordered \n another dimension?",
                mode="confused",
                bubble_direction=LEFT,
            ),
            lag_ratio=0.2,
        ))
        self.wait(3)
        self.play(LaggedStart(
            morty.says("Well, watch\nwhat happens", mode="shruggie"),
            stds[0].debubble(mode="hesitant"),
            stds[1].debubble(mode="maybe"),
            stds[2].change("sassy"),
        ))
        self.wait(3)
        self.play(
            FadeOut(VGroup(morty.bubble, morty.bubble.content)),
            morty.says("It never hurts to\ntry similar problems"),
            self.change_students("pondering", "erm", "pondering", look_at=self.screen)
        )
        self.wait(3)
