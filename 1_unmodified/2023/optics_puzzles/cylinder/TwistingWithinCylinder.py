# ==============================================================================
# Scene:      TwistingWithinCylinder
# Source:     videos/_2023/optics_puzzles/cylinder.py (lines 291-658)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl TwistingWithinCylinder.py TwistingWithinCylinder -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from matplotlib import colormaps


# ----- From _2023/optics_puzzles/objects.py -----

spectral_cmap = colormaps.get_cmap("Spectral")


def get_spectral_color(alpha):
    return Color(rgb=spectral_cmap(alpha)[:3])


def get_spectral_colors(n_colors, lower_bound=0, upper_bound=1):
    return [
        get_spectral_color(alpha)
        for alpha in np.linspace(lower_bound, upper_bound, n_colors)
    ]


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


def get_twist(wave_length, distance):
    # 350 is arbitrary. Change
    return distance / (wave_length / 350)**2


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



# ----- From _2023/optics_puzzles/cylinder.py -----

class TwistingWithinCylinder(InteractiveScene):
    default_frame_orientation = (-40, 80)
    n_lines = 11
    pause_down_the_tube = True

    def construct(self):
        # Reference objects
        frame = self.frame
        axes, plane = get_axes_and_plane(
            x_range=(0, 8),
            y_range=(-2, 2),
            z_range=(-2, 2),
            y_unit=1,
            z_unit=1,
            origin_point=3 * LEFT
        )
        cylinder = SugarCylinder(axes, self.camera, radius=0.5)

        self.add(plane, axes)
        self.add(cylinder)

        # Light lines
        lines = VGroup()
        colors = get_spectral_colors(self.n_lines)
        for color in colors:
            line = Line(ORIGIN, 0.95 * OUT)
            line.set_flat_stroke(False)
            line.set_stroke(color, 2)
            lines.add(line)

        lines.arrange(DOWN, buff=0.1)
        lines.move_to(cylinder.get_left())

        # Add polarizer to the start
        light = GlowDot(color=WHITE, radius=3)
        light.move_to(axes.c2p(-3, 0, 0))
        polarizer = Polarizer(axes, radius=0.6)
        polarizer.move_to(axes.c2p(-1, 0, 0))
        polarizer_label = Text("Linear polarizer", font_size=36)
        polarizer_label.rotate(PI / 2, RIGHT)
        polarizer_label.rotate(PI / 2, IN)
        polarizer_label.next_to(polarizer, OUT)
        frame.reorient(-153, 79, 0)
        frame.shift(1.0 * IN)

        self.play(GrowFromCenter(light))
        self.play(
            Write(polarizer_label),
            FadeIn(polarizer, IN),
            light.animate.shift(LEFT).set_anim_args(time_span=(1, 3)),
            self.frame.animate.reorient(-104, 77, 0).center().set_anim_args(run_time=3),
        )

        # Many waves
        waves = VGroup(*(
            OscillatingWave(
                axes,
                z_amplitude=0.3,
                wave_len=wave_len,
                color=line.get_color(),
                offset=LEFT + line.get_y() * UP
            )
            for line, wave_len in zip(
                lines,
                np.linspace(2.0, 0.5, len(lines))
            )
        ))
        waves.set_stroke(width=1)
        superposition = MeanWave(waves)
        superposition.set_stroke(WHITE, 2)
        superposition.add_updater(lambda m: m.stretch(4, 2, about_point=ORIGIN))

        self.play(
            VFadeIn(superposition),
            FadeOut(cylinder),
        )
        self.play(
            self.frame.animate.reorient(-66, 76, 0),
            light.animate.scale(0.25),
            run_time=10,
        )
        self.remove(superposition)
        superposition.suspend_updating()
        self.play(*(
            TransformFromCopy(superposition, wave, run_time=2)
            for wave in waves
        ))

        # Go through individual waves
        self.add(waves)
        for wave1 in waves:
            anims = []
            for wave2 in waves:
                wave2.current_opacity = wave2.get_stroke_opacity()
                if wave1 is wave2:
                    wave2.target_opacity = 1
                else:
                    wave2.target_opacity = 0.1
                anims.append(UpdateFromAlphaFunc(wave2, lambda m, a: m.set_stroke(
                    opacity=interpolate(m.current_opacity, m.target_opacity, a)
                )))
            self.play(*anims, run_time=0.5)
            self.wait()

        for wave in waves:
            wave.current_opacity = wave.get_stroke_opacity()
            wave.target_opacity = 1

        self.play(
            *(
                UpdateFromAlphaFunc(wave, lambda m, a: m.set_stroke(
                    opacity=interpolate(m.current_opacity, m.target_opacity, a)
                ))
                for wave in waves
            ),
            frame.animate.reorient(-55, 76, 0).move_to([-0.09, 0.13, -0.17]).set_height(7.5),
            run_time=3
        )

        # Introduce lines
        white_lines = lines.copy()
        white_lines.set_stroke(WHITE)
        white_lines.arrange(UP, buff=0)
        white_lines.move_to(axes.get_origin())

        plane = Square(side_length=2 * axes.z_axis.get_unit_size())
        plane.set_fill(WHITE, 0.25)
        plane.set_stroke(width=0)
        plane.add(
            Circle(radius=0.5 * cylinder.get_depth(), n_components=100).set_stroke(BLACK, 1)
        )
        plane.rotate(PI / 2, UP)
        plane.move_to(axes.get_origin())
        plane.save_state()
        plane.stretch(0, 2, about_edge=UP)

        self.play(
            ReplacementTransform(waves, lines, lag_ratio=0.1, run_time=3),
            frame.animate.reorient(-61, 83, 0).move_to([0.03, -0.16, -0.28]).set_height(7).set_anim_args(run_time=2),
            Restore(plane),
            FadeIn(cylinder),
        )
        self.add(axes, lines)
        self.wait()
        self.play(
            lines.animate.arrange(UP, buff=0).move_to(axes.get_origin()),
            FadeIn(white_lines),
            FadeOut(polarizer),
            FadeOut(polarizer_label),
            FadeOut(light),
        )
        self.wait()

        # Enable lines to twist through the tube
        line_start, line_end = white_lines[0].get_start_and_end()

        distance_tracker = ValueTracker(0)

        wave_lengths = np.linspace(700, 400, self.n_lines)  # Is this right?
        for line, wave_length in zip(lines, wave_lengths):
            line.wave_length = wave_length

        def update_lines(lines):
            dist = distance_tracker.get_value()
            for line in lines:
                line.set_points_as_corners([line_start, line_end])
                line.rotate(get_twist(line.wave_length, dist), RIGHT)
                line.move_to(axes.c2p(dist, 0, 0))
                line.set_gloss(3 * np.exp(-3 * dist))

        lines.add_updater(update_lines)

        # Add wave trails
        trails = VGroup(*(
            self.get_wave_trail(line)
            for line in lines
        ))
        continuous_trails = Group(*(
            self.get_continuous_wave_trail(axes, line)
            for line in lines
        ))
        for trail in continuous_trails:
            x_unit = axes.x_axis.get_unit_size()
            x0 = axes.get_origin()[0]
            trail.add_updater(
                lambda t: t.set_clip_plane(LEFT, distance_tracker.get_value() + x0)
            )
        self.add(trails, lines, white_lines)

        # Move light beams down the pole
        self.add(distance_tracker)
        distance_tracker.set_value(0)
        plane.add_updater(lambda m: m.match_x(lines))
        self.remove(white_lines)

        if self.pause_down_the_tube:
            # Test
            self.play(
                self.frame.animate.reorient(-42, 76, 0).move_to([0.03, -0.16, -0.28]).set_height(7.00),
                distance_tracker.animate.set_value(4),
                run_time=6,
                rate_func=linear,
            )
            trails.suspend_updating()
            self.play(
                self.frame.animate.reorient(67, 77, 0).move_to([-0.31, 0.48, -0.33]).set_height(4.05),
                run_time=3,
            )
            self.wait(2)
            trails.resume_updating()
            self.play(
                distance_tracker.animate.set_value(axes.x_axis.x_max),
                self.frame.animate.reorient(-36, 79, 0).move_to([-0.07, 0.06, 0.06]).set_height(7.42),
                run_time=6,
                rate_func=linear,
            )
            trails.clear_updaters()
            self.play(
                self.frame.animate.reorient(-10, 77, 0).move_to([0.42, -0.16, -0.03]).set_height(5.20),
                trails.animate.set_stroke(width=3, opacity=0.25).set_anim_args(time_span=(0, 3)),
                run_time=10,
            )
        else:
            self.play(
                self.frame.animate.reorient(-63, 84, 0).move_to([1.04, -1.86, 0.55]).set_height(1.39),
                distance_tracker.animate.set_value(axes.x_axis.x_max),
                run_time=15,
                rate_func=linear,
            )
            trails.clear_updaters()
            lines.clear_updaters()

            self.play(
                self.frame.animate.reorient(64, 81, 0).move_to([3.15, 0.46, -0.03]).set_height(5),
                run_time=3,
            )
            self.wait()

        # Add polarizer at the end
        end_polarizer = Polarizer(axes, radius=0.6)
        end_polarizer.next_to(lines, RIGHT, buff=0.5)

        self.play(
            FadeIn(end_polarizer, OUT),
            FadeOut(plane),
            self.frame.animate.reorient(54, 78, 0).move_to([3.15, 0.46, -0.03]).set_height(5.00).set_anim_args(run_time=4)
        )
        end_polarizer.save_state()
        self.play(end_polarizer.animate.fade(0.8))

        # Show a few different frequencies
        vertical_components = VGroup()
        for index in range(len(lines)):
            lines.generate_target()
            trails.generate_target()
            lines.target.set_opacity(0)
            trails.target.set_opacity(0)
            lines.target[index].set_opacity(1)
            trails.target[index].set_opacity(0.2)

            line = lines[index]
            x = float(axes.x_axis.p2n(cylinder.get_right()))
            vcomp = line.copy().set_opacity(1)
            vcomp.stretch(0, 1)
            vcomp.move_to(axes.c2p(x, -2 + index / len(lines), 0))
            z = float(axes.z_axis.p2n(vcomp.get_zenith()))
            y_min, y_max = axes.y_range[:2]
            dashed_lines = VGroup(*(
                DashedLine(axes.c2p(x, y_min, u * z), axes.c2p(x, y_max, u * z), dash_length=0.02)
                for u in [1, -1]
            ))
            dashed_lines.set_stroke(WHITE, 0.5)
            dashed_lines.set_flat_stroke(False)

            self.play(
                MoveToTarget(lines),
                MoveToTarget(trails),
                FadeIn(dashed_lines),
                FadeIn(vcomp),
                self.frame.animate.reorient(77, 87, 0).move_to([3.1, 0.4, 0]).set_height(5),
            )
            self.play(
                FadeOut(dashed_lines),
            )

            vertical_components.add(vcomp)

        self.play(
            lines.animate.set_opacity(1),
            trails.animate.set_opacity(0.05),
        )

        # Final color
        def get_final_color():
            rgbs = np.array([
                line.data["stroke_rgba"][0, :3]
                for line in lines
            ])
            depths = np.array([v_line.get_depth() for v_line in vertical_components])
            alphas = depths / depths.sum()
            rgb = ((rgbs**0.5) * alphas[:, np.newaxis]).sum(0)**2.0
            return rgb_to_color(rgb)

        new_color = get_final_color()
        new_lines = vertical_components.copy()
        for line in new_lines:
            line.set_depth(cylinder.get_depth())
            line.set_stroke(new_color, 4)
            line.next_to(end_polarizer, RIGHT, buff=0.5)

        self.play(
            Restore(end_polarizer),
            TransformFromCopy(vertical_components, new_lines),
            self.frame.animate.reorient(43, 73, 0).move_to([3.3, 0.66, -0.38]).set_height(5.68),
            run_time=4,
        )
        self.play(
            self.frame.animate.reorient(45, 72, 0).move_to([3.17, 0.4, -0.56]),
            run_time=8,
        )

        # Twist the tube
        result_line = new_lines[0]
        self.remove(new_lines)
        self.add(result_line)
        result_line.add_updater(lambda l: l.set_stroke(get_final_color()))

        line_group = VGroup(trails, lines)

        p1, p2 = axes.c2p(0, 1, 0), axes.c2p(0, -1, 0)
        twist_arrows = VGroup(
            Arrow(p1, p2, path_arc=PI),
            Arrow(p2, p1, path_arc=PI),
        )
        twist_arrows.rotate(PI / 2, UP, about_point=axes.get_origin())
        twist_arrows.apply_depth_test()
        self.add(twist_arrows, cylinder, line_group, vertical_components)

        for v_comp, line in zip(vertical_components, lines):
            v_comp.line = line
            v_comp.add_updater(lambda m: m.match_depth(m.line))

        self.play(
            ShowCreation(twist_arrows, lag_ratio=0),
            Rotate(line_group, PI, axis=RIGHT, run_time=12, rate_func=linear)
        )

    def get_wave_trail(self, line, spacing=0.05, opacity=0.05):
        trail = VGroup()
        trail.time = 1

        def update_trail(trail, dt):
            trail.time += dt
            if trail.time > spacing:
                trail.time = 0
                trail.add(line.copy().set_opacity(opacity).set_shading(0, 0, 0))

        trail.add_updater(update_trail)
        return trail

    def get_continuous_wave_trail(self, axes, line, opacity=0.4):
        return TwistedRibbon(
            axes,
            amplitude=0.5 * line.get_length(),
            twist_rate=get_twist(line.wave_length, TAU),
            color=line.get_color(),
            opacity=opacity,
        )
