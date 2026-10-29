# ==============================================================================
# Scene:      ReactToDefiningProperty
# Source:     videos/_2023/gauss_int/supplements.py (lines 995-1031)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToDefiningProperty.py ReactToDefiningProperty -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReactToDefiningProperty(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)
        self.play(
            morty.change("raise_right_hand"),
            self.change_students("sassy", "hesitant", "erm", look_at=self.screen),
        )
        self.play(
            self.change_students("erm", "sassy", "hesitant", look_at=self.screen),
        )
        self.wait(2)

        # Ask
        self.play(LaggedStart(
            stds[1].says("But that assumes \n we're in 2D", mode="angry"),
            stds[0].change("sassy"),
            stds[2].animate.look_at(morty),
            morty.change("guilty"),
            lag_ratio=0.2
        ))
        self.wait(3)
        self.play(LaggedStart(
            stds[1].debubble(mode="sassy"),
            stds[2].says("What about\nthe Central Limit Theorem?"),
            stds[0].change("hesitant"),
            morty.change("hesitant"),
        ))
        self.wait(3)
        self.play(morty.change("tease", self.screen))
        self.wait()
        self.play(
            stds[0].change("pondering", self.screen),
            stds[1].change("pondering", self.screen),
        )
        self.wait(3)
