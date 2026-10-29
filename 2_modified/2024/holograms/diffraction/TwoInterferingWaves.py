# ==============================================================================
# Scene:      TwoInterferingWaves
# Source:     videos/_2024/holograms/diffraction.py (lines 720-859)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TwoInterferingWaves.py TwoInterferingWaves -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (HologramFilm.jpg) replaced with regenerable placeholders
#   - `set_uniforms(dict(x.uniforms))` fails because `uniforms` is now a structured array: `x.uniforms` is passed directly
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/HologramFilm.jpg  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
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


class TwoInterferingWaves(DiffractionGratingScene):
    def construct(self):
        # Setup reference and object waves
        frame = self.frame
        self.set_floor_plane("xz")

        film_border = ScreenRectangle()
        film_border.set_height(6)
        film_border.set_fill(BLACK, 0)
        film_border.set_stroke(WHITE, 1)
        film_image = ImageMobject("HologramFilm.jpg")
        film_image.replace(film_border)

        frame.set_height(6)
        self.add(film_image, film_border)

        # Add waves
        obj_vect = 5 * OUT + 2 * LEFT
        ref_vect = 5 * OUT + 2 * RIGHT
        lp = film_border.get_left() + 3 * DOWN
        rp = film_border.get_right() + 3 * DOWN

        obj_points = DotCloud(np.random.random((31, 3)))
        obj_points.set_height(10)
        obj_points.move_to(obj_vect)
        obj_wave = LightWaveSlice(obj_points)
        obj_wave.set_wave_number(8)
        obj_wave.set_frequency(1)
        obj_wave.set_max_amp(3)

        ref_wave = LightWaveSlice(TrueDot(10 * ref_vect))
        ref_wave.match_points(obj_wave)
        # CHANGE: `uniforms` is no longer a dict but a structured array (Uniforms); set_uniforms receives it as is
        ref_wave.set_uniforms(obj_wave.uniforms)
        ref_wave.set_max_amp(1.25)
        ref_wave.set_decay_factor(0)
        ref_wave.set_opacity(0.85)

        rect = film_border
        obj_wave.set_points([
            2 * obj_vect, rect.get_corner(UL), rect.get_corner(DL),
            2 * obj_vect, rect.get_corner(UL), rect.get_corner(UR),
            2 * obj_vect, rect.get_corner(UR), rect.get_corner(DR),
            2 * obj_vect, rect.get_corner(DR), rect.get_corner(DL),
        ])
        ref_wave.set_points([
            2 * ref_vect, rect.get_corner(UL), rect.get_corner(DL),
            2 * ref_vect, rect.get_corner(UL), rect.get_corner(UR),
            2 * ref_vect, rect.get_corner(UR), rect.get_corner(DR),
            2 * ref_vect, rect.get_corner(DR), rect.get_corner(DL),
        ])
        obj_wave.deactivate_depth_test()
        ref_wave.deactivate_depth_test()

        waves = Group(ref_wave, obj_wave)
        waves.set_opacity(0.25)

        self.play(
            FadeIn(waves),
            frame.animate.reorient(0, -21, 0, (-0.09, -0.86, 0.04), 9.40),
            run_time=3
        )
        self.wait(3)

        # Diversion into backdrop for complex wave scene
        if False:
            # Isolate object wave
            new_obj_wave = LightWaveSlice(obj_points)
            new_obj_wave.set_points([2 * obj_vect, rect.get_left(), rect.get_right()])
            # CHANGE: `uniforms` is no longer a dict but a structured array (Uniforms); set_uniforms receives it as is
            new_obj_wave.set_uniforms(obj_wave.uniforms)
            new_obj_wave.set_opacity(1)
            new_obj_wave.set_frequency(0.25)

            frame.reorient(0, -19, 0, (0.01, -0.03, -0.28), 12.53)
            waves.set_opacity(0.4)
            for wave in waves:
                wave.set_frequency(0.25)
            self.wait(4)

            self.play(
                FadeOut(ref_wave),
                FadeOut(film_border),
                FadeOut(film_image),
                FadeOut(obj_wave),
                FadeIn(new_obj_wave)
            )

            # Go to 2d slice
            self.play(
                new_obj_wave.animate.scale(10),
                frame.animate.reorient(-3, -5, 0, (-0.96, 0.03, -0.15), 5.32),
                run_time=5
            )
            self.wait(4)

            # Circle a point
            circle = Circle(radius=0.1).set_stroke(WHITE, 2)
            circle.move_to(LEFT + 2 * DOWN)
            circle.reverse_points()
            full_rect = FullScreenRectangle()
            full_rect.set_fill(BLACK, 0.75)
            full_rect.append_points([full_rect.get_end(), *circle.get_points()])

            circle.fix_in_frame()
            full_rect.fix_in_frame()

            self.play(
                FadeIn(full_rect),
                ShowCreation(circle),
            )
            self.wait(8)

        # Add exposure
        exposure = LightIntensity(obj_points)
        exposure.set_color(WHITE)
        exposure.replace(film_border, stretch=True)
        exposure.set_wave_number(256)
        exposure.set_max_amp(4)

        # One more insertion
        exposure.set_opacity(0.5)
        self.add(exposure, waves)
        frame.reorient(-18, -30, 0, (-5.85, -0.18, -0.89), 15.16)
        self.play(
            frame.animate.reorient(17, -24, 0, (-5.5, -0.82, -0.67), 15.86),
            run_time=30
        )

        self.add(exposure, waves)
        self.play(
            FadeIn(exposure, run_time=5),
            FadeOut(waves, time_span=(3, 5)),
        )

        # Zoom in on the film
        self.play(
            frame.animate.reorient(0, 0, 0, (0.5, 0.07, 0.0), 0.15),
            film_image.animate.set_opacity(0.1).set_anim_args(time_span=(0, 5)),
            run_time=8,
        )
        self.play(frame.animate.reorient(0, 0, 0, (0.41, 0.03, 0.0), 0.05), run_time=8)
