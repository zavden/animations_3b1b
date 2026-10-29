# ==============================================================================
# Scene:      ContinuousAssociation
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 398-412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContinuousAssociation.py ContinuousAssociation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ContinuousAssociation(InteractiveScene):
    def construct(self):
        words = Text("Continuous\nAssociation", font_size=60)
        words.to_corner(UR)
        arrows = VGroup(
            Arrow(3 * LEFT, 3 * RIGHT, path_arc=PI / 2, thickness=6).shift(2.5 * DOWN),
            Arrow(3 * RIGHT, 3 * LEFT, path_arc=PI / 2, thickness=6).shift(2.5 * UP),
        )
        arrows.set_fill(TEAL)

        self.play(
            Write(words),
            *map(Write, arrows)
        )
        self.wait()
