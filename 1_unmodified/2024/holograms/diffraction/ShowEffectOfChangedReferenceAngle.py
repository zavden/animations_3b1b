# ==============================================================================
# Scene:      ShowEffectOfChangedReferenceAngle
# Source:     videos/_2024/holograms/diffraction.py (lines 1606-1679)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowEffectOfChangedReferenceAngle.py ShowEffectOfChangedReferenceAngle -w -m --fps 15
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


class ShowEffectOfChangedReferenceAngle(InteractiveScene):
    def construct(self):
        # Create object and reference wave
        frame = self.frame
        axes = ThreeDAxes()
        self.set_floor_plane("xz")

        wave_width = 100
        wave_number = 10
        frequency = 1

        source_points = GlowDots([OUT, 10 * OUT], color=WHITE, radius=0.0)
        wave = LightWaveSlice(source_points)

        wave.set_width(wave_width)
        wave.rotate(PI / 2, RIGHT, about_point=ORIGIN)
        wave.center()
        wave.set_wave_number(wave_number)
        wave.set_frequency(frequency)
        wave.set_max_amp(1.5)
        wave.set_decay_factor(0.5)

        # Add film
        plate_border = Rectangle(16, 9)
        plate_border.set_fill(BLACK, 0)
        plate_border.set_stroke(WHITE, 2)
        plate = Square3D()
        plate.set_color(BLACK, 0.9)
        plate.replace(plate_border, stretch=True)
        plate.set_shading(0.1, 0.1, 0)
        exposure = LightIntensity(source_points)
        exposure.set_decay_factor(0)
        exposure.set_wave_number(wave_number)
        exposure.replace(plate_border, stretch=True).shift(1e-2 * OUT)
        exposure.set_color(WHITE, 0.85)

        plate_group = Group(plate_border, plate)
        film = Group(plate_group, exposure)
        film.set_height(4)
        film.set_z(-2)

        film_label = Text("Film")
        film_label.next_to(plate_group, UP)
        film_label.set_backstroke(BLACK, 3)
        film_label.set_z_index(1)

        source_dot = GlowDot(source_points.get_points()[0], color=WHITE, radius=0.5)

        self.add(film, exposure, wave, source_points, source_dot)

        # Add reference wave lines
        plate_border.insert_n_curves(max(25 - plate_border.get_num_curves(), 0))
        film_points = np.array([plate_border.pfp(a) for a in np.linspace(0, 1, 500)])
        ref_lines = Line().replicate(len(film_points))
        ref_lines.set_stroke(GREEN_SCREEN, width=1, opacity=0.25)

        def update_ref_lines(lines):
            for line, point in zip(lines, film_points):
                line.set_points_as_corners([source_points.get_points()[1], point])
            return lines

        ref_lines.add_updater(update_ref_lines)

        self.add(ref_lines)

        # Move reference wave
        frame.reorient(-52, -29, 0, (1.21, -0.31, 1.52), 9.28)
        self.wait()
        self.play(
            Rotate(source_points, 60 * DEGREES, axis=UP, about_point=source_points.get_points()[0], run_time=5),
            frame.animate.reorient(-48, -46, 0, (1.17, -0.41, 1.55), 9.28),
            run_time=5
        )
        self.wait(3)
