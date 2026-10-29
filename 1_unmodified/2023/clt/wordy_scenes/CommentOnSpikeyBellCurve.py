# ==============================================================================
# Scene:      CommentOnSpikeyBellCurve
# Source:     videos/_2023/clt/wordy_scenes.py (lines 622-644)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnSpikeyBellCurve.py CommentOnSpikeyBellCurve -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CommentOnSpikeyBellCurve(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        morty = self.teacher
        stds = self.students

        # Test
        self.play(
            morty.says("Kind of a\nbell curve", mode="shruggie"),
            self.change_students("erm", "hesitant", "hesitant", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            stds[1].says("Is it...supposed to\nlook like that?"),
            morty.debubble(),
        )
        self.look_at(self.screen)
        self.wait(2)
        self.play(
            stds[2].says("How many samples\nuntil we're sure?"),
            stds[1].debubble(),
        )
        self.wait(5)
