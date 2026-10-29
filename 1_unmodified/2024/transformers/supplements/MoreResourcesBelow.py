# ==============================================================================
# Scene:      MoreResourcesBelow
# Source:     videos/_2024/transformers/supplements.py (lines 1317-1335)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreResourcesBelow.py MoreResourcesBelow -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MoreResourcesBelow(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle())
        words = Text("More resources below", font_size=72)
        words.move_to(UP)
        arrows = Vector(1.5 * DOWN, stroke_width=10).get_grid(1, 3, buff=1.5)
        arrows.next_to(words, DOWN, buff=MED_LARGE_BUFF)
        morty = Mortimer()
        morty.body.insert_n_curves(100)
        morty.to_corner(DR)

        self.add(words)
        self.play(
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5),
            morty.change("thinking", look_at=4 * DOWN)
        )
        self.play(Blink(morty))
        self.wait()
