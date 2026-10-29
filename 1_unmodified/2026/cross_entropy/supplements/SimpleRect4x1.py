# ==============================================================================
# Scene:      SimpleRect4x1
# Source:     videos/_2026/cross_entropy/supplements.py (lines 34-35)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleRect4x1.py SimpleRect4x1 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SimpleRect(InteractiveScene):
    dimensions = (1, 1)

    def construct(self):
        # Test
        rect = Rectangle(*self.dimensions).set_stroke(YELLOW, 3)
        rect.add_line_to(rect.get_corner(UL))
        rect.insert_n_curves(100)
        self.play(VShowPassingFlash(rect, time_width=1.5, run_time=5))
        self.wait()


class SimpleRect4x1(SimpleRect):
    dimensions = (2, 0.5)
