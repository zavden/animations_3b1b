# ==============================================================================
# Scene:      Confetti
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 101-124)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Confetti.py Confetti -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConfettiSpiril(Animation):
    x_start = 0
    spiril_radius = 0.5
    num_spirals = 4
    run_time = 10
    rate_func = None

    def __init__(self, mobject, **kwargs):
        x_start = kwargs.pop("x_start", self.x_start)
        self.num_spirals = kwargs.pop("num_spirals", self.num_spirals)
        mobject.next_to(x_start * RIGHT + FRAME_Y_RADIUS * UP, UP)
        self.total_vert_shift = FRAME_HEIGHT + mobject.get_height() + 2 * MED_SMALL_BUFF

        super().__init__(mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        submobject.set_points(starting_submobject.get_points())

    def interpolate_mobject(self, alpha):
        Animation.interpolate_mobject(self, alpha)
        angle = alpha * self.num_spirals * TAU
        vert_shift = alpha * self.total_vert_shift

        start_center = self.mobject.get_center()
        self.mobject.shift(self.spiril_radius * OUT)
        self.mobject.rotate(angle, axis=UP, about_point=start_center + 0.5 * RIGHT)
        self.mobject.shift(vert_shift * DOWN)


class Confetti(InteractiveScene):
    def construct(self):
        # Test
        num_confetti_squares = 300
        colors = [RED, YELLOW, GREEN, BLUE, PURPLE, RED]
        confetti_squares = [
            Square(
                side_length=0.2,
                stroke_width=0,
                fill_opacity=0.75,
                fill_color=random.choice(colors),
            )
            for x in range(num_confetti_squares)
        ]
        confetti_spirils = [
            ConfettiSpiril(
                square,
                x_start=2 * random.random() * FRAME_X_RADIUS - FRAME_X_RADIUS,
                num_spirals=np.random.uniform(-5, 5),
            )
            for square in confetti_squares
        ]

        self.play(LaggedStart(*confetti_spirils, lag_ratio=1e-2, run_time=10))
