# ==============================================================================
# Scene:      InterpolateTest
# Source:     videos/_2026/cross_entropy/robot.py (lines 7931-7952)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InterpolateTest.py InterpolateTest -w -m --fps 15
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, *args, **kwargs):
        super().__init__("images/arrow.svg", *args, **kwargs)
        if (direction == UP).all():
            self.rotate(PI / 2)
        elif (direction == LEFT).all():
            self.rotate(PI)
        elif (direction == DOWN).all():
            self.rotate(3 * PI / 2)
        self.direction = direction


class InterpolateTest(InteractiveScene):
    def construct(self):
        # Test Mobject interpolation
        mob1 = InstructionArrow(LEFT).scale(0.3).shift(RIGHT * 6)
        mob2 = Tex("010").shift(LEFT).move_to(mob1)

        self.add(mob1)

        trans = Transform(mob1, mob2)
        trans.begin()
        interpolation_tracker = ValueTracker(0)
        position_tracker = ValueTracker(0)
        original_x = mob1.get_x()
        x_start = 1
        x_end = -1

        def update_arrow(m):
            interpolation_tracker.set_value(max(0, min(1, (x_start - m.get_x()) / (x_start - x_end))))
            trans.interpolate_mobject(interpolation_tracker.get_value())
            m.set_x(original_x - position_tracker.get_value())
        mob1.add_updater(update_arrow)
        self.play(position_tracker.animate(run_time=8, rate_func=linear).set_value(10))
