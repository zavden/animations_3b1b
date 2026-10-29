# ==============================================================================
# Scene:      AngledMediumAnnotations
# Source:     videos/_2023/optics_puzzles/bending_waves.py (lines 474-518)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AngledMediumAnnotations.py AngledMediumAnnotations -w -m --fps 15
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


class AngledMediumAnnotations(InteractiveScene):
    def construct(self):
        # Set up the lane
        h_lines = Line(LEFT, RIGHT).replicate(3)
        h_lines.set_width(0.7 * FRAME_WIDTH)
        h_lines.arrange(DOWN, buff=0.5)
        h_lines.move_to(ORIGIN, RIGHT)

        index = WavesIntoAngledMedium.index
        angle = math.asin(math.sin(45 * DEGREES) / index)
        diag_lines = h_lines.copy()
        for line1, line2 in zip(h_lines, diag_lines):
            line2.move_to(line1.get_end(), LEFT)
            line2.rotate(-angle, about_point=line1.get_end())

        lane_points = [
            h_lines[0].get_left(),
            h_lines[0].get_right(),
            diag_lines[0].get_end(),
            diag_lines[2].get_end(),
            h_lines[2].get_right(),
            h_lines[2].get_left(),
        ]

        fade_rect = FullScreenFadeRectangle()
        fade_rect.scale(1.5)
        fade_rect.start_new_path(lane_points[-1])
        for point in lane_points:
            fade_rect.add_line_to(point)

        fade_rect.set_fill(BLACK, 0.8)

        beam = h_lines[1].copy()
        beam.add_line_to(diag_lines[1].get_end())
        beam.set_stroke(YELLOW, 1.5)
        beam.insert_n_curves(100)

        self.play(
            FadeIn(fade_rect),
        )
        self.play(
            ShowCreation(beam, run_time=3),
            VShowPassingFlash(beam.copy().set_stroke(width=5), run_time=3)
        )
        self.wait()
