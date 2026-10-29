# ==============================================================================
# Scene:      SideBySideForContinuousConv
# Source:     videos/_2022/convolutions/supplements.py (lines 117-127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SideBySideForContinuousConv.py SideBySideForContinuousConv -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SideBySideForContinuousConv(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        squares = Square().replicate(2)
        squares.set_fill(BLACK, 1)
        squares.set_stroke(WHITE, 2)
        squares.set_height(6)
        squares.arrange(RIGHT, buff=0.5)
        squares.set_width(FRAME_WIDTH - 1)
        squares.to_edge(DOWN)
        self.add(squares)
