# ==============================================================================
# Scene:      LinearRegression
# Source:     videos/_2024/transformers/ml_basics.py (lines 1036-1171)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl LinearRegression.py LinearRegression -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class Dial(VGroup):
    def __init__(
        self,
        radius=0.5,
        relative_tick_size=0.2,
        value_range=(0, 1, 0.1),
        initial_value=0,
        arc_angle=270 * DEGREES,
        stroke_width=2,
        stroke_color=WHITE,
        needle_color=BLUE,
        needle_stroke_width=5.0,
        value_to_color_config=dict(),
        set_anim_streak_color=TEAL,
        set_anim_streak_width=4,
        set_value_anim_streak_density=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())



# ----- From _2024/transformers/ml_basics.py -----

class LinearRegression(InteractiveScene):
    radom_seed = 1

    def construct(self):
        # Set up axes
        x_min, x_max = (-1, 12)
        y_min, y_max = (-1, 10)
        axes = Axes((x_min, x_max), (y_min, y_max), width=12, height=6)
        axes.to_edge(DOWN)
        self.add(axes)

        # Add data
        n_data_points = 30
        m = 0.75
        y0 = 1

        data = np.array([
            (x, y0 + m * x + 0.75 * np.random.normal(0, 1))
            for x in np.random.uniform(2, x_max, n_data_points)
        ])
        points = axes.c2p(data[:, 0], data[:, 1])
        dots = DotCloud(points)

        dots.set_color(YELLOW)
        dots.set_glow_factor(1)
        dots.set_radius(0.075)

        self.add(dots)

        # Make title
        title = Text("Linear Regression", font_size=72)
        title.to_edge(UP)

        # Show line
        m_tracker = ValueTracker(m)
        y0_tracker = ValueTracker(y0)
        line = Line()
        line.set_stroke(TEAL, 2)

        def update_line(line):
            curr_y0 = y0_tracker.get_value()
            curr_m = m_tracker.get_value()
            line.put_start_and_end_on(
                axes.c2p(0, curr_y0),
                axes.c2p(x_max, curr_y0 + curr_m * x_max),
            )

        line.add_updater(update_line)

        self.play(
            FadeIn(title, UP),
            ShowCreation(line),
        )
        self.wait()

        # Label inputs and outputs
        in_labels = VGroup(Text("Input"), Text("Square footage"))
        out_labels = VGroup(Text("Output"), Text("Price"))
        for in_label in in_labels:
            in_label.next_to(axes.x_axis, DOWN, buff=0.1, aligned_edge=RIGHT)
        for out_label in out_labels:
            out_label.rotate(90 * DEGREES)
            out_label.next_to(axes.y_axis, LEFT, aligned_edge=UP)

        self.play(LaggedStart(
            FadeIn(in_labels[0], lag_ratio=0.1),
            FadeIn(out_labels[0], lag_ratio=0.1),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(LaggedStart(
            FadeTransform(*in_labels),
            FadeTransform(*out_labels),
            lag_ratio=0.8,
        ))
        self.wait()

        # Emphasize line
        self.play(
            VShowPassingFlash(
                line.copy().set_stroke(BLUE, 8).scale(1.1).insert_n_curves(100),
                time_width=1.5,
                run_time=2
            ),
        )
        self.wait()

        # Add line parameter updaters
        words = ["slope", "y-intercept"]
        value_ranges = [(0, 2, 0.2), (-2, 3, 0.5)]
        m_label, y0_label = labels = VGroup(
            VGroup(
                Dial(value_range=value_range),
                Text(f"{text} = "),
                DecimalNumber(),
            )
            for text, value_range in zip(words, value_ranges)
        )
        for label, tracker in zip(labels, [m_tracker, y0_tracker]):
            label[0].set_height(2 * label[2].get_height())
            label.arrange(RIGHT)
            label[0].f_always.set_value(tracker.get_value)
            label[2].f_always.set_value(tracker.get_value)
        labels.arrange(DOWN, aligned_edge=LEFT)
        labels.next_to(axes.y_axis, RIGHT, buff=1.0)
        labels.to_edge(UP)

        self.play(
            FadeOut(title, UP),
            FadeIn(m_label, UP),
        )
        self.play(
            m_tracker.animate.set_value(1.5),
            run_time=2,
        )
        self.play(FadeIn(y0_label, UP))
        self.play(
            y0_tracker.animate.set_value(-2),
            run_time=2
        )
        self.wait()

        # Tweak line parameters
        for n in range(10):
            alpha = random.random()
            if alpha > 0.5:
                alpha += 1
            new_m = interpolate(m_tracker.get_value(), m, alpha)
            new_y0 = interpolate(y0_tracker.get_value(), y0, alpha)
            self.play(LaggedStart(
                m_tracker.animate.set_value(new_m),
                y0_tracker.animate.set_value(new_y0),
                run_time=1.5,
                lag_ratio=0.25,
            ))
            self.wait(0.5)
