# ==============================================================================
# Scene:      AmbientDecodingInstructions
# Source:     videos/_2026/cross_entropy/robot.py (lines 7877-7928)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AmbientDecodingInstructions.py AmbientDecodingInstructions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder images/pi_creature_mission_control.png (the original is private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - images/pi_creature_mission_control.png (placeholder image: pi creature at a mission control console)
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
#   images/lunar_rover_assets/stationary.png is the faithful conversion of Stationary.tif (the code looks it up in lowercase).
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


def generate_random_instructions(n, distribution, seed=0):
    np.random.seed(seed)
    instructions = []
    for _ in range(n):
        x = np.random.random()
        for i in range(len(distribution)):
            if x < sum(distribution[:i + 1]):
                instructions.append(i)
                break
    return instructions


class AmbientDecodingInstructions(InteractiveScene):
    def construct(self):
        # Add mission_control and the robot
        mission_control = ImageMobject(
            "images/pi_creature_mission_control.png"
        ).set_width(2).to_edge(RIGHT, buff=0.4)
        robot = ImageMobject(
            "images/lunar_rover_assets/stationary.png"
        ).match_height(mission_control).to_edge(LEFT, buff=0.4).align_to(mission_control, DOWN)
        self.add(mission_control, robot)

        # Create a stream of instructions flowing towards the bot, and decode them into instructions by chunks of 2
        distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        instructions = generate_random_instructions(100, distribution, seed=7)

        arrows = VGroup(*[
            InstructionArrow([UP, DOWN, LEFT, RIGHT][instructions[i]]).scale(0.2).match_y(robot).set_color(PINK)
            for i in range(len(instructions))
        ]).arrange(buff=0.5).align_to(mission_control, LEFT)
        self.add(arrows)

        def update_arrows(m):
            for i, arrow in enumerate(m):
                opacity = min(1, max(0, 0.8 * (mission_control.get_left()[0] - (arrow.get_x() + 0.2))))
                if arrow.get_x() < robot.get_right()[0]:
                    opacity = min(1, max(0, 1 - 1.2 * (robot.get_right()[0] - arrow.get_x())))
                arrow.set_opacity(opacity)
        arrows.add_updater(update_arrows)
        encoding = ["0", "10", "110", "111"]
        bits = VGroup(*[
            Tex(encoding[instruction], font_size=70).set_color(PINK)
            for instruction in instructions
        ])
        position_tracker = ValueTracker(0)
        interp_x_start = 1
        interp_x_end = 0.6
        for arrow, grouping in zip(arrows, bits):
            grouping.move_to(arrow)

            trans = Transform(arrow, grouping, lag_ratio=0.8)
            trans.begin()
            interpolation_tracker = ValueTracker(0)
            original_x = arrow.get_x()

            def update_arrow(m, original_x=original_x, interpolation_tracker=interpolation_tracker, trans=trans):
                interpolation_tracker.set_value(max(0, min(1, (interp_x_start - m.get_x()) / (interp_x_start - interp_x_end))))
                trans.interpolate_mobject(interpolation_tracker.get_value())
                m.set_x(original_x - position_tracker.get_value())
            arrow.add_updater(update_arrow)
        robot.set_opacity(0)
        mission_control.set_opacity(0)
        self.play(position_tracker.animate(run_time=80, rate_func=linear).set_value(100))
