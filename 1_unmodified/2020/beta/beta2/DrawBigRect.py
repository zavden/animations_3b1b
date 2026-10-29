# ==============================================================================
# Scene:      DrawBigRect
# Source:     videos/_2020/beta/beta2.py (lines 2026-2049)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawBigRect.py DrawBigRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DrawBigRect(Scene):
    def construct(self):
        rect = Rectangle(width=7, height=2.5)
        rect.set_stroke(RED, 5)
        rect.to_edge(RIGHT)

        words = OldTexText("Not how to\\\\think about it")
        words.set_color(RED)
        words.align_to(rect, LEFT)
        words.to_edge(UP)

        arrow = Arrow(
            words.get_bottom(),
            rect.get_top(),
            buff=0.25,
            color=RED,
        )

        self.play(ShowCreation(rect))
        self.play(
            FadeInFromDown(words),
            GrowArrow(arrow),
        )
        self.wait()
