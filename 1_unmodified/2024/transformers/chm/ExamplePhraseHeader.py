# ==============================================================================
# Scene:      ExamplePhraseHeader
# Source:     videos/_2024/transformers/chm.py (lines 1921-1935)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplePhraseHeader.py ExamplePhraseHeader -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ExamplePhraseHeader(InteractiveScene):
    def construct(self):
        # Test
        phrase = Text("The Computer History Museum\nis located in ?????")
        phrase.to_edge(UP)
        rect = SurroundingRectangle(phrase).set_stroke(WHITE, 2)

        q_marks = phrase["?????"][0]
        q_marks[::4].set_fill(opacity=0)
        q_rect = SurroundingRectangle(q_marks)
        q_rect.set_fill(YELLOW, 0.25)
        q_rect.set_stroke(YELLOW, 2)

        self.add(q_rect)
        self.add(phrase)
