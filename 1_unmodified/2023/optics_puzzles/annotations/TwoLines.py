# ==============================================================================
# Scene:      TwoLines
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 295-301)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoLines.py TwoLines -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TwoLines(InteractiveScene):
    def construct(self):
        h_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(WHITE, 3)
        self.add(lines)
