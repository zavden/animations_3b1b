"""VectorField and TimeVaryingVectorField with the OLD manimgl API.

Origin: manimgl (https://github.com/3b1b/manim), file manimlib/mobject/vector_field.py as it
was at commit 217eb6b4 (21 Sep 2024, "Move new VectorField from optics projects into
main repo"), that is `git show 217eb6b4:manimlib/mobject/vector_field.py`. MIT license,
Copyright (c) 2020-2026 3Blue1Brown LLC (the notice that manimgl's LICENSE.md carries).

Why it exists: the code of _2023/optics_puzzles (and probably other 2022-2023 videos)
uses the interface prior to the November 2024 rewrite (commits 64ae1364, 0ad5a0e7,
55b12c90, 90ab2f64, c6b9826f):

    VectorField(func, x_density=.., y_density=.., z_density=.., width=.., height=.., depth=..,
                center=.., sample_points=.., max_vect_len=.., norm_to_opacity_func=..,
                norm_to_rgb_func=.., stroke_color=.., stroke_width=.., ...)
    TimeVaryingVectorField(time_func, **kwargs)

and its classes (ChargeBasedVectorField, GraphAsVectorField, WaveIntoMedium...) override
get_sample_points() and call update_vectors(). The current VectorField requires a
`coordinate_system`, works in the coordinates of that system and renamed/removed those arguments,
so it is not compatible.

What it covers (same API as commit 217eb6b4):
  - VectorField(VMobject): func receives an (N, 3) array of scene points and returns an
    (N, 3) array; sample_points by grid (center/width/height/depth + x/y/z_density) or
    passed by hand; max_vect_len with tanh; min_drawn_norm; norm_to_opacity_func and
    norm_to_rgb_func; get_sample_points / set_sample_points / update_vectors / set_stroke(width=..).
  - TimeVaryingVectorField(time_func(points, t), **kwargs): updates the time with dt and
    calls update_vectors on every frame.
It does NOT cover OldVectorField (the Arrow-based class with coordinate_system) nor the new
VectorField: those remain in manimlib.

Adaptations to the current manimgl (v1.7.2, 2026):
  - update_vectors writes inside `with self.data.being_written():` instead of calling
    note_changed_data() (the current manimgl counts writes through views).
  - self.set_joint_type('no_joint') was removed: that method no longer exists (joint_roundness=0, the
    default, is equivalent to no joints).
  - The imports were adjusted to current paths (always comes from mobject_update_utils).

It patches nothing globally: it only defines these two classes. The scenes that need them import them
explicitly:
    from legacy_vector_field import VectorField, TimeVaryingVectorField"""
from __future__ import annotations

import numpy as np

from manimlib.constants import BLUE, ORIGIN
from manimlib.mobject.mobject_update_utils import always
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.iterables import cartesian_product


