# ==============================================================================
# Scene:      TwistingLightBeam
# Source:     videos/_2023/optics_puzzles/cylinder.py (lines 96-276)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl TwistingLightBeam.py TwistingLightBeam -w -m --fps 15
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


class SugarCylinder(Cylinder):
    def __init__(
        self, axes, camera,
        radius=0.5,
        color=BLUE_A,
        opacity=0.2,
        shading=(0.5, 0.5, 0.5),
        resolution=(51, 101),
    ):
        super().__init__(
            color=color,
            opacity=opacity,
            resolution=resolution,
            shading=shading,
        )
        self.set_width(2 * axes.z_axis.get_unit_size() * radius)
        self.set_depth(axes.x_axis.get_length(), stretch=True)
        self.rotate(PI / 2, UP)
        self.move_to(axes.get_origin(), LEFT)
        # self.set_shading(*shading)
        self.always_sort_to_camera(camera)


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


class TwistingLightBeam(SimpleLightBeam):
    z_amplitude = 0.5
    wave_len = 2.0
    twist_rate = 1 / 72
    speed = 1.0
    color = YELLOW

    def construct(self):
        # Axes
        axes, plane = get_axes_and_plane(**self.axes_config)
        self.add(axes, plane)

        # Add wave
        wave = OscillatingWave(
            axes,
            z_amplitude=self.z_amplitude,
            wave_len=self.wave_len,
            speed=self.speed,
            color=self.color
        )
        vect_wave = OscillatingFieldWave(axes, wave, **self.oscillating_field_config)

        twist_rate_tracker = ValueTracker(0)

        def update_twist_rate(wave):
            wave.twist_rate = twist_rate_tracker.get_value()
            return wave

        wave.add_updater(update_twist_rate)

        cylinder = SugarCylinder(axes, self.camera, radius=self.z_amplitude)

        self.add(vect_wave, wave)
        self.frame.reorient(-41, 77, 0).move_to([-0.87, 0.9, -0.43])
        self.wait(4)
        cylinder.save_state()
        cylinder.stretch(0, 0, about_edge=RIGHT)
        self.play(
            Restore(cylinder, time_span=(0, 3)),
            twist_rate_tracker.animate.set_value(self.twist_rate).set_anim_args(time_span=(0, 3)),
            self.frame.animate.reorient(-47, 80, 0).move_to([0.06, -0.05, 0.05]).set_height(8.84),
            run_time=6,
        )
        self.wait(2)
        self.play(
            self.frame.animate.reorient(-130, 77, 0).move_to([0.35, -0.36, 0.05]),
            run_time=10,
        )
        self.wait()
        self.play(
            self.frame.animate.reorient(-57, 77, 0).move_to([0.35, -0.36, 0.05]),
            run_time=10,
        )

        # Add rod with oscillating ball
        x_tracker, plane, rod, ball, x_label = self.get_slice_group(axes, wave)
        plane.save_state()
        plane.stretch(0, 2, about_edge=OUT)

        frame_anim = self.frame.animate.reorient(-45, 79, 0)
        frame_anim.move_to([0.63, 0.47, -0.25])
        frame_anim.set_height(10.51)
        frame_anim.set_anim_args(run_time=3)

        self.add(rod, ball, plane, cylinder)
        self.play(
            frame_anim,
            FadeIn(rod),
            Restore(plane),
            FadeIn(x_label),
            UpdateFromAlphaFunc(wave,
                lambda m, a: m.set_stroke(
                    width=interpolate(2, 1, a),
                    opacity=interpolate(1, 0.5, a),
                ),
                run_time=3,
                time_span=(0, 2),
            ),
            UpdateFromAlphaFunc(ball, lambda m, a: m.set_opacity(a)),
        )
        self.wait(9)

        # Show twist down the line of the cylinder
        x_tracker.set_value(0)
        x_tracker.clear_updaters()
        x_tracker.add_updater(lambda m, dt: m.increment_value(0.5 * dt))
        self.add(x_tracker)
        self.wait(5)
        self.play(
            self.frame.animate.reorient(-87, 88, 0).move_to([0.63, 0.47, -0.25]).set_height(10.51),
            run_time=5,
        )
        self.wait(3)
        self.play(
            self.frame.animate.reorient(-43, 78, 0).move_to([0.63, 0.47, -0.25]).set_height(10.51),
            run_time=5
        )
        self.play(
            self.frame.animate.reorient(-34, 80, 0).move_to([1.61, -0.05, 0.3]).set_height(10.30),
            run_time=15,
        )
        self.wait(10)

    def get_slice_group(self, axes, wave):
        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value

        rod = self.get_polarization_rod(axes, wave, get_x)
        ball = self.get_wave_ball(wave, get_x)
        plane = self.get_slice_plane(axes, get_x)
        x_label = self.get_plane_label(axes, plane)

        return Group(x_tracker, plane, rod, ball, x_label)

    def get_polarization_rod(self, axes, wave, get_x, stroke_color=None, length_mult=2.0, stroke_width=3):
        rod = Line(IN, OUT)
        rod.set_stroke(
            color=stroke_color or wave.get_stroke_color(),
            width=stroke_width,
        )
        rod.set_flat_stroke(False)
        wave_z = axes.z_axis.p2n(wave.get_center())
        wave_y = axes.y_axis.p2n(wave.get_center())

        def update_rod(rod):
            x = get_x()
            rod.put_start_and_end_on(
                axes.c2p(x, wave_y, wave_z - length_mult * wave.z_amplitude),
                axes.c2p(x, wave_y, wave_z + length_mult * wave.z_amplitude),
            )
            rod.rotate(TAU * wave.twist_rate * x, RIGHT)
            return rod

        rod.add_updater(update_rod)
        return rod

    def get_wave_ball(self, wave, get_x, radius=0.075):
        ball = TrueDot(radius=radius)
        ball.make_3d()
        ball.set_color(wave.get_color())

        def update_ball(ball):
            ball.move_to(wave.offset + wave.xt_to_point(get_x(), wave.time))
            return ball

        ball.add_updater(update_ball)
        return ball

    def get_slice_plane(self, axes, get_x):
        plane = Square(side_length=axes.z_axis.get_length())
        plane.set_fill(BLUE, 0.25)
        plane.set_stroke(width=0)
        circle = Circle(
            radius=axes.z_axis.get_unit_size() * self.z_amplitude,
            n_components=100,
        )
        circle.set_flat_stroke(False)
        circle.set_stroke(BLACK, 1)
        plane.add(circle)
        plane.rotate(PI / 2, UP)
        plane.add_updater(lambda m: m.move_to(axes.c2p(get_x(), 0, 0)))
        return plane

    def get_plane_label(self, axes, plane, font_size=24, color=GREY_B):
        x_label = Tex("x = 0.00", font_size=font_size)
        x_label.set_fill(color)
        x_label.value_mob = x_label.make_number_changeable("0.00")
        x_label.rotate(PI / 2, RIGHT)
        x_label.rotate(PI / 2, IN)

        def update_x_label(x_label):
            x_value = x_label.value_mob
            x_value.set_value(axes.x_axis.p2n(plane.get_center()))
            x_value.rotate(PI / 2, RIGHT)
            x_value.rotate(PI / 2, IN)
            x_value.next_to(x_label[1], DOWN, SMALL_BUFF)
            x_label.next_to(plane, OUT)
            return x_label

        x_label.add_updater(update_x_label)
        return x_label
