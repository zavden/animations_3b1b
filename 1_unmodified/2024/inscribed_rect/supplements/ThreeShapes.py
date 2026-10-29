# ==============================================================================
# Scene:      ThreeShapes
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 170-189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeShapes.py ThreeShapes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeShapes(InteractiveScene):
    def construct(self):
        # Test
        v_lines = Line(DOWN, UP).replicate(2)
        v_lines.set_height(FRAME_HEIGHT)
        v_lines.arrange(RIGHT, buff=FRAME_WIDTH / 3)
        v_lines.set_stroke(WHITE, 3)

        titles = VGroup(
            Text("Möbius Strip"),
            Text("Torus"),
            Text("Klein Bottle"),
        )
        for title, x in zip(titles, [-1, 0, 1]):
            title.scale(60 / 48)
            title.set_x(x * FRAME_WIDTH / 3)
            title.to_edge(UP)

        self.add(v_lines)
        self.add(titles)
