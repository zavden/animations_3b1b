# ==============================================================================
# Scene:      RobotOnMoon2
# Source:     videos/_2026/cross_entropy/robot.py (lines 327-352)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RobotOnMoon2.py RobotOnMoon2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses placeholder top-down robot sprites (Sprite_Vertical/Horizontal.png are not in the repo).
#   - Uses the placeholder images/far_away_moon.png as the lunar ground texture.
#   - The blinking dot is placed over the light of the robot's own sprites (blinker_offset) and follows it when switching between the vertical and the horizontal sprite.
#
# Placeholder assets (not Grant's originals):
#   - images/lunar_rover_assets/Sprite_Vertical.png and Sprite_Horizontal.png (top-down robot sprites, placeholders)
#   - images/far_away_moon.png (placeholder lunar surface texture, tileable)
#
# Notes:
#   images/arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo; it is not an invented asset.
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


class RobotOnMoon(InteractiveScene):
    def construct(self):
        # Add the robot
        robot = Robot()
        self.play(robot.create(), run_time=2)

        # Add the surface of the far away moon
        moon_surface = ImageMobject("images/far_away_moon.png").get_grid(20, 20, buff=0).scale(5).set_opacity(0.4)
        self.bring_to_back(moon_surface)
        self.play(FadeIn(moon_surface), run_time=2)

        # The robot roams around
        directions = [UP, DOWN, LEFT, RIGHT]
        instruction_set = VGroup(*[
            InstructionArrow(
                direction
            ).scale(
                0.5
            ).set_opacity(
                0
            )
            for direction in directions
        ])
        self.add(instruction_set)
        arrow_length = instruction_set[0].get_height()
        arrow_animation_tracker = ValueTracker(0)
        for arrow in instruction_set:
            def update_arrow(m):
                m.set_opacity(arrow_animation_tracker.get_value() * 0.6)
                m.next_to(
                    robot.overhead_image_vertical, m.direction, buff=0.8 if (m.direction == DOWN).all() else 1.2
                )
                if m.direction[1] == 0:
                    m.stretch_to_fit_width(max(arrow_animation_tracker.get_value() * arrow_length, 0.1))
                else:
                    m.stretch_to_fit_height(max(arrow_animation_tracker.get_value() * arrow_length, 0.1))
            arrow.add_updater(update_arrow)

        fractions = VGroup(
            Tex(R"\mathbf{1/2}", font_size=200),
            Tex(R"\mathbf{1/4}", font_size=200),
            Tex(R"\mathbf{1/8}", font_size=200),
            Tex(R"\mathbf{1/8}", font_size=200)
        ).set_color(WHITE)
        self.add(fractions)
        fraction_opacity_trackers = [ValueTracker(0) for fraction in fractions]
        fractions_master_opacity_tracker = ValueTracker(0)
        for i in range(len(fraction_opacity_trackers)):
            def update_fraction_opacity_tracker(m, i=i):
                m.set_value(max(0, min(1, 8 * (fractions_master_opacity_tracker.get_value() - 0.25 * i))))
            fraction_opacity_trackers[i].add_updater(update_fraction_opacity_tracker)
        self.add(*fraction_opacity_trackers, fractions_master_opacity_tracker)

        def update_fractions(m):
            fractions[0].next_to(instruction_set[0].get_top(), UP, buff=2).set_opacity(fraction_opacity_trackers[0].get_value())
            fractions[1].next_to(instruction_set[1].get_bottom(), DOWN, buff=2).set_opacity(fraction_opacity_trackers[1].get_value())
            fractions[2].next_to(instruction_set[2].get_left(), LEFT, buff=2).set_opacity(fraction_opacity_trackers[2].get_value())
            fractions[3].next_to(instruction_set[3].get_right(), RIGHT, buff=2).set_opacity(fraction_opacity_trackers[3].get_value())
        fractions.add_updater(update_fractions)

        distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        self.gravitate_camera_towards(robot, target_zoom_level=0.7)
        tail = TracingTail(robot.overhead_image_vertical, stroke_color=TEAL, time_traced=5, stroke_width=5)
        self.add(tail)
        instructions = generate_random_instructions(750, distribution)
        arrow_draw_iter = 10
        zoom_out_iter = arrow_draw_iter + 6
        fractions_draw_iter = arrow_draw_iter + 19
        iters_to_draw_fractions = 55
        for i in range(len(instructions)):
            anims = [robot.execute_instruction(instructions[i])]
            if i == arrow_draw_iter:
                anims.append(arrow_animation_tracker.animate(rate_func=lambda a: 2 * smooth(a * 0.5), run_time=1.3).set_value(0.5))
            if i == arrow_draw_iter + 1:
                anims.append(arrow_animation_tracker.animate(rate_func=lambda a: 2 * (smooth((a * 0.5 + 0.5)) - smooth(0.5)), run_time=1.3).set_value(1))
            if fractions_draw_iter <= i < fractions_draw_iter + iters_to_draw_fractions:
                anims.append(
                    fractions_master_opacity_tracker.animate(
                        rate_func=linear
                    ).set_value(
                        ((i + 1) - fractions_draw_iter) / iters_to_draw_fractions
                    )
                )
            run_time = 1
            if i == zoom_out_iter:
                self.gravitate_camera_towards(robot, target_zoom_level=0.25, zoom_gravity_constant=0.01)
                self.bring_to_back(tail)
                tail.add_updater(lambda m: m.set_stroke(width=3))
            if i > zoom_out_iter - 3:
                run_time = max(0.15, smooth(1 - 0.1 * (i - (zoom_out_iter - 3))))
            self.play(AnimationGroup(*anims, run_time=run_time))

    def gravitate_camera_towards(
        self,
        mobject_or_func,
        x_pct=0.5,
        y_pct=0.5,
        target_zoom_level=None,
        friction=0.05,
        gravity_constant=0.01,
        zoom_gravity_constant=0.03
    ):
        frame = self.camera.frame
        frame.clear_updaters()
        frame.velocity = np.zeros(3)
        frame.width_velocity = 0

        def update_camera(f, dt):
            if callable(mobject_or_func):
                target_center = mobject_or_func()
            else:
                target_center = mobject_or_func.get_center()

            offset_x = (x_pct - 0.5) * f.get_width()
            offset_y = (y_pct - 0.5) * f.get_height()

            desired_center = target_center - np.array([offset_x, offset_y, 0])
            current_center = f.get_center()

            direction = desired_center - current_center
            distance = np.linalg.norm(direction)

            if distance > 0:
                acceleration = direction * gravity_constant * distance
                f.velocity += acceleration

            f.velocity *= (1 - friction)
            f.shift(f.velocity * dt)

            if target_zoom_level is not None:
                width_diff = (1 / target_zoom_level) * FRAME_WIDTH - f.get_width()
                width_acceleration = width_diff * zoom_gravity_constant
                f.width_velocity += width_acceleration
                f.width_velocity *= (1 - friction)

                new_width = f.get_width() + f.width_velocity * dt
                f.set_width(new_width)

        frame.add_updater(update_camera)


