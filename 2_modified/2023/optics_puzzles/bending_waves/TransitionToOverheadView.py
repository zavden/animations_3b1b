# ==============================================================================
# Scene:      TransitionToOverheadView
# Source:     videos/_2023/optics_puzzles/bending_waves.py (lines 319-446)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TransitionToOverheadView.py TransitionToOverheadView -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField

class WaveIntoMedium(TimeVaryingVectorField):
    def __init__(
        self,
        interface_origin=ORIGIN,
        interface_normal=DR,
        prop_direction=RIGHT,
        index=1.5,
        c=2.0,
        frequency=0.25,
        amplitude=1.0,
        x_density=5.0,
        y_density=5.0,
        width=15.0,
        height=15.0,
        norm_to_opacity_func=lambda n: np.tanh(n),
        **kwargs
    ):
        def time_func(points, time):
            k = frequency / c
            phase = TAU * (k * np.dot(points, prop_direction.T) - frequency * time)
            kickback = np.dot(points - interface_origin, interface_normal.T)
            kickback[kickback < 0] = 0
            phase += kickback * index * c
            return amplitude * np.outer(np.cos(phase), OUT)

        super().__init__(
            time_func,
            x_density=x_density,
            y_density=y_density,
            width=width,
            height=height,
            norm_to_opacity_func=norm_to_opacity_func,
            **kwargs
        )


class ScalarFieldByOpacity(DotCloud):
    def __init__(
        self,
        # Takes (n, 3) array of points to n-array of values between 0 and 1
        opacity_func,
        width=15,
        height=8,
        density=10,
        color=WHITE,
    ):
        step = 1.0 / density
        radius = step / 2.0
        points = np.array([
            [x, y, 0]
            for x in np.arange(-width / 2, width / 2 + step, step)
            for y in np.arange(-height / 2, height / 2 + step, step)
        ])

        super().__init__(points, color=color, radius=radius)
        self.opacity_func = opacity_func

        def update_opacity(dots):
            dots.set_opacity(opacity_func(dots.get_points()))

        self.add_updater(update_opacity)


class WavesByOpacity(ScalarFieldByOpacity):
    def __init__(
        self,
        wave: VectorField,
        vects_to_opacities=lambda v: np.tanh(v[:, 2]),
        **kwargs
    ):
        super().__init__(
            opacity_func=lambda p: vects_to_opacities(wave.func(p)),
            **kwargs
        )


class WavesIntoAngledMedium(InteractiveScene):
    default_frame_orientation = (0, 0)
    interface_origin = ORIGIN
    interface_normal = DR
    prop_direction = RIGHT
    frequency = 0.5
    c = 1.0
    index = 2.0
    amplitude = 0.5

    def get_medium(
        self,
        width=10,
        height=30,
        depth=5,
        color=BLUE,
        opacity=0.2,
    ):
        medium = VCube(side_length=1.0)
        medium.set_shape(width, height, depth)
        medium.set_fill(color, opacity)
        medium.move_to(self.interface_origin, LEFT)
        medium.rotate(
            angle_of_vector(self.interface_normal),
            about_point=self.interface_origin
        )
        return medium

    def get_wave(self, **kwargs):
        config = dict(
            interface_origin=self.interface_origin,
            interface_normal=self.interface_normal,
            prop_direction=self.prop_direction,
            frequency=self.frequency,
            c=self.c,
            index=self.index,
            max_vect_len=np.inf,
            amplitude=self.amplitude,
            norm_to_opacity_func=lambda n: sigmoid(n),
        )
        config.update(kwargs)
        return WaveIntoMedium(**config)

    def get_wave_dots(self, wave, density=20, offset=0.2, color=WHITE, max_opacity=1.0, **kwargs):
        return WavesByOpacity(
            wave,
            density=density,
            vects_to_opacities=lambda v: max_opacity * np.tanh(v[:, 2] - offset * self.amplitude),
            color=color,
            **kwargs
        )


