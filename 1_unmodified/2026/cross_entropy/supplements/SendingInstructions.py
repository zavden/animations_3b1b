# ==============================================================================
# Scene:      SendingInstructions
# Source:     videos/_2026/cross_entropy/supplements.py (lines 511-535)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl SendingInstructions.py SendingInstructions -w -m --fps 15
#
# Notes:
#   arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2026/cross_entropy/entropy.py -----

class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, width=0.5, *args, **kwargs):
        super().__init__("arrow.svg", *args, **kwargs)
        self.set_width(width)
        self.rotate(angle_of_vector(direction))
        self.direction = direction


class ArrowGroup(VGroup):
    def __init__(self):
        super().__init__(InstructionArrow(v) for v in [UP, DOWN, LEFT, RIGHT])



# ----- From _2026/cross_entropy/supplements.py -----

class SendingInstructions(InteractiveScene):
    def construct(self):
        # Test
        arrow_group = ArrowGroup()
        arrows = VGroup(random.choice(arrow_group).copy() for n in range(25))
        radius = 3
        arrows.move_to(radius * RIGHT)

        def update_arrow(arrow):
            r = get_norm(arrow.get_center())
            op = clip(inverse_interpolate(radius, 0.8 * radius, r), 0, 1)
            arrow.set_fill(opacity=op)

        for arrow in arrows:
            arrow.add_updater(update_arrow)

        self.play(
            LaggedStart(
                (arrow.animate.shift(2 * radius * LEFT).set_anim_args(path_arc=120 * DEG)
                for arrow in arrows),
                lag_ratio=0.1,
                run_time=12
            )
        )
        self.wait()
