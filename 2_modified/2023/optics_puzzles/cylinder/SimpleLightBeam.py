# ==============================================================================
# Scene:      SimpleLightBeam
# Source:     videos/_2023/optics_puzzles/cylinder.py (lines 8-93)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl SimpleLightBeam.py SimpleLightBeam -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField
from matplotlib import colormaps
from typing import TYPE_CHECKING


# ----- From _2023/optics_puzzles/objects.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3


spectral_cmap = colormaps.get_cmap("Spectral")


def get_spectral_color(alpha):
    return Color(rgb=spectral_cmap(alpha)[:3])


def get_axes_and_plane(
    x_range=(0, 24),
    y_range=(-1, 1),
    z_range=(-1, 1),
    x_unit=1,
    y_unit=2,
    z_unit=2,
    origin_point=5 * LEFT,
    axes_opacity=0.5,
    plane_line_style=dict(
        stroke_color=GREY_C,
        stroke_width=1,
        stroke_opacity=0.5
    ),
):
    axes = ThreeDAxes(
        x_range=x_range,
        y_range=y_range,
        z_range=z_range,
        width=x_unit * (x_range[1] - x_range[0]),
        height=y_unit * (y_range[1] - y_range[0]),
        depth=z_unit * (z_range[1] - z_range[0]),
    )
    axes.shift(origin_point - axes.get_origin())
    axes.set_opacity(axes_opacity)
    axes.set_flat_stroke(False)
    plane = NumberPlane(
        axes.x_range, axes.y_range,
        width=axes.x_axis.get_length(),
        height=axes.y_axis.get_length(),
        background_line_style=plane_line_style,
        axis_config=dict(stroke_width=0),
    )
    plane.shift(axes.get_origin() - plane.get_origin())
    plane.set_flat_stroke(False)

    return axes, plane


class OscillatingWave(VMobject):
    def __init__(
        self,
        axes,
        y_amplitude=0.0,
        z_amplitude=0.75,
        z_phase=0.0,
        y_phase=0.0,
        wave_len=0.5,
        twist_rate=0.0,  # In rotations per unit distance
        speed=1.0,
        sample_resolution=0.005,
        stroke_width=2,
        offset=ORIGIN,
        color=None,
        **kwargs,
    ):
        self.axes = axes
        self.y_amplitude = y_amplitude
        self.z_amplitude = z_amplitude
        self.z_phase = z_phase
        self.y_phase = y_phase
        self.wave_len = wave_len
        self.twist_rate = twist_rate
        self.speed = speed
        self.sample_resolution = sample_resolution
        self.offset = offset

        super().__init__(**kwargs)

        color = color or self.get_default_color(wave_len)
        self.set_stroke(color, stroke_width)
        self.set_flat_stroke(False)

        self.time = 0
        self.clock_is_stopped = False

        self.add_updater(lambda m, dt: m.update_points(dt))

    def update_points(self, dt):
        if not self.clock_is_stopped:
            self.time += dt
        xs = np.arange(
            self.axes.x_axis.x_min,
            self.axes.x_axis.x_max,
            self.sample_resolution
        )
        self.set_points_as_corners(
            self.offset + self.xt_to_point(xs, self.time)
        )

    def stop_clock(self):
        self.clock_is_stopped = True

    def start_clock(self):
        self.clock_is_stopped = False

    def xt_to_yz(self, x, t):
        phase = TAU * t * self.speed / self.wave_len
        y_outs = self.y_amplitude * np.sin(TAU * x / self.wave_len - phase - self.y_phase)
        z_outs = self.z_amplitude * np.sin(TAU * x / self.wave_len - phase - self.z_phase)
        twist_angles = x * self.twist_rate * TAU
        y = np.cos(twist_angles) * y_outs - np.sin(twist_angles) * z_outs
        z = np.sin(twist_angles) * y_outs + np.cos(twist_angles) * z_outs

        return y, z

    def xt_to_point(self, x, t):
        y, z = self.xt_to_yz(x, t)
        return self.axes.c2p(x, y, z)

    def get_default_color(self, wave_len):
        return get_spectral_color(inverse_interpolate(
            1.5, 0.5, wave_len
        ))


