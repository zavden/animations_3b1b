# ==============================================================================
# Scene:      NormalName
# Source:     videos/_2023/clt/wordy_scenes.py (lines 23-66)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NormalName.py NormalName -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NormalName(InteractiveScene):
    def construct(self):
        # Names
        names = VGroup(
            Text("Normal distribution"),
            Text("Bell curve"),
            Text("Gaussian distribution"),
        )
        point = 2 * LEFT + 1.5 * UP
        names.next_to(point, UP)
        names.set_color(GREY_A)

        shift = 0.75 * UP
        names[0].scale(2, about_edge=DOWN)
        self.play(Write(names[0]), run_time=1)
        self.wait()
        self.play(
            names[0].animate.scale(0.5, about_edge=DOWN).shift(shift),
            FadeIn(names[1], shift=0.5 * shift),
        )
        self.wait()
        self.play(
            names[:2].animate.shift(shift),
            FadeIn(names[2], shift=0.5 * shift)
        )
        self.wait()

        # In a moment
        words = TexText("We'll unpack this in a bit", font_size=36)
        words.set_fill(GREY_A)
        words.next_to(point, UP)
        words.shift(0.5 * UL)
        arrow = Arrow(
            words.get_bottom() + LEFT, words.get_bottom() + DOWN,
            stroke_width=3, stroke_color=GREY_A,
        )

        self.play(LaggedStart(
            FadeOut(names[1:]),
            FadeIn(words, lag_ratio=0.1),
            ShowCreation(arrow),
            lag_ratio=0.25
        ))
        self.wait()
