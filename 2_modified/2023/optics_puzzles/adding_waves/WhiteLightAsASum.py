# ==============================================================================
# Scene:      WhiteLightAsASum
# Source:     videos/_2023/optics_puzzles/adding_waves.py (lines 5-101)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl WhiteLightAsASum.py WhiteLightAsASum -w -m --fps 15
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


class MeanWave(VMobject):
    def __init__(self, waves, **kwargs):
        self.waves = waves
        self.offset = np.array(ORIGIN)
        self.time = 0
        super().__init__(**kwargs)
        self.set_flat_stroke(False)
        self.add_updater(lambda m, dt: m.update_points(dt))

    def update_points(self, dt):
        for wave in self.waves:
            wave.update_points(dt)

        self.time += dt

        points = sum(wave.get_points() for wave in self.waves) / len(self.waves)
        self.set_points(points)

    def xt_to_yz(self, x, t):
        return tuple(
            np.array([
                wave.xt_to_yz(x, t)[i]
                for wave in self.waves
            ]).mean(0)
            for i in (0, 1)
        )


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



# ----- From _2023/optics_puzzles/adding_waves.py -----

class WhiteLightAsASum(InteractiveScene):
    def construct(self):
        # Initial orientation
        frame = self.frame
        frame.reorient(0, 90)

        # Create axes
        n_colors = 15
        axes_width = 9.0
        x_max = 8
        spectral_axes = VGroup(*(
            ThreeDAxes((0, x_max), (-1, 1), (-1, 1))
            for _ in range(n_colors)
        ))
        spectral_axes.set_width(axes_width)
        spectral_axes.arrange(UP, buff=0.05)

        white_axes = ThreeDAxes((0, x_max), (-1, 1), (-1, 1))
        white_axes.set_width(axes_width)
        white_axes.shift(2 * DOWN)
        spectral_axes.next_to(white_axes, UP)

        all_axes = [white_axes, *spectral_axes]
        for axes in all_axes:
            axes.y_axis.set_opacity(0)

        for axes in spectral_axes:
            axes.z_axis.stretch(0.5, 2)

        white_axes.z_axis.stretch(1.5, 2)

        # Create individual waves
        white_parts = VGroup()
        spectral_waves = VGroup()
        alphas = np.linspace(0.0, 1.0, n_colors)
        for alpha, s_axes in zip(alphas, spectral_axes):
            wave_len = interpolate(1.0, 2.0, alpha)
            for axes, group in [(s_axes, spectral_waves), (white_axes, white_parts)]:
                wave = OscillatingWave(
                    axes,
                    y_amplitude=0,
                    z_amplitude=1,
                    wave_len=wave_len,
                    color=get_spectral_color(1 - alpha)
                )
                group.add(wave)

        # Show white wave
        white_wave = MeanWave(white_parts)
        white_wave.set_stroke(width=1)
        white_vects = OscillatingFieldWave(white_axes, white_wave, tip_width_ratio=3)
    
        self.add(white_axes, white_wave, white_vects)
        self.wait(5)

        # Show spectral parts
        symbols = Tex("=" + "+" * (n_colors - 1))
        symbols.scale(2)
        symbols.rotate(90 * DEGREES)
        for symbol, a1, a2 in zip(symbols, all_axes, all_axes[1:]):
            symbol.move_to(VGroup(a1, a2))

        spectral_vect_waves = VGroup()
        for sa, sw in zip(spectral_axes, spectral_waves):
            vwave = OscillatingFieldWave(sa, sw, tip_width_ratio=3)
            sw.set_stroke(width=1)
            spectral_vect_waves.add(vwave)

        self.play(
            frame.animate.reorient(50, 65, 0).move_to([0.6, 2.9, -0.16]).set_height(11).set_anim_args(run_time=3),
            LaggedStartMap(FadeIn, spectral_axes),
            LaggedStartMap(VFadeIn, spectral_waves),
            LaggedStartMap(VFadeIn, spectral_vect_waves),
            LaggedStartMap(FadeIn, symbols),
        )
        self.play(
            self.frame.animate.reorient(19, 65, 0).move_to([0.6, 2.9, -0.16]).set_height(11.00),
            run_time=8
        )
        return

        # Scrap
        arrows = VGroup(*(
            Arrow(
                sa.get_left(),
                interpolate(white_axes.get_corner(UR), white_axes.get_corner(DR), alpha),
                buff=0.3,
                stroke_color=wave.get_color()
            )
            for sa, wave, alpha in zip(
                spectral_axes,
                spectral_waves,
                np.linspace(0, 1, n_colors),
            )
        ))

        pass
