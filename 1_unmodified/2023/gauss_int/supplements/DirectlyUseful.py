# ==============================================================================
# Scene:      DirectlyUseful
# Source:     videos/_2023/gauss_int/supplements.py (lines 576-595)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DirectlyUseful.py DirectlyUseful -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DirectlyUseful(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        rects = ScreenRectangle().replicate(2)
        rects.set_stroke(WHITE, 2)
        rects.set_fill(BLACK, 1)
        rects.arrange(RIGHT, buff=LARGE_BUFF)
        rects.set_width(FRAME_WIDTH - 1)
        rects.to_edge(DOWN, buff=1.5)
        self.add(rects)

        arrow = Arrow(rects[1].get_top(), rects[0].get_top(), path_arc=0.5 * PI)
        words = Text("Directly useful")
        words.next_to(arrow, UP)

        self.play(
            ShowCreation(arrow),
            FadeIn(words, lag_ratio=0.1),
        )
        self.wait()
