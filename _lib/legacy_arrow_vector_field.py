"""VectorField and StreamLines with the OLD arrow-based manimgl API (before September 2024).

Origin: manimgl (https://github.com/3b1b/manim), file manimlib/mobject/vector_field.py as it
was just before commit 217eb6b4 (21 Sep 2024, "Move new VectorField from optics projects into
main repo"), that is `git show 217eb6b4^:manimlib/mobject/vector_field.py`. MIT license,
Copyright (c) 2020-2026 3Blue1Brown LLC (the notice that manimgl's LICENSE.md carries).

Why it exists: _2021/matrix_exp.py (and probably other 2021-2023 videos) uses this interface:

    VectorField(func, coordinate_system, step_multiple=.., magnitude_range=.., length_func=..,
                opacity=.., vector_config={"thickness": ..})      # a VGroup of arrows
    StreamLines(func, coordinate_system, step_multiple=.., ...)    # func(x, y) -> (x', y')

where `func` receives the LOOSE coordinates (`func(x, y)`) and returns a tuple. The current VectorField
(since Nov 2024) is something else: a single VMobject with strokes, `density` instead of `step_multiple`, without
`vector_config`/`length_func`/`opacity`, and its `func` is vectorized (it receives an array of coordinates).
The current StreamLines also requires a vectorized `func` and solves an ODE. They are not compatible, and the
scenes iterate over the arrows (`for v in vector_field: v.get_start()`, `GrowArrow`...).

What it covers: VectorField and StreamLines from commit 217eb6b4^, without behavior changes.
It does not define AnimatedStreamLines: manimgl's current one works with these StreamLines (it only needs
`line.virtual_time`).

Adaptations to the current manimgl (v1.7.2):
  - The arrows are created with `FillArrow` from manim_imports_ext (the `Arrow` of that time already measured
    `thickness` on the new scale; the 2021 code passes `thickness` on FillArrow's old scale).
  - `from legacy_arrow_vector_field import VectorField, StreamLines` must go AFTER
    `from manim_imports_ext import *`, to override manimgl's names.

It patches nothing globally. The scenes that need them import them explicitly."""
from __future__ import annotations

import itertools as it

import numpy as np

from manimlib.animation.indication import VShowPassingFlash  # noqa: F401  (same dependency as the original)
from manimlib.constants import WHITE
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.color import rgb_to_color
from manimlib.utils.dict_ops import merge_dicts_recursively
from manimlib.utils.simple_functions import sigmoid
from manimlib.utils.space_ops import get_norm
from manimlib.mobject.vector_field import get_rgb_gradient_function
from manimlib.mobject.vector_field import get_vectorized_rgb_gradient_function


def get_sample_points_from_coordinate_system(coordinate_system, step_multiple):
    ranges = []
    for range_args in coordinate_system.get_all_ranges():
        _min, _max, step = range_args
        step *= step_multiple
        ranges.append(np.arange(_min, _max + step, step))
    return it.product(*ranges)


