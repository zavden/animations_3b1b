# ==============================================================================
# Scene:      BigPlus
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1257-1267)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigPlus.py BigPlus -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class BigPlus(InteractiveScene):
    def construct(self):
        brace = Brace(Line(2 * DOWN, 2 * UP), RIGHT)
        brace.set_height(7)
        brace.move_to(2 * LEFT)
        plus = Tex("+", font_size=90)
        plus.next_to(brace, LEFT, buff=2.5)
        equals = Tex("=", font_size=90)
        equals.next_to(brace, RIGHT, buff=1.0)

        self.add(plus, brace, equals)
