# ==============================================================================
# Scene:      FeelsLikeATrick
# Source:     videos/_2023/gauss_int/supplements.py (lines 675-698)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeelsLikeATrick.py FeelsLikeATrick -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FeelsLikeATrick(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            Text("This feels \n like a trick"),
            Text("How could you have \n discovered this?"),
        )
        words.to_corner(UL)
        screen = ScreenRectangle(height=5)
        screen.to_corner(DR)

        arrows = VGroup(*(
            Arrow(word.get_right(), screen.get_top(), path_arc=-0.3 * PI)
            for word in words
        ))

        self.play(Write(words[0], run_time=1), ShowCreation(arrows[0]))
        self.wait(2)
        self.play(
            FadeOut(words[0], UP),
            FadeIn(words[1], UP),
            Transform(*arrows),
        )
        self.wait(2)
