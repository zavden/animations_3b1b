# ==============================================================================
# Scene:      ImplicationPIP
# Source:     videos/_2023/gauss_int/supplements.py (lines 853-873)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImplicationPIP.py ImplicationPIP -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ImplicationPIP(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        screens = ScreenRectangle().replicate(2)
        screens.set_height(0.45 * FRAME_HEIGHT)
        screens.arrange(RIGHT, buff=0.75)
        screens.set_stroke(WHITE, 2)
        screens.set_fill(BLACK, 1)
        screens.move_to(0.5 * DOWN)

        arrow = Arrow(screens[0].get_top(), screens[1].get_top(), path_arc=-0.4 * PI)
        words = Text("These necessarily imply")
        words.next_to(arrow, UP)

        self.add(screens)
        self.wait()
        self.play(
            ShowCreation(arrow),
            FadeIn(words, lag_ratio=0.1)
        )
        self.wait()
