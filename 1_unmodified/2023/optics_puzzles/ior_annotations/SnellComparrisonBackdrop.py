# ==============================================================================
# Scene:      SnellComparrisonBackdrop
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 394-402)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SnellComparrisonBackdrop.py SnellComparrisonBackdrop -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SnellComparrisonBackdrop(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 1))
        rects = Rectangle(6, 7).replicate(2)
        rects.set_fill(BLACK, 1)
        rects.set_stroke(WHITE, 1)
        rects[0].set_x(-FRAME_WIDTH / 4)
        rects[1].set_x(FRAME_WIDTH / 4)
        self.add(rects)
