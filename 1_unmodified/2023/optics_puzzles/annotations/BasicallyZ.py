# ==============================================================================
# Scene:      BasicallyZ
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 540-552)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BasicallyZ.py BasicallyZ -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class BasicallyZ(InteractiveScene):
    def construct(self):
        rect = Rectangle(6.0, 2.0)
        rect.set_stroke(YELLOW, 2)
        rect.set_fill(YELLOW, 0.2)
        rect.to_edge(RIGHT, buff=0.25)
        words = Text("Essentially parallel\nto the z-axis")
        words.next_to(rect, UP)
        self.play(
            FadeIn(words, 0.25 * UP),
            FadeIn(rect)
        )
        self.wait()
