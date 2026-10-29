# ==============================================================================
# Scene:      RobotTest
# Source:     videos/_2026/cross_entropy/robot.py (lines 58-66)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RobotTest.py RobotTest -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses placeholder top-down robot sprites (Sprite_Vertical/Horizontal.png are not in the repo).
#   - The blinking dot is placed over the light of the robot's own sprites (blinker_offset) and follows it when switching between the vertical and the horizontal sprite.
#
# Placeholder assets (not Grant's originals):
#   - images/lunar_rover_assets/Sprite_Vertical.png and Sprite_Horizontal.png (top-down robot sprites, placeholders)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Robot(Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.overhead_image_vertical = ImageMobject("images/lunar_rover_assets/Sprite_Vertical.png")
        self.overhead_image_horizontal = ImageMobject("images/lunar_rover_assets/Sprite_Horizontal.png").set_opacity(0)
        self.add(self.overhead_image_vertical, self.overhead_image_horizontal)

        self.blinker = GlowDot().set_width(
            self.overhead_image_vertical.get_width() * 0.3
        ).set_color(
            YELLOW
        ).move_to(
            # CHANGE: the own sprites have the light in a different place than Grant's; the dot goes over it
            self.overhead_image_vertical.get_center() + self.blinker_offset(vertical=True)
        )
        self.blinker_opacity_tracker = ValueTracker(0)
        self.blinker.add_updater(lambda m: m.set_opacity(self.blinker_opacity_tracker.get_value()))
        self.add(self.blinker)

        self.move_amount = 0.5
        self.set_width(2.1249567493816737)

    def create(self):
        return FadeIn(self)

    def blinker_offset(self, vertical):
        # CHANGE: position of the orange light on each own sprite, as fractions of the width (the
        # vertical sprite is the horizontal one rotated 90° clockwise)
        dx, dy = (0.116, -0.280) if vertical else (0.280, 0.116)
        return (dx * RIGHT + dy * UP) * self.overhead_image_vertical.get_width()

    def blink_antenna(self):
        return UpdateFromAlphaFunc(self.blinker_opacity_tracker, lambda m, a: m.set_value(1 - (2 * a - 1)**2))

    def execute_instruction(self, instruction_index):
        direction = [UP, DOWN, LEFT, RIGHT][instruction_index]
        if direction[0] == 0:
            self.overhead_image_vertical.set_opacity(1)
            self.overhead_image_horizontal.set_opacity(0)
        else:
            self.overhead_image_vertical.set_opacity(0)
            self.overhead_image_horizontal.set_opacity(1)
        # CHANGE: the blinking dot follows the light of the visible sprite
        self.blinker.move_to(self.overhead_image_vertical.get_center() + self.blinker_offset(vertical=direction[0] == 0))
        return AnimationGroup(
            self.blink_antenna(),
            self.animate.shift(direction * self.move_amount * self.overhead_image_vertical.get_width()), lag_ratio=0.3)


class RobotTest(InteractiveScene):
    def construct(self):
        # Create the robot
        robot = Robot()
        self.play(robot.create())
        # for _ in range(5):
        #     self.play(robot.blink_antenna())
        for instruction in [0, 1, 2, 3, 0, 1, 2, 3]:
            self.play(robot.execute_instruction(instruction))
