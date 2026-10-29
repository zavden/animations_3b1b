# ==============================================================================
# Scene:      CurvyCurvyArrow
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1270-1282)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CurvyCurvyArrow.py CurvyCurvyArrow -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CurvyCurvyArrow(InteractiveScene):
    def construct(self):
        # Test
        kw = dict(path_arc=-PI, buff=0.2, stroke_width=30, tip_width_ratio=4)
        arrows = VGroup(
            Arrow(DOWN, UP, **kw),
            Arrow(UP, DOWN, **kw),
        )
        arrows.set_color(WHITE)
        arrows.set_height(5)
        self.frame.reorient(-9, 75, 90)
        self.frame.set_field_of_view(1 * DEGREES)
        self.add(arrows)
