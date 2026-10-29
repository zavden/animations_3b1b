# ==============================================================================
# Scene:      InducedWiggleInCylinder
# Source:     videos/_2023/optics_puzzles/cylinder.py (lines 661-935)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl InducedWiggleInCylinder.py InducedWiggleInCylinder -w -m --fps 15
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


class Polarizer(VGroup):
    def __init__(
        self, axes,
        radius=1.0,
        angle=0,
        stroke_color=GREY_C,
        stroke_width=2,
        fill_color=GREY_C,
        fill_opacity=0.25,
        n_lines=14,
        line_opacity=0.2,
        arrow_stroke_color=WHITE,
        arrow_stroke_width=5,

    ):
        true_radius = radius * axes.z_axis.get_unit_size()
        circle = Circle(
            radius=true_radius,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )

        lines = VGroup(*(
            Line(circle.pfp(a), circle.pfp(1 - a))
            for a in np.arccos(np.linspace(1, -1, n_lines + 2)[1:-1]) / TAU
        ))
        lines.set_stroke(WHITE, 1, opacity=line_opacity)

        arrow = Vector(
            0.5 * true_radius * UP,
            stroke_color=arrow_stroke_color,
            stroke_width=arrow_stroke_width,
        )
        arrow.move_to(circle.get_top(), DOWN)

        super().__init__(
            circle, lines, arrow,
            # So the center works correctly
            VectorizedPoint(circle.get_bottom() + arrow.get_height() * DOWN),
        )
        self.set_flat_stroke(True)
        self.rotate(PI / 2, RIGHT)
        self.rotate(PI / 2, IN)
        self.rotate(angle, RIGHT)
        self.rotate(1 * DEGREES, UP)


class ProbagatingRings(VGroup):
    def __init__(
        self, line,
        n_rings=5,
        start_width=3,
        width_decay_rate=0.1,
        stroke_color=WHITE,
        growth_rate=2.0,
        spacing=0.2,
    ):
        ring = Circle(radius=1e-3, n_components=101)
        ring.set_stroke(stroke_color, start_width)
        ring.apply_matrix(z_to_vector(line.get_vector()))
        ring.move_to(line)
        ring.set_flat_stroke(False)

        super().__init__(*ring.replicate(n_rings))

        self.growth_rate = growth_rate
        self.spacing = spacing
        self.width_decay_rate = width_decay_rate
        self.start_width = start_width
        self.time = 0

        self.add_updater(lambda m, dt: self.update_rings(dt))

    def update_rings(self, dt):
        if dt == 0:
            return
        self.time += dt
        space = 0
        for ring in self.submobjects:
            effective_time = max(self.time - space, 0)
            target_radius = max(effective_time * self.growth_rate, 1e-3)
            ring.scale(target_radius / ring.get_radius())
            space += self.spacing
            ring.set_stroke(width=np.exp(-self.width_decay_rate * effective_time))
        return self


class TwistedRibbon(ParametricSurface):
    def __init__(
        self,
        axes,
        amplitude,
        twist_rate,
        start_point=(0, 0, 0),
        color=WHITE,
        opacity=0.4,
        resolution=(101, 11),
    ):
        super().__init__(
            lambda u, v: axes.c2p(
                u,
                v * amplitude * np.sin(TAU * twist_rate * u),
                v * amplitude * np.cos(TAU * twist_rate * u)
            ),
            u_range=axes.x_range[:2],
            v_range=(-1, 1),
            color=color,
            opacity=opacity,
            resolution=resolution,
            preferred_creation_axis=0,
        )
        self.shift(axes.c2p(*start_point) - axes.get_origin())


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


