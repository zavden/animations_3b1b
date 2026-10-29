# ==============================================================================
# Scene:      ThinkAboutOverallMap
# Source:     videos/_2024/transformers/attention.py (lines 3104-3117)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkAboutOverallMap.py ThinkAboutOverallMap -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThinkAboutOverallMap(InteractiveScene):
    def construct(self):
        # Test
        rect = Rectangle(6.5, 2.75)
        rect.round_corners(radius=0.5)
        rect.set_stroke(RED_B, 2)
        label = Text("Think about the\noverall map")
        label.next_to(rect, UP, aligned_edge=LEFT)
        label.shift(0.5 * RIGHT)
        self.play(
            ShowCreation(rect),
            FadeIn(label, UP),
        )
        self.wait()
