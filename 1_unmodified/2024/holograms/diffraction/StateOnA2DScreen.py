# ==============================================================================
# Scene:      StateOnA2DScreen
# Source:     videos/_2024/holograms/diffraction.py (lines 4092-4158)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StateOnA2DScreen.py StateOnA2DScreen -w -m --fps 15
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


class StateOnA2DScreen(InteractiveScene):
    def construct(self):
        # Add screen
        frame = self.frame
        self.set_floor_plane("xz")

        screen = ScreenRectangle()
        screen.set_height(6)
        screen.set_stroke(WHITE, 1)

        source_points = DotCloud(np.random.random((10, 3)))
        source_points.set_width(8)
        source_points.move_to(screen, OUT)
        wave2d = LightWaveSlice(source_points)
        wave2d.replace(screen, stretch=True)
        wave2d.set_wave_number(4)
        wave2d.set_frequency(1)
        wave2d.set_max_amp(4)
        wave2d.set_decay_factor(0)

        axes = ThreeDAxes((-5, 5), (-5, 5), (-5, 5))

        self.add(axes)
        self.add(screen)
        self.add(wave2d)
        self.wait(4)

        # Zoom out to 3d waves
        wave3d = Group(
            # wave2d.copy().rotate(PI / 2, RIGHT).stretch(10, 2).move_to(ORIGIN, IN)
        )
        n_slices = 3
        for x in np.linspace(-5, 5, n_slices):
            wave_slice = wave2d.copy()
            wave_slice.scale(20)
            wave_slice.rotate(PI / 2, UP)
            wave_slice.move_to(ORIGIN, IN)
            wave_slice.set_x(x)
            wave_slice.set_opacity(1.0 / n_slices)
            wave3d.add(wave_slice)

        for wave in wave3d:
            wave.set_opacity(1)
            wave.set_max_amp(10)

        # wave3d[n_slices // 2].set_opacity(0.75)
        # wave3d.set_opacity(0.1)
        # wave3d.save_state()
        # wave3d.stretch(0, dim=2, about_point=ORIGIN)

        self.play(
            frame.animate.reorient(101, -1, 0, (-0.53, 0.13, 7.82), 13.40),
            FadeIn(wave3d, time_span=(3, 8)),
            run_time=8,
        )

        # Linger and collapse
        self.wait(4)
        self.play(
            LaggedStart(*(
                wave.animate.match_points(wave2d).set_opacity(1).shift(1e-2 * IN)
                for wave in wave3d
            ), lag_ratio=0),
            frame.animate.reorient(25, -6, 0, (0.18, 0.29, 0.15), 9.15).set_anim_args(time_span=(1, 4)),
            run_time=4
        )
        self.wait(8)
