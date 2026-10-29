# ==============================================================================
# Scene:      VectorLabel
# Source:     videos/_2024/transformers/chm.py (lines 1810-1827)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VectorLabel.py VectorLabel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VectorLabel(InteractiveScene):
    def construct(self):
        # Test
        brace = Brace(Line(4 * UP, ORIGIN), LEFT)
        brace.center()
        brace.set_stroke(WHITE, 3)
        text = Text("Vector", font_size=90)
        text.next_to(brace, LEFT, MED_SMALL_BUFF)
        text.shift(SMALL_BUFF * UP)

        self.play(
            GrowFromCenter(brace),
            Write(text)
        )
        self.play(
            FlashUnder(text, color=YELLOW)
        )
        self.wait()