class VectorField(VGroup):
    def __init__(
        self,
        func,
        coordinate_system,
        step_multiple: float = 0.5,
        magnitude_range=(0, 2),
        color_map: str = "3b1b_colormap",
        # Takes in actual norm, spits out displayed norm
        length_func=lambda norm: 0.45 * sigmoid(norm),
        opacity: float = 1.0,
        vector_config: dict = dict(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.func = func
        self.coordinate_system = coordinate_system
        self.step_multiple = step_multiple
        self.magnitude_range = magnitude_range
        self.color_map = color_map
        self.length_func = length_func
        self.opacity = opacity
        self.vector_config = dict(vector_config)

        self.value_to_rgb = get_rgb_gradient_function(
            *self.magnitude_range, self.color_map,
        )

        samples = get_sample_points_from_coordinate_system(
            coordinate_system, self.step_multiple
        )
        self.add(*(
            self.get_vector(coords)
            for coords in samples
        ))

    def get_vector(self, coords, **kwargs):
        # Late import: manim_imports_ext imports the whole of manimlib and defines FillArrow
        from manim_imports_ext import FillArrow

        vector_config = merge_dicts_recursively(
            self.vector_config,
            kwargs
        )

        output = np.array(self.func(*coords), dtype=float)
        norm = get_norm(output)
        if norm > 0:
            output *= self.length_func(norm) / norm

        origin = self.coordinate_system.get_origin()
        _input = self.coordinate_system.c2p(*coords)
        _output = self.coordinate_system.c2p(*output)

        vect = FillArrow(
            origin, _output, buff=0,
            **vector_config
        )
        vect.shift(_input - origin)
        vect.set_color(
            rgb_to_color(self.value_to_rgb(norm)),
            opacity=self.opacity,
        )
        return vect


class StreamLines(VGroup):
    def __init__(
        self,
        func,
        coordinate_system,
        step_multiple: float = 0.5,
        n_repeats: int = 1,
        noise_factor: float | None = None,
        # Config for drawing lines
        dt: float = 0.05,
        arc_len: float = 3,
        max_time_steps: int = 200,
        n_samples_per_line: int = 10,
        cutoff_norm: float = 15,
        # Style info
        stroke_width: float = 1.0,
        stroke_color=WHITE,
        stroke_opacity: float = 1,
        color_by_magnitude: bool = True,
        magnitude_range=(0, 2.0),
        taper_stroke_width: bool = False,
        color_map: str = "3b1b_colormap",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.func = func
        self.coordinate_system = coordinate_system
        self.step_multiple = step_multiple
        self.n_repeats = n_repeats
        self.noise_factor = noise_factor
        self.dt = dt
        self.arc_len = arc_len
        self.max_time_steps = max_time_steps
        self.n_samples_per_line = n_samples_per_line
        self.cutoff_norm = cutoff_norm
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.stroke_opacity = stroke_opacity
        self.color_by_magnitude = color_by_magnitude
        self.magnitude_range = magnitude_range
        self.taper_stroke_width = taper_stroke_width
        self.color_map = color_map

        self.draw_lines()
        self.init_style()

    def point_func(self, point):
        in_coords = self.coordinate_system.p2c(point)
        out_coords = self.func(*in_coords)
        return self.coordinate_system.c2p(*out_coords)

    def draw_lines(self) -> None:
        lines = []
        origin = self.coordinate_system.get_origin()
        for point in self.get_start_points():
            points = [point]
            total_arc_len = 0
            time = 0
            for x in range(self.max_time_steps):
                time += self.dt
                last_point = points[-1]
                new_point = last_point + self.dt * (self.point_func(last_point) - origin)
                points.append(new_point)
                total_arc_len += get_norm(new_point - last_point)
                if get_norm(last_point) > self.cutoff_norm:
                    break
                if total_arc_len > self.arc_len:
                    break
            line = VMobject()
            line.virtual_time = time
            step = max(1, int(len(points) / self.n_samples_per_line))
            line.set_points_as_corners(points[::step])
            line.make_smooth(approx=True)
            lines.append(line)
        self.set_submobjects(lines)

    def get_start_points(self):
        cs = self.coordinate_system
        sample_coords = get_sample_points_from_coordinate_system(
            cs, self.step_multiple,
        )

        noise_factor = self.noise_factor
        if noise_factor is None:
            noise_factor = cs.x_range[2] * self.step_multiple * 0.5

        return np.array([
            cs.c2p(*coords) + noise_factor * np.random.random(3)
            for n in range(self.n_repeats)
            for coords in sample_coords
        ])

    def init_style(self) -> None:
        if self.color_by_magnitude:
            values_to_rgbs = get_vectorized_rgb_gradient_function(
                *self.magnitude_range, self.color_map,
            )
            cs = self.coordinate_system
            for line in self.submobjects:
                norms = [
                    get_norm(self.func(*cs.p2c(point)))
                    for point in line.get_points()
                ]
                rgbs = values_to_rgbs(norms)
                rgbas = np.zeros((len(rgbs), 4))
                rgbas[:, :3] = rgbs
                rgbas[:, 3] = self.stroke_opacity
                line.set_rgba_array(rgbas, "stroke_rgba")
        else:
            self.set_stroke(self.stroke_color, opacity=self.stroke_opacity)

        if self.taper_stroke_width:
            width = [0, self.stroke_width, 0]
        else:
            width = self.stroke_width
        self.set_stroke(width=width)