class TransitionToOverheadView(WavesIntoAngledMedium):
    interface_normal = RIGHT
    index = 2.0
    amplitude = 0.5

    def construct(self):
        # 1D case
        frame = self.frame
        medium = self.get_medium(opacity=0.3, height=8.0, depth=2.0)
        medium.remove(medium[-1])
        medium.sort(lambda p: -p[1] - p[2])
        medium.set_stroke(WHITE, 0.5, 0.5)
        medium.set_flat_stroke(False)
        wave_1d = self.get_wave(x_density=10, height=0.0)
        wave_1d.set_stroke(YELLOW)
        plane = NumberPlane(
            background_line_style=dict(
                stroke_color=BLUE_D,
                stroke_width=1,
                stroke_opacity=1,
            ),
        )
        plane.axes.set_stroke(width=1)
        plane.fade(0.5)

        self.add(plane, medium, wave_1d)
        frame.reorient(-37, 61, 0)

        self.play(
            frame.animate.reorient(0, 90).set_height(6),
            run_time=5,
        )
        self.wait(10)

        # Highlight wave length
        past_time = wave_1d.time
        wave_1d.suspend_updating()
        wave_len = 1.0
        mult = 2.0
        brace1 = Brace(Line(ORIGIN, mult * wave_len * RIGHT), UP)
        brace1.add(brace1.get_tex(Rf"\lambda = {wave_len}"))
        brace2 = Brace(Line(ORIGIN, 0.6 * mult * wave_len * RIGHT), UP)
        brace2.add(brace2.get_tex(Rf"\lambda = {0.6 * wave_len}"))

        for brace in [brace1, brace2]:
            brace.rotate(90 * DEGREES, RIGHT)
            brace.set_fill(border_width=0)

        brace1.next_to(3 * LEFT + 0.35 * OUT, OUT)
        brace2.next_to(1.85 * RIGHT + 0.35 * OUT, OUT)

        self.play(FadeIn(brace1, lag_ratio=0.1))
        self.wait()
        self.play(FadeTransform(brace1.copy(), brace2))
        self.wait()
        wave_1d.time = past_time
        wave_1d.resume_updating()
        self.play(
            FadeOut(brace1, RIGHT),
            FadeOut(brace2, 0.6 * RIGHT),
        )
        self.wait(3)

        # Transition to 2d
        wave_2d = self.get_wave(
            width=20.0, height=8.0,
            norm_to_opacity_func=lambda n: 0.5 * sigmoid(2 * n),
        )
        wave_2d.set_stroke(YELLOW)
        invisible_wave_2d = self.get_wave(
            width=20.0, height=12.0,
            norm_to_opacity_func=None,
            stroke_opacity=0,
        )
        wave_dots = self.get_wave_dots(
            invisible_wave_2d,
        )

        self.remove(wave_1d)
        wave_2d.time = wave_1d.time
        self.add(wave_2d)
        self.play(
            frame.animate.reorient(-10, 45).set_height(8).set_anim_args(
                run_time=7,
                time_span=(1, 7),
            ),
        )
        self.wait(2)
        self.wait(8)

        self.remove(wave_2d)
        invisible_wave_2d.time = wave_2d.time
        self.add(invisible_wave_2d, wave_dots)
        self.wait(2)
        self.play(
            frame.animate.reorient(0, 0),
            plane.animate.fade(0.5),
            medium.animate.set_opacity(0.2),
            run_time=4,

        )
        self.wait(8)

        # Show wave lengths again
        invisible_wave_2d.suspend_updating()
        VGroup(brace1, brace2).rotate(90 * DEGREES, LEFT)
        VGroup(brace1, brace2).set_backstroke(BLACK, 3)
        brace1.next_to(4 * LEFT, UP)
        brace2.next_to(2.45 * RIGHT, UP)
        braces = VGroup(brace1, brace2)

        self.play(
            FadeIn(braces),
        )
        self.wait()

        # Pan back down to 1d wave
        wave_1d.time = invisible_wave_2d.time
        wave_1d.update()
        wave_1d.clear_updaters()
        self.play(
            # FadeOut(wave_dots),
            FadeIn(wave_1d),
            frame.animate.reorient(0, 70),
            braces.animate.rotate(90 * DEGREES, RIGHT, about_point=ORIGIN).shift(0.3 * OUT),
            run_time=5,
        )
        self.wait()
