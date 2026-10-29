# ==============================================================================
# Scene:      AmbientModelPredictions
# Source:     videos/_2026/cross_entropy/language_models.py (lines 95-104)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl AmbientModelPredictions.py AmbientModelPredictions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


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


class MachineWithDials(VGroup):
    default_dial_config = dict(
        stroke_width=1.0,
        needle_stroke_width=5.0,
        relative_tick_size=0.25,
        set_anim_streak_width=2,
    )

    def __init__(
        self,
        width=5.0,
        height=4.0,
        n_rows=6,
        n_cols=8,
        dial_buff_ratio=0.5,
        stroke_color=WHITE,
        stroke_width=1,
        fill_color=GREY_D,
        fill_opacity=1.0,
        dial_config=dict(),
    ):
        super().__init__()
        box = Rectangle(width, height)
        box.set_stroke(stroke_color, stroke_width)
        box.set_fill(fill_color, fill_opacity)
        self.box = box

        dial_config = dict(**self.default_dial_config, **dial_config)
        dials = Dial(**dial_config).get_grid(n_rows, n_cols, buff_ratio=dial_buff_ratio)
        buff = dials[0].get_width() * dial_buff_ratio
        dials.set_width(box.get_width() - buff)
        dials.set_max_height(box.get_width() - buff)
        dials.move_to(box)
        for dial in dials:
            dial.set_value(dial.get_random_value())
        self.dials = dials

        self.add(box, dials)

    def random_change_animation(self, lag_factor=0.5, run_time=3.0, **kwargs):
        return LaggedStart(
            *(
                dial.animate_set_value(dial.get_random_value())
                for dial in self.dials
            ), lag_ratio=lag_factor / len(self.dials),
            run_time=run_time,
            **kwargs
        )

    def rotate_all_dials(self, run_time=2, lag_factor=1.0):
        shuffled_dials = list(self.dials)
        random.shuffle(shuffled_dials)
        return LaggedStart(
            *(
                Rotate(dial.needle, TAU, about_point=dial.get_center())
                for dial in shuffled_dials
            ),
            lag_ratio=lag_factor / len(self.dials)
        )



# ----- From _2026/cross_entropy/language_models.py -----

class LanguageModel(VGroup):
    def __init__(
        self,
        block_dims=(4, 2.5, 0.2),
        n_blocks=10,
        block_color=GREY_D,
        block_opacity=0.5,
        block_shading=(0.25, 0.5, 0.2),
        phi=0 * DEG,
        theta=25 * DEG,
        dial_config=dict(
            n_rows=8,
            n_cols=14,
        ),
    ):
        super().__init__()
        # Add blocks
        blocks = VGroup(
            VPrism(*block_dims)
            for n in range(n_blocks)
        )
        blocks.set_fill(block_color, block_opacity)
        blocks.set_stroke(WHITE, 3, 0.5)
        blocks.set_shading(*block_shading)
        blocks.arrange(OUT)
        blocks.move_to(ORIGIN, OUT)

        self.blocks = blocks
        self.add(blocks)

        # Add dials
        front_face = MachineWithDials(
            width=block_dims[0],
            height=block_dims[1],
            **dial_config,
        )
        front_face.box.set_opacity(0)
        front_face.move_to(blocks, OUT)

        self.front_face = front_face
        self.add(front_face)

        # Rotate
        self.rotate(phi, RIGHT, about_edge=OUT)
        self.rotate(theta, UP, about_edge=OUT)
        self.center()

    def forward_pass(self, lag_ratio=0.1, run_time=2):
        over_blocks = self.blocks.copy()
        over_blocks.set_fill(TEAL_E, 0.5)
        return self.blocks.animate.set_fill(TEAL_E).set_anim_args(
            rate_func=there_and_back, lag_ratio=lag_ratio, run_time=run_time
        )


class AmbientModelPredictions(InteractiveScene):
    def construct(self):
        # Add model
        frame = self.frame
        model = LanguageModel()
        model.set_height(2)
        self.add(model)

        # Test
        self.play(model.forward_pass(lag_ratio=0.01))
