# ==============================================================================
# Scene:      IsntThatOvercomplicated
# Source:     videos/_2023/convolutions2/supplements.py (lines 213-244)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsntThatOvercomplicated.py IsntThatOvercomplicated -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IsntThatOvercomplicated(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        # Show
        self.play(
            stds[0].change("erm", self.screen),
            stds[2].change("confused", self.screen),
            stds[1].says(
                "Isn't that...a little\nover-complicated?",
                mode="angry",
                bubble_config=dict(width=7, height=4),
            ),
            morty.change("shruggie")
        )
        self.wait(2)
        self.play(morty.change("guilty"))
        self.wait()
        self.play(
            morty.says("It's fun!", mode="hooray", bubble_config=dict(width=2, height=1.5)),
            stds[1].debubble()
        )
        self.play(self.change_students("hesitant", "tease", "pondering", look_at=self.screen))
        self.wait(3)

        self.play(
            morty.debubble(mode="raise_right_hand"),
            self.change_students("pondering", "erm", "pondering", look_at=self.screen)
        )
        self.wait(5)
