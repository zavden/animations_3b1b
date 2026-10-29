# ==============================================================================
# Scene:      IndicatingRectangle
# Source:     videos/_2023/convolutions2/supplements.py (lines 589-591)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IndicatingRectangle.py IndicatingRectangle -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IndicatingRectangle(InteractiveScene):
    def construct(self):
        self.play(FlashAround(Rectangle(9, 3), run_time=2, time_width=1.5, stroke_width=8))
