# ==============================================================================
# Scene:      YLineFlash
# Source:     videos/_2023/gauss_int/supplements.py (lines 548-553)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YLineFlash.py YLineFlash -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class YLineFlash(InteractiveScene):
    def construct(self):
        line = Line(7 * RIGHT, 7 * LEFT)
        line.insert_n_curves(50)
        line.set_stroke(YELLOW, 5)
        self.play(VShowPassingFlash(line, run_time=3, time_width=0.7))
