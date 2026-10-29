# ==============================================================================
# Scene:      LightExposingFilm
# Source:     videos/_2024/holograms/diffraction.py (lines 407-717)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightExposingFilm.py LightExposingFilm -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `VectorField` changed its API in manimgl (it requires coordinate_system and `sample_coords`; it no longer accepts sample_points/width/height/x_density): the `make_vector_field` wrapper was added with an identity coordinate system
#   - `set_uniforms(dict(x.uniforms))` fails because `uniforms` is now a structured array: `x.uniforms` is passed directly
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

# CHANGE: VectorField changed its API in manimgl (it now requires a coordinate system and receives
# `sample_coords`; it no longer accepts sample_points or width/height/depth/x_density...). This wrapper keeps the
# old call by using an identity coordinate system (unit 1, origin at ORIGIN), so func receives global points
def make_vector_field(
    func,
    sample_points=None,
    center=ORIGIN,
    width=FRAME_WIDTH,
    height=FRAME_HEIGHT,
    depth=0.0,
    x_density=2.0,
    y_density=2.0,
    z_density=2.0,
    **kwargs
):
    identity_axes = ThreeDAxes(
        x_range=(-1, 1, 1), y_range=(-1, 1, 1), z_range=(-1, 1, 1),
        width=2, height=2, depth=2,
    )
    if sample_points is None:
        sample_points = VectorField.get_sample_points(
            None, center, width, height, depth, x_density, y_density, z_density
        )
    return VectorField(func, identity_axes, sample_coords=np.array(sample_points), **kwargs)


# How many sources the shader has room for, see diffraction.wgsl
MAX_LIGHT_SOURCES = 32


class LightWaveSlice(Mobject):
    shader_file: str = str(Path(__file__).with_suffix(".wgsl"))
    data_dtype: np.dtype = np.dtype([
        ('point', np.float32, (3,)),
    ])
    # The four corners are expanded into the two triangles covering them by the vertex
    # shader, six of the vertices drawn doing that and the rest collapsing
    verts_per_record: int = 6
    uniform_dtype: np.dtype = uniform_block_dtype(
        *COMMON_UNIFORMS,
        ("color", 3),
        ("opacity", 1),
        ("frequency", 1),
        ("wave_number", 1),
        ("max_amp", 1),
        ("decay_factor", 1),
        ("show_intensity", 1),
        ("n_sources", 1),
        ("time", 1),
        ("time_rate", 1),
        ("point_sources", 4, MAX_LIGHT_SOURCES),
    )

    def __init__(
        self,
        point_sources: Mobject,
        shape: tuple[float, float] = (8.0, 8.0),
        color: ManimColor = BLUE_D,
        opacity: float = 1.0,
        frequency: float = 1.0,
        wave_number: float = 1.0,
        max_amp: Optional[float] = None,
        decay_factor: float = 0.5,
        show_intensity: bool = False,
        **kwargs
    ):
        self.shape = shape
        self.point_sources = point_sources
        super().__init__(**kwargs)

        if max_amp is None:
            max_amp = point_sources.get_num_points()
        self.set_uniform(
            frequency=frequency,
            wave_number=wave_number,
            max_amp=max_amp,
            time=0,
            decay_factor=decay_factor,
            show_intensity=float(show_intensity),
            time_rate=1.0,
        )
        self.set_color(color, opacity)

        self.add_updater(lambda m, dt: m.increment_time(dt))
        self.always.sync_points()
        self.apply_depth_test()

    def init_data(self) -> None:
        super().init_data(length=4)
        self.data["point"] = [UL, DL, UR, DR]

    def init_points(self) -> None:
        self.set_shape(*self.shape)

    def set_color(
        self,
        color: ManimColor | Iterable[ManimColor] | None,
        opacity: float | Iterable[float] | None = None,
        recurse=False,
    ) -> Self:
        if color is not None:
            self.set_uniform(color=color_to_rgb(color))
        if opacity is not None:
            self.set_uniform(opacity=opacity)
        return self

    def set_opacity(self, opacity: float, recurse=False):
        self.set_uniform(opacity=opacity)
        return self

    def set_wave_number(self, wave_number: float):
        self.set_uniform(wave_number=wave_number)
        return self

    def set_frequency(self, frequency: float):
        self.set_uniform(frequency=frequency)
        return self

    def set_max_amp(self, max_amp: float):
        self.set_uniform(max_amp=max_amp)
        return self

    def set_decay_factor(self, decay_factor: float):
        self.set_uniform(decay_factor=decay_factor)
        return self

    def set_time_rate(self, time_rate: float):
        self.set_uniform(time_rate=time_rate)
        return self

    def set_sources(self, point_sources: DotCloud):
        self.point_sources = point_sources
        return self

    def sync_points(self):
        """
        Takes the sources' places as they stand, which an updater does every frame so that
        moving a source moves the wave it makes.
        """
        points = self.point_sources.get_points()[:MAX_LIGHT_SOURCES]
        # A block holds four floats per array element whatever it is asked for, so a point
        # sits in the first three of them, see uniform_block_dtype
        sources = np.zeros((MAX_LIGHT_SOURCES, 4))
        sources[:len(points), :3] = points
        self.set_uniform(point_sources=sources, n_sources=len(points))
        return self

    def increment_time(self, dt):
        self.uniforms["time"] += self.uniforms["time_rate"] * dt
        return self

    def show_intensity(self, show: bool = True):
        self.set_uniform(show_intensity=float(show))

    def pause(self):
        self.set_uniform(time_rate=0)
        return self

    def unpause(self):
        self.set_uniform(time_rate=1)
        return self

    def interpolate(
        self,
        wave1: LightWaveSlice,
        wave2: LightWaveSlice,
        alpha: float,
        path_func: Callable[[np.ndarray, np.ndarray, float], np.ndarray] = straight_path
    ) -> Self:
        # The clock is the updater's to advance, not an animation's to interpolate: both
        # ends of one were copied at the moment it began, so letting it through would stop
        # the wave for as long as the animation ran
        time = self.uniforms["time"]
        super().interpolate(wave1, wave2, alpha, path_func)
        self.set_uniform(time=time)
        return self

    def wave_func(self, points):
        time = self.uniforms["time"]
        wave_number = self.uniforms["wave_number"]
        frequency = self.uniforms["frequency"]
        decay_factor = self.uniforms["decay_factor"]

        values = np.zeros(len(points))
        for source_point in self.point_sources.get_points():
            dists = np.linalg.norm(points - source_point, axis=1)
            values += np.cos(TAU * (wave_number * dists - frequency * time)) * (dists + 1)**(-decay_factor)
        return values