class RobotOnMoon2(RobotOnMoon):
    def construct(self):
        # Add the robot and the moon
        robot = Robot()
        moon_surface = ImageMobject("images/far_away_moon.png").get_grid(20, 20, buff=0).scale(5).set_opacity(0.4)
        self.add(moon_surface, robot)
        self.gravitate_camera_towards(robot, gravity_constant=0.1)

        # Move the robot around a bit randomly
        tail = TracingTail(robot.overhead_image_vertical, stroke_color=TEAL, time_traced=5, stroke_width=5)
        self.add(tail)
        distribution = [1 / 2, 1 / 4, 1 / 8, 1 / 8]
        instructions = generate_random_instructions(18, distribution)
        for instruction in instructions:
            self.play(robot.execute_instruction(instruction))
            self.bring_to_back(tail)
        self.wait(6)

        # Move the robot according to the specific instructions from the encoding example
        instructions = [1, 0, 2, 0, 2, 0, 1, 3, 1, 1, 0, 0, 0, 3, 2, 0] + generate_random_instructions(40, distribution)
        for i in range(len(instructions)):
            self.play(robot.execute_instruction(instructions[i]), run_time=1 if i < 3 else 0.35)
            self.bring_to_back(tail)
            if i < 3:
                self.wait(6)
        self.wait(6)
