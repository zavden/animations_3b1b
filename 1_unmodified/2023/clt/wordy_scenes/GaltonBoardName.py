# ==============================================================================
# Scene:      GaltonBoardName
# Source:     videos/_2023/clt/wordy_scenes.py (lines 6-20)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaltonBoardName.py GaltonBoardName -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GaltonBoardName(InteractiveScene):
    def construct(self):
        # Test
        name = Text("Galton \nBoard", font_size=120)
        name.next_to(ORIGIN, RIGHT).shift(2 * UP)
        point = name.get_bottom() + 1 * DOWN
        arrow = Arrow(
            point,
            point + FRAME_WIDTH * LEFT * 0.25,
            stroke_width=10
        )

        self.add(name)
        self.play(GrowArrow(arrow))
        self.wait()