class VectorField(VMobject):
    def __init__(
        self,
        func,
        stroke_color=BLUE,
        stroke_opacity: float = 1.0,
        center=ORIGIN,
        sample_points=None,
        x_density: float = 2.0,
        y_density: float = 2.0,
        z_density: float = 2.0,
        width: float = 14.0,
        height: float = 8.0,
        depth: float = 0.0,
        stroke_width: float = 2,
        tip_width_ratio: float = 4,
        tip_len_to_width: float = 0.01,
        max_vect_len: float | None = None,
        min_drawn_norm: float = 1e-2,
        flat_stroke: bool = False,
        norm_to_opacity_func=None,
        norm_to_rgb_func=None,
        **kwargs
    ):
        self.func = func
        self.stroke_width = stroke_width
        self.tip_width_ratio = tip_width_ratio
        self.tip_len_to_width = tip_len_to_width
        self.min_drawn_norm = min_drawn_norm
        self.norm_to_opacity_func = norm_to_opacity_func
        self.norm_to_rgb_func = norm_to_rgb_func

        if max_vect_len is not None:
            self.max_vect_len = max_vect_len
        else:
            densities = np.array([x_density, y_density, z_density])
            dims = np.array([width, height, depth])
            self.max_vect_len = 1.0 / densities[dims > 0].mean()

        if sample_points is None:
            self.sample_points = self.get_sample_points(
                center, width, height, depth,
                x_density, y_density, z_density
            )
        else:
            self.sample_points = sample_points

        self.init_base_stroke_width_array(len(self.sample_points))

        super().__init__(
            stroke_color=stroke_color,
            stroke_opacity=stroke_opacity,
            flat_stroke=flat_stroke,
            **kwargs
        )

        n_samples = len(self.sample_points)
        self.set_points(np.zeros((8 * n_samples - 1, 3)))
        self.set_stroke(width=stroke_width)
        # (set_joint_type('no_joint') no longer exists: joint_roundness=0 is the default)
        self.update_vectors()

    def get_sample_points(
        self,
        center: np.ndarray,
        width: float,
        height: float,
        depth: float,
        x_density: float,
        y_density: float,
        z_density: float
    ) -> np.ndarray:
        to_corner = np.array([width / 2, height / 2, depth / 2])
        spacings = 1.0 / np.array([x_density, y_density, z_density])
        to_corner = spacings * (to_corner / spacings).astype(int)
        lower_corner = center - to_corner
        upper_corner = center + to_corner + spacings
        return cartesian_product(*(
            np.arange(low, high, space)
            for low, high, space in zip(lower_corner, upper_corner, spacings)
        ))

    def init_base_stroke_width_array(self, n_sample_points):
        arr = np.ones(8 * n_sample_points - 1)
        arr[4::8] = self.tip_width_ratio
        arr[5::8] = self.tip_width_ratio * 0.5
        arr[6::8] = 0
        arr[7::8] = 0
        self.base_stroke_width_array = arr

    def set_sample_points(self, sample_points):
        self.sample_points = sample_points
        return self

    def set_stroke(self, color=None, width=None, opacity=None, behind=None, flat=None, recurse=True):
        super().set_stroke(color, None, opacity, behind, flat, recurse)
        if width is not None:
            self.set_stroke_width(float(width))
        return self

    def set_stroke_width(self, width: float):
        if self.get_num_points() > 0:
            self.data['stroke_width'] = width * self.base_stroke_width_array[:, np.newaxis]
            self.stroke_width = width
        return self

    def update_vectors(self):
        tip_width = self.tip_width_ratio * self.stroke_width
        tip_len = self.tip_len_to_width * tip_width
        samples = self.sample_points

        # Get raw outputs and lengths
        outputs = self.func(samples)
        norms = np.linalg.norm(outputs, axis=1)[:, np.newaxis]

        # How long should the arrows be drawn?
        max_len = self.max_vect_len
        if max_len < np.inf:
            drawn_norms = max_len * np.tanh(norms / max_len)
        else:
            drawn_norms = norms

        # What's the distance from the base of an arrow to
        # the base of its head?
        dist_to_head_base = np.clip(drawn_norms - tip_len, 0, np.inf)

        unit_outputs = np.zeros_like(outputs)
        np.true_divide(outputs, norms, out=unit_outputs, where=(norms > self.min_drawn_norm))

        # Writing through views of the data (current manimgl)
        with self.data.being_written():
            # Set all points
            points = self.get_points()
            points[0::8] = samples
            points[2::8] = samples + dist_to_head_base * unit_outputs
            points[4::8] = points[2::8]
            points[6::8] = samples + drawn_norms * unit_outputs
            for i in (1, 3, 5):
                points[i::8] = 0.5 * (points[i - 1::8] + points[i + 1::8])
            points[7::8] = points[6:-1:8]

            # Adjust stroke widths
            width_arr = self.stroke_width * self.base_stroke_width_array
            width_scalars = np.clip(drawn_norms / tip_len, 0, 1)
            width_scalars = np.repeat(width_scalars, 8)[:-1]
            self.get_stroke_widths()[:] = width_scalars * width_arr

            # Potentially adjust opacity and color
            if self.norm_to_opacity_func is not None:
                self.get_stroke_opacities()[:] = self.norm_to_opacity_func(
                    np.repeat(norms, 8)[:-1]
                )
            if self.norm_to_rgb_func is not None:
                self.get_stroke_colors()
                self.data['stroke_rgba'][:, :3] = self.norm_to_rgb_func(
                    np.repeat(norms, 8)[:-1]
                )
        return self


class TimeVaryingVectorField(VectorField):
    def __init__(
        self,
        # Takes in an array of points and a float for time
        time_func,
        **kwargs
    ):
        self.time = 0
        super().__init__(func=lambda p: time_func(p, self.time), **kwargs)
        self.add_updater(lambda m, dt: m.increment_time(dt))
        always(self.update_vectors)

    def increment_time(self, dt):
        self.time += dt
