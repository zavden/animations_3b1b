# ==============================================================================
# Scene:      LowTempHighTempContrast
# Source:     videos/_2024/transformers/supplements.py (lines 765-784)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LowTempHighTempContrast.py LowTempHighTempContrast -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LowTempHighTempContrast(InteractiveScene):
    def construct(self):
        # Test
        titles = VGroup(
            Text("Temp = 0", font_size=72).set_x(-FRAME_WIDTH / 4),
            Text("Temp = 5", font_size=72).set_x(FRAME_WIDTH / 4),
        )
        titles.to_edge(UP, buff=0.25)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN, buff=0.1)
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        lines = VGroup(h_line, v_line)
        lines.set_stroke(GREY_B, 2)

        self.play(
            LaggedStartMap(FadeIn, titles, shift=0.25 * UP, lag_ratio=0.25),
            LaggedStartMap(Write, lines, lag_ratio=0.5),
            run_time=1
        )
        self.wait()