class InducedWiggleInCylinder(TwistingLightBeam):
    random_seed = 3
    cylinder_radius = 0.5
    wave_config = dict(
        z_amplitude=0.15,
        wave_len=0.5,
        color=get_spectral_color(0.1),
        speed=1.0,
        twist_rate=-1 / 24
    )

    def construct(self):
        # Setup
        frame = self.frame
        frame.reorient(-51, 80, 0).move_to(0.5 * IN).set_height(9)

        axes, plane = get_axes_and_plane(**self.axes_config)
        cylinder = SugarCylinder(axes, self.camera, radius=self.cylinder_radius)
        wave = OscillatingWave(axes, **self.wave_config)
        x_tracker, plane, rod, ball, x_label = slice_group = self.get_slice_group(axes, wave)
        rod = self.get_polarization_rod(axes, wave, x_tracker.get_value, length_mult=5.0)

        axes_labels = Tex("yz", font_size=30)
        axes_labels.rotate(89 * DEGREES, RIGHT)
        axes_labels[0].next_to(axes.y_axis.get_top(), OUT, SMALL_BUFF)
        axes_labels[1].next_to(axes.z_axis.get_zenith(), OUT, SMALL_BUFF)
        axes.add(axes_labels)

        light = GlowDot(radius=4, color=RED)
        light.move_to(axes.c2p(-3, 0, 0))

        polarizer = Polarizer(axes, radius=0.5)
        polarizer.move_to(axes.c2p(-1, 0, 0))

        self.add(axes, cylinder, polarizer, light)

        # Bounces of various points
        randy = self.get_observer(axes.c2p(8, -3, -0.5))
        self.play(
            self.frame.animate.reorient(-86, 70, 0).move_to([1.01, -2.98, -0.79]).set_height(11.33),
            FadeIn(randy, time_span=(0, 1)),
            run_time=2,
        )
        max_y = 0.5 * self.cylinder_radius
        line = VMobject()
        line.set_stroke(RED, 2)
        line.set_flat_stroke(False)
        dot = TrueDot(radius=0.05)
        dot.make_3d()
        for x in range(10):
            point = axes.c2p(
                random.uniform(axes.x_axis.x_min, axes.x_axis.x_max),
                random.uniform(-max_y, -max_y),
                random.uniform(-max_y, -max_y),
            )
            line_points = [light.get_center(), point, randy.eyes.get_top()]
            self.add(dot, cylinder)
            if x == 0:
                dot.move_to(point)
                line.set_points_as_corners(line_points)
                self.play(ShowCreation(line))
            else:
                self.play(
                    line.animate.set_points_as_corners(line_points),
                    dot.animate.move_to(point),
                )
                self.wait()
        self.play(
            FadeOut(line),
            FadeOut(dot),
        )

        # Show slice such that wiggling is in z direction
        x_tracker.set_value(0)
        self.add(wave, cylinder)
        self.play(
            self.frame.animate.reorient(-73, 78, 0).move_to([0.8, -2.22, -0.83]).set_height(10.64),
            light.animate.scale(0.5),
            polarizer.animate.fade(0.5),
            VFadeIn(wave),
        )
        self.wait(4)
        self.add(wave, cylinder)
        self.play(
            FadeIn(plane),
            FadeIn(x_label),
            FadeIn(rod),
        )
        self.play(
            x_tracker.animate.set_value(12),
            run_time=12,
            rate_func=linear,
        )
        self.add(rod, ball, wave, cylinder)

        # Show observer
        line_of_sight = DashedLine(randy.eyes.get_top(), rod.get_center())
        line_of_sight.set_stroke(WHITE, 2)
        line_of_sight.set_flat_stroke(False)

        self.play(
            self.frame.animate.reorient(-60, 79, 0).move_to([0.73, -0.59, -0.39]).set_height(9.63),
            Write(line_of_sight, time_span=(3, 4), lag_ratio=0),
            run_time=5,
        )
        self.wait(2)

        # Show propagating rings
        self.show_propagation(rod)

        # Move to a less favorable spot
        new_line_of_sight = DashedLine(randy.eyes.get_top(), axes.c2p(6, 0, 0))
        new_line_of_sight.match_style(line_of_sight)
        new_line_of_sight.set_flat_stroke(False)

        self.remove(ball)
        self.play(
            x_tracker.animate.set_value(6),
            FadeOut(line_of_sight, time_span=(0, 0.5)),
            run_time=4,
        )
        self.add(ball, wave, cylinder, plane)
        self.play(ShowCreation(new_line_of_sight))
        self.wait(4)

        # New propagations
        self.show_propagation(rod)

        # Show ribbon
        ribbon = TwistedRibbon(
            axes,
            amplitude=wave.z_amplitude,
            twist_rate=wave.twist_rate,
            color=wave.get_color(),
        )

        self.add(ribbon, cylinder)
        self.play(ShowCreation(ribbon, run_time=5))
        self.wait()
        self.play(
            self.frame.animate.reorient(8, 77, 0).move_to([2.01, -0.91, -0.58]).set_height(5.55),
            FadeOut(randy),
            run_time=2,
        )
        self.wait(4)
        self.play(
            self.frame.animate.reorient(-25, 76, 0).move_to([4.22, -1.19, -0.5]),
            x_tracker.animate.set_value(12),
            FadeOut(new_line_of_sight, time_span=(0, 0.5)),
            run_time=3,
        )
        self.wait(4)
        self.play(
            self.frame.animate.reorient(-61, 78, 0).move_to([0.7, 0.05, -0.69]).set_height(9.68),
            FadeIn(randy),
            run_time=3,
        )
        self.play(
            LaggedStartMap(FadeOut, Group(
                line_of_sight, plane, rod, ball, x_label
            ))
        )

        # Show multiple waves
        n_waves = 11
        amp = 0.03
        zs = np.linspace(0.5 - amp, -0.5 + amp, n_waves)
        small_wave_config = dict(self.wave_config)
        small_wave_config["z_amplitude"] = amp

        waves = VGroup(*(
            OscillatingWave(
                axes,
                offset=axes.c2p(0, 0, z)[2] * OUT,
                **small_wave_config
            )
            for z in zs
        ))

        self.remove(ribbon)
        self.play(
            FadeOut(wave),
            VFadeIn(waves),
        )
        self.wait(4)

        # Focus on various x_slices
        x_tracker.set_value(0)
        rods = VGroup(*(
            self.get_polarization_rod(
                axes, lil_wave, x_tracker.get_value,
                length_mult=1,
                stroke_width=2,
            )
            for lil_wave in waves
        ))
        balls = Group(*(
            self.get_wave_ball(lil_wave, x_tracker.get_value, radius=0.025)
            for lil_wave in waves
        ))
        sf = 1.2 * axes.z_axis.get_unit_size() / plane.get_height()
        plane.scale(sf)
        plane[0].scale(1.0 / sf)

        plane.update()
        x_label.update()
        self.add(plane, rods, balls, cylinder, x_label)
        self.play(
            self.frame.animate.reorient(-90, 83, 0).move_to([0.17, -0.37, -0.63]).set_height(7.35).set_anim_args(run_time=3),
            FadeOut(light),
            FadeOut(polarizer),
            FadeIn(plane),
            FadeIn(rods),
            FadeIn(x_label),
            waves.animate.set_stroke(width=0.5, opacity=0.5).set_anim_args(time_span=(1, 2), suspend_mobject_updating=False),
            cylinder.animate.set_opacity(0.05).set_anim_args(time_span=(1, 2))
        )
        self.wait(4)
        self.play(
            self.frame.animate.reorient(-91, 90, 0).move_to([-0.01, -1.39, 0.21]).set_height(3.70),
            x_tracker.animate.set_value(5).set_anim_args(rate_func=linear),
            run_time=12,
        )
        self.wait(4)

        # Show lines of sight
        lines_of_sight = VGroup(*(
            self.get_line_of_sign(rod, randy, stroke_width=0.5)
            for rod in rods
        ))

        self.play(ShowCreation(lines_of_sight[0]))
        self.show_propagation(rods[0])
        for line1, line2 in zip(lines_of_sight, lines_of_sight[1:]):
            self.play(FadeOut(line1), FadeIn(line2), run_time=0.25)
            self.wait(0.25)
        self.wait(4)
        self.play(FadeIn(lines_of_sight[:-1]))
        self.add(lines_of_sight)

        # Move closer and farther
        self.play(
            randy.animate.shift(3.5 * UP + 0.5 * IN),
            run_time=2,
        )
        self.wait(8)
        self.play(
            self.frame.animate.reorient(-91, 89, 0).move_to([-0.05, -3.75, 0.07]).set_height(8.92),
            randy.animate.shift(10 * DOWN),
            run_time=2,
        )
        self.wait(8)

    def show_propagation(self, rod, run_time=10):
        rings = ProbagatingRings(rod, start_width=5)
        self.add(rings)
        self.wait(run_time)
        self.play(VFadeOut(rings))

    def get_observer(self, location=ORIGIN):
        randy = Randolph(mode="pondering")
        randy.look(RIGHT)
        randy.rotate(PI / 2, RIGHT)
        randy.rotate(PI / 2, OUT)
        randy.move_to(location)
        return randy

    def get_line_of_sign(self, rod, observer, stroke_color=WHITE, stroke_width=1):
        line = Line(ORIGIN, 5 * RIGHT)
        line.set_stroke(stroke_color, stroke_width)
        line.add_updater(lambda l: l.put_start_and_end_on(
            observer.eyes.get_top(), rod.get_center()
        ))
        line.set_flat_stroke(False)
        return line