class LightIntensity(LightWaveSlice):
    def __init__(
        self,
        *args,
        color: ManimColor = BLUE,
        show_intensity: bool = True,
        **kwargs
    ):
        super().__init__(*args, color=color, show_intensity=show_intensity, **kwargs)


class DiffractionGratingScene(InteractiveScene):
    light_position = 10 * DOWN + 5 * OUT + 3 * LEFT

    def setup(self):
        super().setup()
        self.camera.light_source.move_to(self.light_position)

    def get_wall_with_slits(self, n_slits, spacing=1.0, slit_width=0.1, height=0.25, depth=3.0, total_width=40, color=GREY_D, shading=(0.5, 0.5, 0.5)):
        width = spacing - slit_width
        cube = Cube().set_shape(width, height, depth)
        parts = cube.replicate(n_slits + 1)
        parts.arrange(RIGHT, buff=slit_width)
        edge_piece_width = 0.5 * (total_width - parts.get_width()) + parts[0].get_width()
        parts[0].set_width(edge_piece_width, stretch=True, about_edge=RIGHT)
        parts[-1].set_width(edge_piece_width, stretch=True, about_edge=LEFT)

        parts.set_color(color)
        parts.set_shading(*shading)
        return parts

    def get_point_sources_from_wall(self, wall, z=0):
        sources = GlowDots(np.array([
            midpoint(p1.get_right(), p2.get_left())
            for p1, p2 in zip(wall, wall[1:])
        ]))
        sources.set_color(WHITE)
        sources.set_z(z)
        return sources

    def get_plane_wave(self, direction=UP):
        return LightWaveSlice(DotCloud([-1000 * direction]), decay_factor=0)

    def get_graph_over_wave(self, line, light_wave, color=WHITE, stroke_width=2, direction=OUT, scale_factor=0.5, n_curves=500):
        line.insert_n_curves(n_curves - line.get_num_curves())
        graph = line.copy()
        graph.line = line

        def update_graph(graph):
            points = graph.line.get_anchors()
            values = scale_factor * light_wave.wave_func(points)
            graph.set_points_smoothly(points + values[:, np.newaxis] * direction)

        graph.add_updater(update_graph)
        graph.apply_depth_test()
        graph.set_stroke(color, stroke_width)
        return graph


