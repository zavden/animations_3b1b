# ==============================================================================
# Scene:      SharedInsights
# Source:     videos/_2022/convolutions/supplements.py (lines 139-159)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SharedInsights.py SharedInsights -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SharedInsights(InteractiveScene):
    def construct(self):
        # Rects
        rects = ScreenRectangle().get_grid(2, 2, h_buff=2.0, v_buff=2.0)
        rects.set_width(FRAME_WIDTH - 3)
        rects.set_stroke(WHITE, 2)
        rects.set_fill(BLACK, 1)
        self.add(FullScreenRectangle())
        self.add(rects)

        # Inter-relate
        kw = dict(stroke_width=5, stroke_color=YELLOW)
        arrows = VGroup(
            Arrow(rects[3].get_top(), rects[1].get_bottom(), **kw),
            Arrow(rects[3].get_corner(UL), rects[0].get_corner(DR), **kw),
            Arrow(rects[3].get_left(), rects[2].get_right(), **kw),
        )

        self.wait()
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5))
        self.wait()
