# ==============================================================================
# Scene:      FocusOnWall
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 100-115)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FocusOnWall.py FocusOnWall -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FocusOnWall(InteractiveScene):
    def construct(self):
        # Test
        words = Text("Notice what color comes out", font_size=72)
        words.set_backstroke(BLACK, 5)
        words.to_edge(UP)
        arrow = Arrow(
            words["Notice what"].get_bottom(), 6.5 * LEFT + 0.5 * UP,
            buff=0.5,
            stroke_color=RED, stroke_width=14,
        )
        self.play(
            FadeIn(words, 0.25 * UP),
            GrowArrow(arrow),
        )
        self.wait()
