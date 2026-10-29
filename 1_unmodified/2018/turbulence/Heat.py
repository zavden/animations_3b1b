# ==============================================================================
# Scene:      Heat
# Source:     videos/_2018/turbulence.py (lines 1307-1351)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Heat.py Heat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Heat(Scene):
    def construct(self):
        box = Square(
            side_length=2,
            stroke_color=WHITE,
        )
        balls = VGroup(*[
            self.get_ball(box)
            for x in range(20)
        ])

        self.add(box, balls)
        self.wait(20)

    def get_ball(self, box):
        speed_factor = random.random()
        ball = Dot(
            radius=0.05,
            color=interpolate_color(BLUE, RED, speed_factor)
        )
        speed = 2 + 3 * speed_factor
        direction = rotate_vector(RIGHT, TAU * random.random())
        ball.velocity = speed * direction
        x0, y0, z0 = box.get_corner(DL)
        x1, y1, z1 = box.get_corner(UR)
        ball.move_to(np.array([
            interpolate(x0, x1, random.random()),
            interpolate(y0, y1, random.random()),
            0
        ]))

        def update(ball, dt):
            ball.shift(ball.velocity * dt)
            if ball.get_left()[0] < box.get_left()[0]:
                ball.velocity[0] = abs(ball.velocity[0])
            if ball.get_right()[0] > box.get_right()[0]:
                ball.velocity[0] = -abs(ball.velocity[0])
            if ball.get_bottom()[1] < box.get_bottom()[1]:
                ball.velocity[1] = abs(ball.velocity[1])
            if ball.get_top()[1] > box.get_top()[1]:
                ball.velocity[1] = -abs(ball.velocity[1])
            return ball

        ball.add_updater(update)
        return ball