class LightExposingFilm(DiffractionGratingScene):
    def construct(self):
        # Set up wave
        frame = self.frame
        self.set_floor_plane("xz")

        source_dist = 16.5
        source = GlowDot(source_dist * OUT).set_opacity(0)
        wave = LightWaveSlice(source, decay_factor=0, wave_number=0.5)
        wave.set_opacity(0)
        wave_line = Line(source.get_center(), ORIGIN)
        wave_line.set_stroke(width=0)
        initial_wave_amp = 0.75
        wave_amp_tracker = ValueTracker(initial_wave_amp)
        graph = self.get_graph_over_wave(wave_line, wave, direction=UP, scale_factor=wave_amp_tracker.get_value(), n_curves=200)
        graph.add_updater(lambda m: m.stretch(wave_amp_tracker.get_value() / initial_wave_amp, dim=1))

        # Set up linear vector field
        def field_func(points):
            result = np.zeros_like(points)
            result[:, 1] = wave_amp_tracker.get_value() * wave.wave_func(points)
            return result

        linear_field = make_vector_field(field_func, sample_points=wave_line.get_points()[::4], max_vect_len=2.0)
        linear_field.always.update_vectors()
        linear_field.set_stroke(WHITE, width=1.5, opacity=0.75)

        # Add film
        film = Rectangle(16, 9)
        film.set_fill(GREY_E, 0.75)
        film.set_height(8)
        film.center()

        exp_source = GlowDot(OUT).set_opacity(0)
        exposure = LightIntensity(exp_source)
        exposure.set_color(GREEN)
        exposure.set_decay_factor(3)
        exposure.set_max_amp(0.15)
        exposure.set_opacity(0.7)
        exposure.replace(film, stretch=True)

        film_label = Text("Film", font_size=96)
        film_label.next_to(film, UP, MED_SMALL_BUFF)

        frame.reorient(-18, -7, 0, (0.46, -0.4, -2.46), 17.86)
        self.add(film, exposure, film_label)
        self.add(wave, linear_field, graph)

        # Fade in
        self.play(
            frame.animate.reorient(-88, -4, 0, (3.56, -0.71, 4.59), 14.60),
            FadeIn(exposure, time_span=(0, 3)),
            run_time=7.5
        )

        # Label amplitude
        low_line = DashedLine(8 * OUT, ORIGIN)
        high_line = low_line.copy().shift(wave_amp_tracker.get_value() * UP)
        amp_lines = VGroup(low_line, high_line)
        amp_lines.set_stroke(YELLOW, 3)
        brace = Brace(amp_lines, RIGHT)
        brace.rotate(PI / 2, DOWN)
        brace.next_to(amp_lines, OUT, SMALL_BUFF)
        amp_label = Tex(R"\text{Amplitude}", font_size=72)
        amp_label.set_backstroke(BLACK, 5)
        amp_label.rotate(PI / 2, DOWN)
        amp_label.next_to(brace, OUT, SMALL_BUFF)
        fade_rect = Rectangle(8, 3)
        fade_rect.rotate(PI / 2, DOWN)
        fade_rect.next_to(amp_lines, OUT, buff=0)
        fade_rect.set_stroke(BLACK, 0)
        fade_rect.set_fill(BLACK, 0.7)

        self.play(
            FadeIn(fade_rect),
            GrowFromCenter(brace),
            FadeIn(amp_lines[0]),
            ReplacementTransform(amp_lines[0].copy().fade(1), amp_lines[1]),
        )
        self.play(Write(amp_label, stroke_color=WHITE, lag_ratio=0.1, run_time=2.0))
        self.wait_until(lambda: 8 / 30 < wave.uniforms["time"] % 1 < 9 / 30)

        # Label phase
        phase_text = Text("Phase", font_size=72)
        phase_circle = Circle(radius=0.75)
        phase_circle.set_stroke(BLUE, 2)
        phase_circle.next_to(phase_text, DOWN)
        phase_vect = Arrow(phase_circle.get_center(), phase_circle.get_right(), buff=0, thickness=2)
        phase_vect.set_fill(BLUE)

        phase_label = VGroup(phase_text, phase_circle, phase_vect)
        phase_label.rotate(PI / 2, DOWN)
        phase_label.next_to(amp_lines, DOWN, buff=2)
        phase_label.set_z(2)
        og_phase_label = phase_label.copy()

        wavelength = 1.0 / wave.uniforms["wave_number"]
        start_z = 0
        phase_line = Line(start_z * OUT, (start_z + wavelength) * OUT)
        phase_line.set_stroke(BLUE, 3)

        phase_arrow = Arrow(phase_text.get_corner(IN + UP) + 0.2 * (OUT + UP), phase_line.get_start(), buff=0)
        phase_arrow.always.set_perpendicular_to_camera(self.frame)

        self.play(
            wave.animate.pause(),
            FadeIn(phase_label),
            FadeIn(phase_arrow),
            frame.animate.reorient(-99, -2, 0, (3.56, -0.71, 4.59), 14.60),
        )
        self.play(
            Rotate(phase_vect, -TAU, axis=LEFT, about_point=phase_vect.get_start()),
            ShowCreation(phase_line),
            phase_arrow.animate.put_start_and_end_on(phase_arrow.get_start(), phase_line.get_end()),
            run_time=3
        )
        self.play(
            Rotate(phase_vect, TAU, axis=LEFT, about_point=phase_vect.get_start()),
            phase_arrow.animate.put_start_and_end_on(phase_arrow.get_start(), phase_line.get_start()),
            run_time=3
        )
        self.wait(2)

        # Decrease and increase amplitude
        amp_group = VGroup(amp_lines, brace)
        amp_group.f_always.set_height(wave_amp_tracker.get_value, stretch=lambda: True)
        amp_group.always.move_to(ORIGIN, IN + DOWN)
        amp_label.always.next_to(brace, OUT, SMALL_BUFF)
        self.add(amp_group, amp_label)

        phase_vect.add_updater(lambda m: m.put_start_and_end_on(
            phase_circle.get_center(),
            phase_circle.pfp((wave.uniforms["frequency"] * wave.uniforms["time"]) % 1),
        ))
        phase_vect.always.set_perpendicular_to_camera(self.frame)

        self.play(
            wave.animate.set_time_rate(0.5),
            frame.animate.reorient(-55, -13, 0, (2.59, -0.61, 2.18), 17.00),
            phase_arrow.animate.fade(0.8),
            phase_label.animate.fade(0.8),
            FadeOut(phase_line),
            run_time=3
        )
        self.play(
            wave_amp_tracker.animate.set_value(0.25),
            exposure.animate.set_opacity(0.25),
            run_time=3,
        )
        self.wait(2)
        self.play(
            wave_amp_tracker.animate.set_value(1.0),
            exposure.animate.set_opacity(1.0),
            run_time=4
        )
        self.wait()

        # Write exposure expression
        exp_expr = Tex(R"\text{Exposure} = c \cdot |\text{Amplitude}|^2", font_size=72)
        exp_expr.move_to(2 * UP)

        self.play(
            LaggedStart(
                Write(exp_expr[R"\text{Exposure} = c \cdot |"][0]),
                TransformFromCopy(amp_label.copy().clear_updaters(), exp_expr[R"\text{Amplitude}"][0]),
                Write(exp_expr[R"|^2"][0]),
                lag_ratio=0.1,
            ),
            frame.animate.reorient(-34, -15, 0, (1.48, -0.23, 1.29), 16.08),
            run_time=3,
        )
        self.wait(8)

        # Focus on phase again
        to_fade = VGroup(fade_rect, amp_group, amp_label)
        wave.pause()
        self.play(
            FadeOut(to_fade, lag_ratio=0.01, time_span=(0, 1.5)),
            phase_label.animate.match_style(og_phase_label),
            phase_arrow.animate.set_fill(opacity=1),
            frame.animate.reorient(-86, -4, 0, (2.43, -0.97, 1.94), 12.91),
            run_time=2
        )

        # Shift back the phase
        shift_label = TexText(R"Shift back phase $\rightarrow$")
        shift_label.rotate(PI / 2, DOWN)
        shift_label.move_to(7 * OUT + 1.5 * DOWN)

        self.play(
            wave.animate.set_uniform(time_rate=-0.5).set_anim_args(rate_func=there_and_back),
            FadeIn(shift_label, shift=OUT),
            run_time=2.0
        )
        self.play(FadeOut(shift_label))
        self.wait()

        # Play for a while
        self.play(wave.animate.set_time_rate(0.5))
        self.wait(16)

        # Shine a second beam in
        source2 = GlowDot(source_dist * (OUT + RIGHT))
        wave2 = LightWaveSlice(source2)
        # CHANGE: `uniforms` is no longer a dict but a structured array (Uniforms); set_uniforms receives it as is
        wave2.set_uniforms(wave.uniforms)
        wave2.set_opacity(0)
        line2 = Line(ORIGIN, source2.get_center())
        ref_amp = 0.75
        graph2 = self.get_graph_over_wave(line2, wave2, direction=UP, scale_factor=ref_amp, n_curves=int(200 * math.sqrt(2)))
        graph2.set_color(YELLOW)
        graph2.update()

        def field_func2(points):
            result = np.zeros_like(points)
            result[:, 1] = ref_amp * wave2.wave_func(points)
            return result

        linear_field2 = make_vector_field(field_func2, sample_points=line2.get_points()[::4], max_vect_len=2.0)
        linear_field2.always.update_vectors()
        linear_field2.set_stroke(YELLOW, width=1.5, opacity=0.75)

        ref_wave_label = Text("Reference Wave", font_size=72)
        ref_wave_label.set_color(YELLOW)
        ref_wave_label.set_backstroke(BLACK, 3)
        ref_wave_label.rotate(PI / 4, DOWN)
        ref_wave_label.move_to([5, 1.25, 5])

        self.play(
            FadeOut(phase_label),
            FadeOut(phase_arrow),
            wave_amp_tracker.animate.set_value(0.75),
            exposure.animate.set_opacity(0.75),
            frame.animate.reorient(-32, -20, 0, (1.48, -0.73, 0.84), 14.72),
            run_time=2,
        )
        self.wait_until(lambda: 8 / 30 < wave.uniforms["time"] % 1 < 9 / 30)
        self.add(wave2)
        self.play(
            FadeIn(graph2),
            FadeIn(linear_field2),
        )
        self.wait()
        self.play(FadeIn(ref_wave_label, shift=UP))
        self.wait(5)

        # Zoom in
        self.play(
            frame.animate.reorient(-58, -18, 0, (3.29, 0.39, 0.55), 10.68),
            run_time=4
        )
        self.play(
            exposure.animate.set_opacity(1).set_max_amp(0.1),
            run_time=2
        )
        self.wait(3)

        # Shift back
        shift_label = TexText(R"Shift back phase $\rightarrow$")
        shift_label.rotate(PI / 2, DOWN)
        shift_label.set_backstroke(BLACK, 5)
        shift_label.move_to(5 * OUT + 1.25 * UP)

        self.play(
            wave.animate.pause(),
            wave2.animate.pause(),
        )
        self.play(
            wave.animate.set_uniform(time_rate=-0.5).set_anim_args(rate_func=there_and_back),
            exposure.animate.set_max_amp(0.2).set_opacity(0.15),
            FadeIn(shift_label, OUT),
            run_time=2.0
        )
        self.play(FadeOut(shift_label))
        self.play(
            wave.animate.set_time_rate(0.5),
            wave2.animate.set_time_rate(0.5),
        )
        self.play(
            frame.animate.reorient(-54, -16, 0, (3.01, -0.09, 0.55), 14.47),
            run_time=10,
        )

        wave.pause()
        wave2.pause()
        self.play(
            wave.animate.set_uniform(time_rate=-0.5).set_anim_args(rate_func=there_and_back),
            exposure.animate.set_max_amp(0.1).set_opacity(1),
            FadeIn(shift_label, OUT),
            run_time=2.0
        )
        self.play(FadeOut(shift_label))
        wave.set_time_rate(0.5)
        wave2.set_time_rate(0.5)
        self.play(
            frame.animate.reorient(15, -22, 0, (2.14, -0.48, -0.07), 15.51),
            run_time=12,
        )

        wave.pause()
        wave2.pause()
        self.play(
            wave.animate.set_uniform(time_rate=-0.5).set_anim_args(rate_func=there_and_back),
            exposure.animate.set_max_amp(0.2).set_opacity(0.15),
            run_time=2.0
        )
        wave.set_time_rate(0.5)
        wave2.set_time_rate(0.5)
        self.play(
            frame.animate.reorient(15, -14, 0, (1.47, 0.09, -0.04), 13.26),
            run_time=12,
        )