class GraphAsVectorField(VectorField):
    def __init__(
        self,
        axes: Axes | ThreeDAxes,
        # Maps x to y, or x to (y, z)
        graph_func: Callable[[VectN], VectN] | Callable[[VectN], Tuple[VectN, VectN]],
        x_density=10.0,
        max_vect_len=np.inf,
        **kwargs,
    ):
        self.sample_xs = np.arange(axes.x_axis.x_min, axes.x_axis.x_max, 1.0 / x_density)
        self.axes = axes

        def vector_func(points):
            output = graph_func(self.sample_xs)
            if isinstance(axes, ThreeDAxes):
                graph_points = axes.c2p(self.sample_xs, *output)
            else:
                graph_points = axes.c2p(self.sample_xs, output)
            base_points = axes.x_axis.n2p(self.sample_xs)
            return graph_points - base_points

        super().__init__(
            func=vector_func,
            max_vect_len=max_vect_len,
            **kwargs
        )
        always(self.update_vectors)

    def reset_sample_points(self):
        self.sample_points = self.get_sample_points()

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.axes.x_axis.n2p(self.sample_xs)


class OscillatingFieldWave(GraphAsVectorField):
    def __init__(self, axes, wave, **kwargs):
        self.wave = wave
        if "stroke_color" not in kwargs:
            kwargs["stroke_color"] = wave.get_color()
        super().__init__(
            axes=axes,
            graph_func=lambda x: wave.xt_to_yz(x, wave.time),
            **kwargs
        )

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.wave.offset + self.axes.x_axis.n2p(self.sample_xs)



# ----- From _2023/optics_puzzles/cylinder.py -----

class SimpleLightBeam(InteractiveScene):
    default_frame_orientation = (-33, 85)
    axes_config = dict()
    z_amplitude = 0.5
    wave_len = 2.0
    speed = 1.0
    color = YELLOW
    oscillating_field_config = dict(
        stroke_opacity=0.5,
        stroke_width=2,
        tip_width_ratio=1
    )

    def construct(self):
        axes, plane = get_axes_and_plane(**self.axes_config)
        self.add(axes, plane)

        # Introduce wave
        wave = OscillatingWave(
            axes,
            z_amplitude=self.z_amplitude,
            wave_len=self.wave_len,
            speed=self.speed,
            color=self.color
        )
        vect_wave = OscillatingFieldWave(axes, wave, **self.oscillating_field_config)

        def update_wave(wave):
            st = self.time * self.speed  # Suppressor threshold
            points = wave.get_points().copy()
            xs = axes.x_axis.p2n(points)
            suppressors = np.clip(smooth(st - xs), 0, 1)
            points[:, 1] *= suppressors
            points[:, 2] *= suppressors
            wave.set_points(points)
            return wave

        wave.add_updater(update_wave)
        vect_wave.add_updater(update_wave)

        self.add(wave)
        self.play(
            self.frame.animate.reorient(-98, 77, 0).move_to([-0.87, 0.9, -0.43]),
            run_time=8,
        )
        self.add(vect_wave, wave)
        self.play(
            VFadeIn(vect_wave),
            self.frame.animate.reorient(-10, 77, 0).move_to([-0.87, 0.9, -0.43]),
            run_time=4
        )
        self.wait(3)

        # Label directions
        z_label = Tex("z")
        z_label.rotate(PI / 2, RIGHT)
        z_label.next_to(axes.z_axis, OUT)

        y_label = Tex("y")
        y_label.rotate(PI / 2, RIGHT)
        y_label.next_to(axes.y_axis, UP + OUT)

        x_label = VGroup(
            TexText("$x$-direction"),
            Vector(RIGHT, stroke_color=WHITE),
        )
        x_label.arrange(RIGHT)
        x_label.set_flat_stroke(False)
        x_label.rotate(PI / 2, RIGHT)
        x_label.next_to(z_label, RIGHT, buff=2.0)
        x_label.match_z(axes.c2p(0, 0, 0.75))

        self.play(
            FadeIn(z_label, 0.5 * OUT),
            FadeIn(y_label, 0.5 * UP),
        )
        self.wait(3)
        self.play(
            Write(x_label[0]),
            GrowArrow(x_label[1]),
        )
        self.play(
            self.frame.animate.reorient(-41, 77, 0).move_to([-0.87, 0.9, -0.43]),
            run_time=12,
        )
        self.wait(6)
