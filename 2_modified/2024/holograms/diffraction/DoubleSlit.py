# ==============================================================================
# Scene:      DoubleSlit
# Source:     videos/_2024/holograms/diffraction.py (lines 1682-2104)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DoubleSlit.py DoubleSlit -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `set_uniforms(dict(x.uniforms))` fails because `uniforms` is now a structured array: `x.uniforms` is passed directly
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

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


class DoubleSlit(DiffractionGratingScene):
    def construct(self):
        # Show a diffraction grating
        frame = self.frame
        full_width = 40

        n_slit_wall = self.get_wall_with_slits(16, spacing=1.0, total_width=full_width)
        n_slit_wall.move_to(0.5 * IN, IN)
        n_slit_wall.save_state()
        n_slit_wall.arrange(RIGHT, buff=0)
        n_slit_wall.move_to(n_slit_wall.saved_state)

        in_wave = self.get_plane_wave()
        in_wave.set_opacity(0.85)
        in_wave.set_width(full_width)
        in_wave.move_to(ORIGIN, UP)

        line = Line(0.5 * IN + 16 * DOWN + 0.5 * OUT, 0.5 * IN + 0.5 * OUT)
        graph = self.get_graph_over_wave(line, in_wave)

        self.add(graph)
        self.add(n_slit_wall)
        self.add(in_wave)

        frame.reorient(-31, 67, 0, (-3.1, 1.32, -1.12), 15.89)
        self.play(
            frame.animate.reorient(33, 65, 0, (1.24, 1.09, -0.39), 10.01),
            UpdateFromAlphaFunc(
                graph,
                lambda m, a: m.set_stroke(width=3 * clip(there_and_back_with_pause(2 * a, 0.7), 0, 1)),
            ),
            Restore(n_slit_wall, time_span=(9, 12)),
            run_time=15
        )

        # Preview the other side
        sources = self.get_point_sources_from_wall(n_slit_wall)
        sources.set_opacity(0)
        out_wave = LightWaveSlice(sources)
        out_wave.set_max_amp(1)
        out_wave.set_opacity(0.85)
        out_wave.set_decay_factor(0.5)
        out_wave.set_width(full_width * 2.5)
        out_wave.move_to(ORIGIN, DOWN)

        self.add(sources)
        self.play(
            frame.animate.reorient(1, 49, 0, (-0.02, 3.62, 0.61), 11.96),
            FadeIn(out_wave, time_span=(0, 2), suspend_mobject_updating=False),
            run_time=10
        )
        self.wait(3)

        # Change spacing
        wall = n_slit_wall
        wall.target = self.get_wall_with_slits(16, spacing=2 + 0.2 * PI, total_width=2 * full_width)
        wall.target.move_to(wall)
        in_wave.match_width(out_wave)
        in_wave.move_to(ORIGIN, UP)

        start_arrows, end_arrows = [
            VGroup(
                Tex(R"\leftrightarrow").set_width(0.7 * block.get_width(), stretch=True).next_to(block, OUT)
                for block in group[1:-1]
            ).rotate(30 * DEGREES, RIGHT).set_backstroke(BLACK, 5)
            for group in [wall, wall.target]
        ]

        self.play(FadeIn(start_arrows))
        self.play(
            Transform(start_arrows, end_arrows),
            MoveToTarget(wall),
            sources.animate.match_points(self.get_point_sources_from_wall(wall.target)),
            # frame.animate.reorient(0, 40, 0, (-0.61, 5.11, 1.62), 24.87),
            run_time=5
        )
        self.play(FadeOut(start_arrows))

        out_wave.set_width(500, about_edge=DOWN)
        self.play(
            frame.animate.reorient(0, 52, 0, (0.91, 35.42, 33.91), 102.49),
            run_time=16
        )

        # Reduce to one slit
        single_slit_wall = self.get_wall_with_slits(1)
        single_slit_wall.move_to(wall)
        source = self.get_point_sources_from_wall(single_slit_wall)
        source.set_radius(0.5)
        radial_wave = LightWaveSlice(source)
        radial_wave.set_width(full_width)
        radial_wave.move_to(ORIGIN, DOWN)

        self.play(
            frame.animate.reorient(11, 65, 0, (-0.03, 0.06, 0.14), 8.66),
            run_time=3
        )
        self.add(single_slit_wall, in_wave)
        self.play(
            FadeOut(wall, scale=0.9),
            FadeOut(out_wave, suspend_mobject_updating=False),
            FadeIn(single_slit_wall),
        )
        self.wait(3)

        self.play(
            frame.animate.reorient(0, 9, 0, (-0.04, 1.61, 0.15), 8.66),
            FadeIn(radial_wave, suspend_mobject_updating=False),
            run_time=3
        )
        self.wait(2)
        single_slit_wall.set_z_index(1)
        self.play(
            FadeIn(source),
            single_slit_wall.animate.set_opacity(0.1),
            in_wave.animate.set_opacity(0.1),
        )
        self.wait(6)

        # Setup for sine waves
        def field_func(points):
            result = np.zeros_like(points)
            result[:, 2] = 0.5 * radial_wave.wave_func(points)
            return result

        # Expose some film
        film_shape = (12, 6)
        film = Rectangle(*film_shape)
        film.set_fill(GREY_E, 1)
        film.set_stroke(WHITE, 1)
        film.rotate(PI / 2, RIGHT)
        film.move_to(source).set_y(5)

        exposure = LightIntensity(source, shape=film_shape)
        exposure.rotate(PI / 2, RIGHT)
        exposure.move_to(film)
        exposure.set_color(GREEN_SCREEN)
        exposure.set_decay_factor(3.5)
        exposure.set_max_amp(0.005)
        exposure.set_opacity(1e-3)

        radial_wave.set_z_index(1)

        single_slit_wall.set_opacity(1)
        single_slit_wall.set_depth(1.5, about_edge=IN)

        self.play(
            FadeOut(source),
            FadeIn(film, shift=5 * IN),
            FadeIn(exposure, shift=5 * IN),
            FadeIn(single_slit_wall),
            in_wave.animate.set_opacity(0.85).set_time_rate(1.0).set_anim_args(suspend_mobject_updating=False),
            radial_wave.animate.set_time_rate(1.0).set_anim_args(suspend_mobject_updating=False),
            frame.animate.reorient(-19, 68, 0, (-2.38, 4.22, 0.53), 10.86),
            run_time=3
        )
        self.play(exposure.animate.set_opacity(1))
        self.wait(3)

        # Wave to various spots
        exposure_glow = GlowDot(color=GREEN_SCREEN)
        exposure_glow.move_to(film.get_center())
        line = Line(stroke_color=TEAL)
        line.f_always.put_start_and_end_on(
            source.get_center, exposure_glow.get_center
        )
        graph = self.get_graph_over_wave(line, radial_wave, scale_factor=0.2)
        graph.set_stroke(WHITE, 2, 1)
        line.set_stroke(opacity=0)

        graph.set_z_index(0)
        line.set_stroke(TEAL, 2, 1)
        self.add(line, graph, radial_wave)
        self.play(
            VFadeIn(graph),
            VFadeIn(line),
            FadeIn(exposure_glow),
            frame.animate.reorient(-46, 65, 0, (-1.12, 3.76, 0.49), 6.83),
            run_time=3
        )
        self.wait(3)
        self.play(exposure_glow.animate.shift(5 * RIGHT).set_opacity(0.5), run_time=3)
        self.play(
            radial_wave.animate.set_decay_factor(1.0).set_max_amp(0.75).set_anim_args(suspend_mobject_updating=False),
            run_time=2,
        )
        self.play(
            frame.animate.reorient(9, 59, 0, (0.54, 4.02, 0.04), 8.32),
            run_time=12,
        )
        self.wait(4)
        source.match_points(self.get_point_sources_from_wall(single_slit_wall))

        # Change to double slit
        two_slit_wall = self.get_wall_with_slits(2, spacing=3.0, depth=single_slit_wall.get_depth())
        two_slit_wall.move_to(single_slit_wall)

        source.match_points(self.get_point_sources_from_wall(two_slit_wall))

        self.remove(single_slit_wall, graph, line, exposure_glow)
        self.add(two_slit_wall)
        self.wait(4)
        self.play(
            frame.animate.reorient(-25, 48, 0, (0.23, 4.15, -0.03), 9.80),
            run_time=8
        )
        self.play(
            frame.animate.reorient(28, 50, 0, (0.23, 4.15, -0.03), 9.80),
            run_time=8
        )

        out_wave = radial_wave  # Just rename

        # Down to two point sources
        source_pair = source
        source1 = source.copy().set_points(source.get_points()[0:1])
        source2 = source.copy().set_points(source.get_points()[1:2])

        self.play(
            FadeOut(two_slit_wall, shift=2 * IN),
            FadeOut(in_wave, suspend_mobject_updating=False),
            FadeIn(source1),
            FadeIn(source2),
        )
        self.play(
            frame.animate.reorient(0, 68, 0, (0.23, 4.15, -0.03), 9.80),
            run_time=4
        )

        # Show each individual wave
        wave1 = out_wave.copy().set_sources(source1).shift(1e-3 * OUT)
        wave2 = out_wave.copy().set_sources(source2).shift(1e-3 * IN)
        exp1 = exposure.copy().set_sources(source1).shift(1e-3 * DOWN)
        exp2 = exposure.copy().set_sources(source2).shift(2e-3 * DOWN)

        self.play(
            FadeOut(source2),
            FadeOut(out_wave, suspend_mobject_updating=False),
            FadeIn(wave1, suspend_mobject_updating=False),
            exposure.animate.set_opacity(0),
            FadeIn(exp1),
        )
        self.wait(3)
        self.add(wave2, wave1)
        self.play(
            FadeOut(source1),
            FadeIn(source2),
            FadeOut(wave1, suspend_mobject_updating=False),
            FadeIn(wave2, suspend_mobject_updating=False),
            FadeOut(exp1),
            FadeIn(exp2),
        )
        self.wait(3)
        self.play(
            FadeIn(source1),
            FadeOut(wave2, suspend_mobject_updating=False),
            FadeIn(out_wave, suspend_mobject_updating=False),
            FadeOut(exp2),
            exposure.animate.set_opacity(1),
        )
        self.wait(3)

        # Focus on center point
        exposure_point = GlowDot(color=GREEN_SCREEN)
        exposure_point.move_to(film.get_center())

        lines = Line().replicate(2)
        lines.set_stroke(TEAL, 2)
        lines[0].f_always.put_start_and_end_on(source1.get_center, exposure_point.get_center)
        lines[1].f_always.put_start_and_end_on(source2.get_center, exposure_point.get_center)

        graphs = VGroup(
            self.get_graph_over_wave(lines[0], wave1),
            self.get_graph_over_wave(lines[1], wave2),
        )

        self.play(
            out_wave.animate.pause().set_opacity(0.5),
            exposure.animate.set_opacity(0),
            frame.animate.reorient(0, 69, 0, (-0.09, 4.1, -0.16), 7.52),
            FadeIn(exposure_point),
            run_time=3,
        )
        wave1.set_uniform(time=out_wave.uniforms["time"])
        wave2.set_uniform(time=out_wave.uniforms["time"])
        self.play(ShowCreation(lines, lag_ratio=0, suspend_mobject_updating=True))
        self.wait()
        self.play(ShowCreation(graphs, lag_ratio=0, run_time=3, suspend_mobject_updating=True))

        # Show combination from a side angle
        self.play(frame.animate.reorient(-80, 83, 0, (-0.09, 4.1, -0.16), 7.52), run_time=3)
        wave1.pause().set_opacity(0)
        wave2.pause().set_opacity(0)
        self.add(wave1, wave2)
        self.play(*(
            wave.animate.unpause().set_anim_args(suspend_mobject_updating=False)
            for wave in [out_wave, wave1, wave2]
        ))
        self.wait(4)
        self.play(
            frame.animate.reorient(0, 66, 0, (0.12, 4.03, -0.38), 7.52),
            *(
                wave.animate.pause().set_anim_args(suspend_mobject_updating=False)
                for wave in [out_wave, wave1, wave2]
            ),
            run_time=3
        )
        self.wait()

        # Shift to a destructive point
        self.play(
            exposure_point.animate.shift(0.9 * RIGHT).set_opacity(0.25),
            run_time=2
        )
        self.wait()
        self.play(
            frame.animate.reorient(-98, 82, 0, (0.27, 4.19, -0.01), 2.93),
            *(
                wave.animate.unpause().set_anim_args(suspend_mobject_updating=False)
                for wave in [out_wave, wave1, wave2]
            ),
            run_time=3,
        )
        self.wait(8)
        self.play(
            frame.animate.reorient(-2, 69, 0, (-0.23, 2.91, 0.1), 6.38),
            exposure.animate.set_opacity(1),
            run_time=4
        )
        self.wait(3)

        # And now over to another constructive point
        self.play(
            exposure_point.animate.shift(0.9 * RIGHT).set_opacity(1),
            run_time=2
        )
        self.wait(2)
        self.play(
            frame.animate.reorient(81, 88, 0, (-0.23, 2.91, 0.1), 6.38),
            run_time=5,
        )
        self.wait(2)
        self.play(
            frame.animate.reorient(0, 67, 0, (-0.07, 1.75, 0.9), 6.42),
            *(
                wave.animate.pause().set_anim_args(suspend_mobject_updating=False)
                for wave in [out_wave, wave1, wave2]
            ),
            run_time=4,
        )
        self.play(
            exposure_point.animate.shift(5 * LEFT),
            run_time=6
        )
        self.play(
            exposure_point.animate.move_to(film.get_center()),
            run_time=5
        )

        # Shorten wave length
        trg_color = Color(hsl=(0.7, 0.7, 0.5))
        self.play(
            *(
                wave.animate.set_wave_number(2).set_anim_args(suspend_mobject_updating=False)
                for wave in [out_wave, wave1, wave2, exposure]
            ),
            UpdateFromAlphaFunc(
                Point(),
                lambda m, a: exposure.set_color(interpolate_color_by_hsl(GREEN_SCREEN, trg_color, a)),
                remover=True
            ),
            exposure_point.animate.set_color(trg_color),
            run_time=6
        )

        new_out_wave = LightWaveSlice(source_pair)
        new_out_wave.replace(out_wave, stretch=True)
        # CHANGE: `uniforms` is no longer a dict but a structured array (Uniforms); set_uniforms receives it as is
        new_out_wave.set_uniforms(out_wave.uniforms)
        new_out_wave.pause()
        self.remove(out_wave)
        self.add(new_out_wave)
        out_wave = new_out_wave

        # Pan over various spots
        for wave in [out_wave, wave1, wave2]:
            wave.set_frequency(2)

        self.play(
            frame.animate.reorient(-80, 68, 0, (-0.22, 2.44, 0.8), 6.42),
            run_time=3
        )
        self.play(
            exposure_point.animate.shift(3 * LEFT),
            rate_func=there_and_back,
            run_time=16,
        )
        self.play(
            FadeOut(lines),
            FadeOut(graphs),
        )
        self.remove(wave1, wave2)

        # Bring back slits, look over it all
        self.play(out_wave.animate.unpause().set_opacity(1).set_anim_args(suspend_mobject_updating=False))
        new_in_wave = self.get_plane_wave()
        new_in_wave.replace(in_wave)
        new_in_wave.set_wave_number(2)
        new_in_wave.set_frequency(2)
        new_in_wave.set_opacity(0.75)

        self.play(
            FadeIn(new_in_wave, time_span=(0, 2), suspend_mobject_updating=False),
            FadeIn(two_slit_wall, time_span=(0, 1)),
            FadeOut(source1, time_span=(0, 2)),
            FadeOut(source2, time_span=(0, 2)),
            frame.animate.reorient(-25, 62, 0, (-0.82, 2.58, 0.5), 9.13),
            run_time=8
        )
        self.play(
            frame.animate.reorient(30, 60, 0, (-0.48, 2.77, 0.52), 9.13),
            rate_func=there_and_back,
            run_time=24
        )
