# ==============================================================================
# Scene:      InformationOfRobotInstructions
# Source:     videos/_2026/cross_entropy/robot.py (lines 7401-7416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InformationOfRobotInstructions.py InformationOfRobotInstructions -w -m --fps 15
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


class InformationOfRobotInstructions(InteractiveScene):
    def construct(self):
        # Write the information of each instruction
        information_calculations = VGroup(*[
            Tex(R"\text{Information}\Big(\Big) = -\log_2\left(\frac{1}{" + str([2, 4, 8, 8][i]) + R"}\right) = " + str([1, 2, 3, 3][i]))
            for i in range(4)
        ]).arrange(DOWN, buff=0.3)
        for calculation in information_calculations:
            calculation.align_to(information_calculations[0], LEFT)
        arrows = VGroup(*[InstructionArrow([UP, DOWN, LEFT, RIGHT][i]) for i in range(4)])
        for calculation, arrow in zip(information_calculations, arrows):
            arrow.scale(0.2)
            arrow.next_to(calculation[11], RIGHT)
            calculation[12:].align_to(arrow.get_right() + RIGHT * 0.2, LEFT)
            self.play(FadeIn(calculation), FadeIn(arrow))
            self.wait(2)
