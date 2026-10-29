# ==============================================================================
# Scene:      PIPHelper
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 1707-1721)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PIPHelper.py PIPHelper -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PIPHelper(InteractiveScene):
    def construct(self):
        frame = Square(side_length=3)
        frame.set_stroke(WHITE, 4)
        frame.set_fill(WHITE, 0.25)
        frame.to_corner(UR)

        vect = Vector(RIGHT, stroke_color=BLUE)
        vect.shift(frame.get_center())
        self.add(frame)
        self.play(
            Rotating(vect, -15 * TAU, about_point=frame.get_center()),
            run_time=30,
            rate_func=linear,
        )
