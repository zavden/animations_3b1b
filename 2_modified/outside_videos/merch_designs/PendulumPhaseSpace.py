# ==============================================================================
# Scene:      PendulumPhaseSpace
# Source:     videos/outside_videos/merch_designs.py (lines 87-154)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PendulumPhaseSpace.py PendulumPhaseSpace -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the fractals import is removed (not used in this scene; besides, manimlib.once_useful_constructs no longer exists and its fractals.py does not import)
#   - the 2019 arrow VectorField (delta_x, length_func...) no longer exists in manimgl; minimal equivalent version
#   - Axes: x_min/x_max/tick_frequency -> x_range/y_range with step
#   - uses OldVectorField; without max_magnitude or tip_length, and the thickness (stroke 12) becomes the arrow's thickness
# ==============================================================================

from manim_imports_ext import *
# CHANGE: the fractals import is removed (not used in this scene; besides, manimlib.once_useful_constructs no longer exists and its fractals.py does not import)

# CHANGE: the 2019 arrow VectorField (delta_x, length_func...) no longer exists in manimgl; minimal equivalent version
class OldVectorField(VGroup):
    def __init__(
        self, func,
        delta_x=0.5, delta_y=0.5,
        x_min=int(np.floor(-FRAME_WIDTH / 2)), x_max=int(np.ceil(FRAME_WIDTH / 2)),
        y_min=int(np.floor(-FRAME_HEIGHT / 2)), y_max=int(np.ceil(FRAME_HEIGHT / 2)),
        length_func=lambda norm: 0.45 * sigmoid(norm),
        vector_config=dict(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.func = func
        self.length_func = length_func
        self.vector_config = vector_config
        x_range = np.arange(x_min, x_max + delta_x, delta_x)
        y_range = np.arange(y_min, y_max + delta_y, delta_y)
        for x, y in it.product(x_range, y_range):
            self.add(self.get_vector(x * RIGHT + y * UP))

    def get_vector(self, point):
        output = np.array(self.func(point))
        norm = get_norm(output)
        if norm == 0:
            output *= 0
        else:
            output *= self.length_func(norm) / norm
        vect = Vector(output, **self.vector_config)
        vect.shift(point)
        return vect


class PendulumPhaseSpace(Scene):
    def construct(self):
        # CHANGE: Axes: x_min/x_max/tick_frequency -> x_range/y_range with step
        axes = Axes(
            x_range=(-PI, PI, PI / 4),
            y_range=(-2, 2, 0.25),
            x_axis_config={
                "unit_size": FRAME_WIDTH / TAU,
                "include_tip": False,
            },
            y_axis_config={
                "unit_size": 4,
            },
        )

        def func(point, mu=0.1, k=0.5):
            theta, theta_dot = axes.p2c(point)
            return axes.c2p(
                theta_dot,
                -mu * theta_dot - k * np.sin(theta),
            )

        # CHANGE: uses OldVectorField; without max_magnitude or tip_length, and the thickness (stroke 12) becomes the arrow's thickness
        field = OldVectorField(
            func,
            delta_x=1.5 * FRAME_WIDTH / 12,
            delta_y=1.5,
            y_min=-6,
            y_max=6,
            length_func=lambda norm: 1.25 * sigmoid(norm),
            vector_config={
                "max_tip_length_to_length_ratio": 0.35,
                "thickness": 6,
            },
        )
        colors = list(Color(BLUE).range_to(RED, 5))
        for vect in field:
            mag = get_norm(1.18 * func(vect.get_start()))
            vect.set_color(colors[min(int(mag), len(colors) - 1)])

        line = VMobject()
        line.start_new_path(axes.c2p(
            -3 * TAU / 4,
            1.75,
        ))

        dt = 0.1
        t = 0
        total_time = 60

        while t < total_time:
            t += dt
            last_point = line.get_last_point()
            new_point = last_point + dt * func(last_point)
            if new_point[0] > FRAME_WIDTH / 2:
                new_point = last_point + FRAME_WIDTH * LEFT
                line.start_new_path(new_point)
            else:
                line.add_smooth_curve_to(new_point)

        line.set_stroke(WHITE, 6)

        # self.add(axes)
        self.add(field)
