# ==============================================================================
# Scene:      ReferenceMeanAndSD
# Source:     videos/_2023/clt/wordy_scenes.py (lines 665-703)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceMeanAndSD.py ReferenceMeanAndSD -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReferenceMeanAndSD(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(
            morty.says("We must put\nnumbers to those!", mode="surprised"),
            self.change_students("hesitant", "concerned_musician", "tease")
        )
        self.look_at(self.screen)
        self.wait(3)

        # Mean and sd
        kw = dict(t2c={R"\mu": PINK, R"\sigma": RED}, font_size=42)
        terms = VGroup(
            Tex(R"\text{Mean: } \mu = E[X]", **kw),
            Tex(R"\text{Std dev: } \sigma = \sqrt{E[(X - \mu)^2]}", **kw),
        )

        terms.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        terms.next_to(morty, UP, LARGE_BUFF)
        terms.to_edge(RIGHT)

        self.play(
            morty.debubble(mode="raise_right_hand", look_at=terms),
            self.change_students("pondering", "hesitant", "happy", look_at=terms),
            LaggedStartMap(FadeIn, terms, shift=UP, lag_ratio=0.5)
        )
        self.wait(3)
        self.play(
           stds[2].says("Great!", mode="hooray"),
           morty.change("happy")
        )
        self.play(
            stds[0].says("Wait, can you\nremind me?", mode="guilty"),
            morty.change("tease")
        )
        self.wait(5)
