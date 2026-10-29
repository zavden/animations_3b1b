# ==============================================================================
# Scene:      RotationMove
# Source:     videos/_2024/puzzles/added_dimension.py (lines 233-263)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationMove.py RotationMove -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RotationMove(InteractiveScene):
    def construct(self):
        # Add hex
        lozenge = Polygon(math.sqrt(3) * LEFT, UP, math.sqrt(3) * RIGHT, DOWN)
        lozenge.move_to(ORIGIN, DOWN)
        hexagon = VGroup(
            lozenge,
            lozenge.copy().rotate(TAU / 3, about_point=ORIGIN),
            lozenge.copy().rotate(2 * TAU / 3, about_point=ORIGIN),
        )
        hexagon.set_fill(TEAL_E, 1)
        hexagon.set_stroke(WHITE, 3)
        hexagon.set_height(3)
        hexagon.move_to(3 * LEFT)

        rot_hex = hexagon.copy()
        hexagon.rotate(-60 * DEGREES)
        rot_hex.move_to(3 * RIGHT)

        arrow1 = Arrow(hexagon, rot_hex, thickness=5, path_arc=60 * DEGREES).shift(DOWN)
        arrow2 = Arrow(rot_hex, hexagon, thickness=5, path_arc=60 * DEGREES).shift(UP)

        self.add(hexagon, rot_hex, arrow1, arrow2)
        self.wait()
        self.play(LaggedStart(
            VShowPassingFlash(arrow1.copy().set_stroke(YELLOW, 3)),
            TransformFromCopy(hexagon, rot_hex, path_arc=60 * DEGREES),
            lag_ratio=0.1,
            run_time=2,
        ))
        self.wait()
