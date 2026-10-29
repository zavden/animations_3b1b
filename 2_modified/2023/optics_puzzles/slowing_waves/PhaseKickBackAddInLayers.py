# ==============================================================================
# Scene:      PhaseKickBackAddInLayers
# Source:     videos/_2023/optics_puzzles/slowing_waves.py (lines 796-817)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl PhaseKickBackAddInLayers.py PhaseKickBackAddInLayers -w -m --fps 15
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



# ----- From _2023/optics_puzzles/slowing_waves.py -----

class SlicedWave(Group):
    default_wave_config = dict(
        z_amplitude=0,
        y_amplitude=1,
        wave_len=2.0,
        color=BLUE,
    )
    default_layer_style = dict(
        stroke_width=2.0,
        stroke_color=WHITE,
    )
    default_vect_wave_style = dict(
        stroke_opacity=0.5
    )

    def __init__(
        self,
        axes,
        layer_xs,
        phase_kick_back=0,
        layer_height=4.0,
        damping_per_layer=1.0,
        wave_config = dict(),
        vect_wave_style=dict(),
        layer_style=dict(),
    ):
        self.layer_xs = layer_xs
        self.axes = axes
        wave_kw = merge_dicts_recursively(self.default_wave_config, wave_config)
        vwave_kw = merge_dicts_recursively(self.default_vect_wave_style, vect_wave_style)
        line_kw = merge_dicts_recursively(self.default_layer_style, layer_style)

        self.wave = OscillatingWave(axes, **wave_kw)
        self.vect_wave = OscillatingFieldWave(axes, self.wave, **vwave_kw)
        self.phase_kick_trackers = [
            ValueTracker(phase_kick_back)
            for x in layer_xs
        ]
        self.absorbtion_trackers = [
            ValueTracker(damping_per_layer)
            for x in layer_xs
        ]
        self.layers = VGroup()
        for x in layer_xs:
            line = Line(DOWN, UP, **line_kw)
            line.set_height(layer_height)
            line.move_to(axes.c2p(x, 0))
            self.layers.add(line)

        self.wave.xt_to_yz = self.xt_to_yz

        super().__init__(
            self.wave,
            self.vect_wave,
            self.layers,
            *self.phase_kick_trackers
        )

    def set_layer_xs(self, xs):
        self.layer_xs = xs

    def xt_to_yz(self, x, t):
        phase = np.ones_like(x)
        phase *= TAU * t * self.wave.speed / self.wave.wave_len
        amplitudes = self.wave.y_amplitude * np.ones_like(x)
        for layer_x, pkt, at in zip(self.layer_xs, self.phase_kick_trackers, self.absorbtion_trackers):
            phase[x > layer_x] += pkt.get_value()
            amplitudes[x > layer_x] *= at.get_value()

        y = amplitudes * np.sin(TAU * x / self.wave.wave_len - phase)
        return y, np.zeros_like(x)


class SpeedInMediumFastPart(InteractiveScene):
    z_amplitude = 0
    y_amplitude = 1.0
    color = YELLOW
    wave_len = 3.0
    speed = 1.5
    medium_color = BLUE
    medium_opacity = 0.35
    add_label = True
    run_time = 30
    material_label = "Glass"

    def construct(self):
        # Basic wave
        axes = ThreeDAxes((-12, 12), (-4, 4))
        axes.z_axis.set_stroke(opacity=0)
        axes.y_axis.set_stroke(opacity=0)
        wave = OscillatingWave(
            axes,
            z_amplitude=self.z_amplitude,
            y_amplitude=self.y_amplitude,
            color=self.color,
            wave_len=self.wave_len,
            speed=self.speed,
        )
        vect_wave = OscillatingFieldWave(axes, wave)
        vect_wave.set_stroke(opacity=0.5)

        self.add(axes, wave, vect_wave)

        # Water label
        rect = FullScreenRectangle()
        rect.stretch(0.5, 0, about_edge=RIGHT)
        rect.set_stroke(width=0)
        rect.set_fill(self.medium_color, self.medium_opacity)
        self.add(rect)

        if self.add_label:
            label = Text(self.material_label, font_size=60)
            label.next_to(rect.get_top(), DOWN)
            self.add(label)

        # Propagate
        self.wait(self.run_time)


class PhaseKickBacks(SpeedInMediumFastPart):
    layer_xs = np.arange(0, 8, 1)
    kick_back_value = 0
    axes_config = dict(
        x_range=(-8, 8),
        y_range=(-4, 4),
    )
    line_style = dict()
    wave_config = dict()
    vect_wave_style = dict()
    layer_add_on_run_time = 5
    damping_per_layer = 1.0

    def get_axes(self):
        axes = ThreeDAxes(**self.axes_config)
        axes.z_axis.set_stroke(opacity=0)
        return axes

    def get_layer_xs(self):
        return self.layer_xs

    def get_sliced_wave(self):
        return SlicedWave(
            self.get_axes(),
            self.get_layer_xs(),
            wave_config=self.wave_config,
            vect_wave_style=self.vect_wave_style,
            layer_style=self.line_style,
            phase_kick_back=self.kick_back_value,
            damping_per_layer=self.damping_per_layer,
        )

    def setup(self):
        super().setup()
        self.sliced_wave = self.get_sliced_wave()
        self.add(self.sliced_wave)


class PhaseKickBackAddInLayers(PhaseKickBacks):
    n_layers = 10
    kick_back_value = 0
    target_kick_back = -0.5

    def get_layer_xs(self):
        return np.linspace(0, 8, self.n_layers)

    def construct(self):
        sliced_wave = self.sliced_wave
        lag_kw = dict(run_time=self.layer_add_on_run_time, lag_ratio=0.5)
        self.play(
            LaggedStart(*(
                FadeIn(line, 0.5 * DOWN)
                for line in sliced_wave.layers
            ), **lag_kw),
            LaggedStart(*(
                pkt.animate.set_value(self.target_kick_back)
                for pkt in sliced_wave.phase_kick_trackers
            ), **lag_kw),
        )
        self.wait(8)
