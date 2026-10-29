# ==============================================================================
# Scene:      LightFieldAroundScene
# Source:     videos/_2024/holograms/diffraction.py (lines 215-356)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightFieldAroundScene.py LightFieldAroundScene -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The image folder from Grant's Dropbox (/Users/grant/...) was changed to _lib/assets/raster_images/LightFieldDraft, with placeholders for the scene, the top cutoff and the lamp
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/LightFieldDraft/LightFieldScene.png  (placeholder RGBA 1600x1000; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/LightFieldDraft/TopHalfCutoff.png  (placeholder RGBA 1600x1000; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#   - _lib/assets/raster_images/LightFieldDraft/Lamp.png  (placeholder RGBA 1600x1000; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
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


class LightFieldAroundScene(InteractiveScene):
    def construct(self):
        # Add scene
        frame = self.frame
        # CHANGE: the images from Grant's Dropbox folder were replaced by placeholders in _lib/assets/raster_images/LightFieldDraft
        folder = "LightFieldDraft"
        scene, scene_top, lamp = group = Group(
            ImageMobject(os.path.join(folder, "LightFieldScene")),
            ImageMobject(os.path.join(folder, "TopHalfCutoff")),
            ImageMobject(os.path.join(folder, "Lamp")),
        )
        group.set_height(7)
        group.to_edge(RIGHT)

        light_point = scene.get_corner(UL) + 1.6 * RIGHT + 0.8 * DOWN
        scene_point = scene.get_center() + 0.8 * RIGHT + 0.4 * DOWN

        frame.reorient(0, 0, 0, (3.44, -0.2, 0.0), 4.78)
        self.add(scene)
        self.play(FadeIn(scene, 0.25 * UP))
        self.wait()

        # Add light
        line = Line(light_point, scene_point)
        n_dots = 50
        light = Group(
            GlowDot(line.pfp(a), color=WHITE, radius=interpolate(0.5, 4, a), opacity=3 / n_dots)
            for a in np.linspace(0, 1, n_dots)
        )
        self.play(
            FadeIn(lamp, time_span=(1, 3)),
            FadeIn(light, lag_ratio=0.2, time_span=(1, 3)),
            frame.animate.reorient(0, 0, 0, (3.64, 0.68, 0.0), 5.30),
            run_time=2,
        )
        self.wait()

        # Set up wave
        sources = DotCloud([
            (2.42, -0.27, 0.0),
            (1.96, -0.14, 0.0),
            (2.11, 0.05, 0.0),
            (2.51, 0.16, 0.0),
            (2.75, 0.07, 0.0),
            (3.19, 0.41, 0.0),
            (3.48, 0.39, 0.0),
            (4.81, 0.28, 0.0),
            (5.1, 0.22, 0.0),
            (5.53, -0.04, 0.0),
            (5.8, -0.18, 0.0),
            (4.87, -0.58, 0.0),
            (4.71, -0.68, 0.0),
            (4.28, -0.61, 0.0),
            (3.92, -0.51, 0.0),
            (4.18, -0.27, 0.0),
            (3.8, 0.09, 0.0),
            (3.55, 0.23, 0.0),
            (2.43, 0.7, 0.0),
            (2.43, 0.7, 0.0),
            (3.71, 0.51, 0.0),
            (3.94, -0.49, 0.0),
            (1.9, -0.3, 0.0),
            (2.61, 0.06, 0.0),
            (2.92, 0.23, 0.0),
            (3.25, 0.38, 0.0),
        ])
        wave = LightWaveSlice(sources)
        wave.set_max_amp(math.sqrt(30))
        wave.set_shape(50, 100)
        wave.rotate(70 * DEGREES, LEFT)
        wave.set_wave_number(4)
        wave.set_frequency(1)

        n_perp_waves = 10
        perp_waves = Group(wave.copy().rotate(PI / 2, RIGHT).shift(z * OUT) for z in np.linspace(-1, 1, n_perp_waves))
        perp_waves.set_opacity(0.1)

        self.add(scene, wave, perp_waves, scene_top, lamp, light)
        self.play(
            FadeIn(wave),
            FadeIn(perp_waves),
            light.animate.set_opacity(2 / n_dots),
            scene.animate.set_opacity(0.5),
            run_time=2
        )

        # Slow zoom out
        self.play(
            frame.animate.to_default_state(),
            run_time=12
        )

        # Linger
        self.wait(12)

        # Reflection
        if False:
            self.remove(light)
            self.remove(lamp)
            self.frame.set_theta(-10 * DEGREES).set_y(0.5)
            scene_top.set_opacity(0.5)
            self.wait(12)

        # Show an observer
        eye_dot = GlowDot(1.0 * LEFT, radius=0.5, color=WHITE)

        self.play(FadeIn(eye_dot))
        self.wait(3)
        self.play(
            eye_dot.animate.move_to(1.5 * LEFT + 2 * DOWN).set_anim_args(path_arc=45 * DEGREES),
            run_time=12,
            rate_func=there_and_back,
        )
        self.play(FadeOut(eye_dot))

        # Show recreation
        right_rect = FullScreenRectangle().set_fill(BLACK, 1)
        right_rect.stretch(0.35, 0, about_edge=RIGHT)
        film_rect = Rectangle()
        film_rect.set_fill(interpolate_color(RED_E, BLACK, 0.8), 1).set_stroke(WHITE, 1)
        film_rect.rotate(80 * DEGREES, UP)
        film_rect.rotate(20 * DEGREES, RIGHT)
        film_rect.move_to(right_rect.get_left())

        laser_point = RIGHT_SIDE + RIGHT
        laser_light = VGroup(
            Line(laser_point, film_rect.pfp(a + random.random() / 250))
            for a in np.linspace(0, 1, 250)
        )
        laser_light.set_stroke(GREEN_SCREEN, (0, 1), 0.2)
        laser_light.shuffle()

        self.play(
            FadeOut(lamp),
            FadeOut(light),
            FadeOut(scene),
            FadeOut(scene_top),
            FadeIn(right_rect),
            FadeIn(film_rect),
        )
        self.play(ShowCreation(laser_light, lag_ratio=0.001))
        self.wait(12)
        self.wait(2)  # Just in case
