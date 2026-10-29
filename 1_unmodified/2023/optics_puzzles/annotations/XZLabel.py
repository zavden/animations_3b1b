# ==============================================================================
# Scene:      XZLabel
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 627-633)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XZLabel.py XZLabel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class XZLabel(InteractiveScene):
    def construct(self):
        xz_label = Tex("xz")
        x, z = xz_label
        x.next_to(ORIGIN, UP, SMALL_BUFF).to_edge(RIGHT, buff=0.2)
        z.next_to(ORIGIN, RIGHT, SMALL_BUFF).to_edge(UP, buff=0.2)
        self.add(xz_label)
