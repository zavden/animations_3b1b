# ==============================================================================
# Scene:      PaperTitle
# Source:     videos/_2023/gauss_int/supplements.py (lines 64-80)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PaperTitle.py PaperTitle -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PaperTitle(InteractiveScene):
    def construct(self):
        # Test
        title = Text(R"""
            The Unreasonable Effectiveness
            of Mathematics in the
            Natural Sciences
        """, alignment="LEFT", font_size=60)
        title.to_corner(UL)
        self.play(Write(title, run_time=3, lag_ratio=0.1))
        self.wait()
        part = title["Unreasonable Effectiveness"]
        self.play(
            part.animate.set_color(BLUE),
            FlashUnder(part, time_width=1.5, run_time=2, color=BLUE)
        )
        self.wait()
