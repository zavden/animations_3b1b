# ==============================================================================
# Scene:      ThatWhichDoesntKillHeader
# Source:     videos/_2024/transformers/supplements.py (lines 1505-1518)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThatWhichDoesntKillHeader.py ThatWhichDoesntKillHeader -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThatWhichDoesntKillHeader(InteractiveScene):
    def construct(self):
        # Test
        words = Text("That which does not kill you only makes you")
        words.to_edge(UP)
        rect = SurroundingRectangle(words["you"][-1], buff=0.1)
        rect.set_stroke(BLUE, 3)
        rect.set_fill(BLUE, 0.5)
        arrow = Arrow(rect.get_bottom(), rect.get_bottom() + 2 * DL)
        arrow.match_color(rect)

        brace = Brace(rect, DOWN, buff=0.1)

        self.add(rect, words, brace)
