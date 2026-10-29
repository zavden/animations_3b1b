# ==============================================================================
# Scene:      ContrastWithEarlierFrame
# Source:     videos/_2024/transformers/chm.py (lines 622-647)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastWithEarlierFrame.py ContrastWithEarlierFrame -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ContrastWithEarlierFrame(InteractiveScene):
    def construct(self):
        # Test
        vline = Line(UP, DOWN)
        vline.set_height(FRAME_HEIGHT)
        self.add(vline)

        titles = VGroup(
            VGroup(
                Text("Most earlier models"),
                # Vector(0.75 * DOWN, thickness=4),
                # Text("One word at a time")
            ),
            VGroup(
                Text("Transformers"),
                # Vector(0.75 * DOWN, thickness=4),
                # Text("All words in parallel")
            ),
        )
        for title, vect in zip(titles, [LEFT, RIGHT]):
            title.arrange(DOWN, buff=0.2)
            title.scale(1.5)
            title.move_to(FRAME_WIDTH * vect / 4)
            title.to_edge(UP)

        self.add(titles)
