# ==============================================================================
# Scene:      DimensionComparrison
# Source:     videos/_2024/transformers/supplements.py (lines 686-709)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DimensionComparrison.py DimensionComparrison -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DimensionComparrison(InteractiveScene):
    def construct(self):
        titles = VGroup(
            Text("3d vectors"),
            Text("Word vectors"),
        )
        titles.scale(1.5)
        for title, vect in zip(titles, [LEFT, RIGHT]):
            title.move_to(vect * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=MED_SMALL_BUFF)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN)
        h_line.set_x(0)
        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(GREY_B, 2)

        self.play(
            ShowCreation(lines, lag_ratio=0.5),
            LaggedStartMap(Write, titles, lag_ratio=0.5)
        )
        self.wait()
