# ==============================================================================
# Scene:      DrawingDividingLines
# Source:     videos/_2026/cross_entropy/supplements.py (lines 672-688)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrawingDividingLines.py DrawingDividingLines -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np

class DrawingDividingLines(InteractiveScene):
    def construct(self):
        # Test
        x_values = list(np.arange(-8, 8, 0.5))
        last_lines = VGroup()
        for n in range(5):
            lines = VGroup(Line(UP, DOWN).set_height(0.5).set_stroke(WHITE, 2))
            lines.set_x(-5)
            for k in range(20):
                lines.add(lines[-1].copy().shift(0.35 * random.choice([1, 2, 3]) * RIGHT))

            if n == 0:
                self.play(ShowCreation(lines, lag_ratio=0.05, run_time=1))
            else:
                self.play(ReplacementTransform(last_lines, lines))
            self.wait()
            last_lines = lines
