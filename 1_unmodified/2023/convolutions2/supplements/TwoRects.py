# ==============================================================================
# Scene:      TwoRects
# Source:     videos/_2023/convolutions2/supplements.py (lines 568-579)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoRects.py TwoRects -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TwoRects(InteractiveScene):
    height = 5.5
    width = 6.11
    buff = 1.0
    bottom_buff = MED_LARGE_BUFF

    def construct(self):
        rects = Rectangle(self.width, self.height).replicate(2)
        rects.set_stroke(WHITE, 2)
        rects.arrange(RIGHT, buff=self.buff)
        rects.to_edge(DOWN, buff=self.bottom_buff)
        self.add(rects)
