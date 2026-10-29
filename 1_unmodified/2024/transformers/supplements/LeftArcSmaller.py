# ==============================================================================
# Scene:      LeftArcSmaller
# Source:     videos/_2024/transformers/supplements.py (lines 1035-1040)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeftArcSmaller.py LeftArcSmaller -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LeftArcSmaller(InteractiveScene):
    def construct(self):
        # Test
        arrow = Arrow(RIGHT, LEFT, path_arc=1.0 * PI, stroke_color=RED, stroke_width=8)
        self.play(ShowCreation(arrow))
        self.wait()
