# ==============================================================================
# Scene:      SuperpositionOfPoints
# Source:     videos/_2024/holograms/diffraction.py (lines 3490-3783)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SuperpositionOfPoints.py SuperpositionOfPoints -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - PiCreaturePointCloud.csv (Grant's scan, it was in his output folder) is now read from _lib/data/2024/holograms/data/; the file is a synthetic cloud shaped like the pi creature
#   - `set_uniforms(dict(x.uniforms))` fails because `uniforms` is now a structured array: `x.uniforms` is passed directly
#
# Placeholder assets (not Grant's originals):
#   - _lib/data/2024/holograms/data/PiCreaturePointCloud.csv  (500 000 x,y,z points inside the silhouette of a PiCreature; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
#
# Notes:
#   The published video is the one from the 360p, 10 fps test: at 720p it takes too long (more than 500 s at 360p).
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


class SuperpositionOfPoints(InteractiveScene):
    def construct(self):
        # Set up pi creature dot cloud
        frame = self.frame
        self.set_floor_plane("xz")

        # CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
        data_file = Path(get_directories()["data"], "2024/holograms/data/PiCreaturePointCloud.csv")
        all_points = np.loadtxt(data_file, delimiter=',', skiprows=1)
        all_points = all_points[:int(0.8 * len(all_points))]  # Limit to first 400k
        dot_cloud = DotCloud(all_points)
        dot_cloud.set_height(4).center()
        dot_cloud.rotate(50 * DEGREES, DOWN)
        points = dot_cloud.get_points().copy()
        max_z_index = np.argmax(points[:, 2])
        min_z_index = np.argmin(points[:, 2])
        all_points = np.array([points[max_z_index], points[min_z_index], *points])

        dot_cloud.set_points(all_points[:100_000])
        dot_cloud.set_radius(0.02)

        # Add axes, points and plate
        plate_center = 5 * IN
        axes = ThreeDAxes(x_range=(-6, 6), y_range=(-4, 4), z_range=(-4, 8))
        axes.shift(plate_center - axes.get_origin())

        dist_point = 1000 * OUT
        dot_cloud.set_points(np.array([2 * LEFT, 2 * LEFT, dist_point]))
        dot_cloud.set_color(BLUE_B)
        dot_cloud.set_radius(0.5)
        dot_cloud.set_glow_factor(2)

        plate = LightIntensity(dot_cloud)
        plate.set_color(WHITE)
        plate.set_shape(16, 9)
        plate.set_height(6)
        plate.move_to(plate_center)
        plate.set_wave_number(16)
        plate.set_max_amp(4)
        plate.set_decay_factor(0)

        frame.reorient(-66, -21, 0, (-0.95, 0.41, -1.11), 11.73)
        frame.clear_updaters()
        frame.add_ambient_rotation(1 * DEGREES)
        self.add(axes)
        self.add(plate)
        self.add(dot_cloud)

        # Separate out pair of points
        point_sets = [
            (2 * LEFT, RIGHT + OUT),
            (2 * LEFT + IN, RIGHT + OUT),
            (2 * LEFT + IN, 3 * RIGHT + 2 * IN),
            (LEFT + 2 * OUT, RIGHT + OUT),
        ]

        for point_set in point_sets:
            self.play(
                dot_cloud.animate.set_points([*point_set, dist_point]),
                run_time=3
            )
            self.wait(2)

        # Zoom in on the plate
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(-18, -11, 0, (-1.52, 1.18, -0.67), 0.92),
            run_time=6,
        )
        self.wait()

        dot_cloud.set_points([point_sets[-1][0], dist_point])
        plate.set_max_amp(3)
        self.wait(2)
        dot_cloud.set_points([point_sets[-1][1], dist_point])
        self.wait(2)
        dot_cloud.set_points([*point_sets[-1], dist_point])
        plate.set_max_amp(4)
        self.play(
            frame.animate.reorient(61, -7, 0, (0.61, -0.11, -2.44), 8.66),
            run_time=5
        )

        # Add on up to 32 points
        self.play(
            dot_cloud.animate.set_points([*all_points[:2], dist_point]).set_radius(0.2),
            run_time=8
        )
        frame.clear_updaters()
        frame.add_ambient_rotation(0.5 * DEGREES)
        self.play(
            UpdateFromAlphaFunc(
                dot_cloud,
                lambda m, a: m.set_points(
                    [*all_points[:int(2 + a * 29)], dist_point]
                )
            ),
            UpdateFromFunc(plate, lambda m: m.set_max_amp(2 * np.sqrt(dot_cloud.get_num_points()))),
            run_time=10
        )
        self.wait(2)

        # Describe as a combination of zone plates
        zone_plates = Group()
        for point in all_points[:30]:
            zone_plate = LightIntensity(DotCloud([point, dist_point]))
            # CHANGE: `uniforms` is no longer a dict but a structured array (Uniforms); set_uniforms receives it as is
            zone_plate.set_uniforms(plate.uniforms)
            zone_plate.match_points(plate)
            zone_plate.set_max_amp(10)
            zone_plate.set_opacity(0.25)
            zone_plates.add(zone_plate)

        zone_plates.deactivate_depth_test()
        self.remove(plate)
        self.add(zone_plates)

        for n, zone_plate, point in zip(it.count(1), zone_plates, all_points[:30]):
            zone_plate.shift(1e-2 * IN)
            zone_plate.save_state()
            zone_plate.scale(0).move_to(point).set_max_amp(2).set_opacity(1)

        self.play(
            UpdateFromAlphaFunc(plate, lambda m, a: m.set_opacity(1 - there_and_back_with_pause(a, 0.6))),
            LaggedStartMap(Restore, zone_plates, lag_ratio=0.05),
            frame.animate.reorient(66, -18, 0, (1.44, 0.59, -6.18), 16.05),
            run_time=5
        )
        self.play(FadeOut(zone_plates))

        # Move around points
        frame.clear_updaters()
        frame.add_ambient_rotation(-2 * DEGREES)

        dot_cloud.save_state()
        self.play(dot_cloud.animate.shift(2 * IN), run_time=3)
        self.play(Rotate(dot_cloud, PI / 2 , axis=UP, about_point=ORIGIN), run_time=3)
        self.play(Restore(dot_cloud), run_time=3)
        self.wait(3)

        # Show reference wave through it
        rect = Rectangle().replace(plate, stretch=True)
        rect.insert_n_curves(20)
        beam = VGroup(
            Line(25 * OUT, rect.pfp(a))
            for a in np.linspace(0, 1, 500)
        )
        beam.set_stroke(GREEN_SCREEN, (1, 0), 0.5)
        beam.shuffle()

        self.play(
            ShowCreation(beam, lag_ratio=1 / len(beam)),
            FadeOut(dot_cloud),
            frame.animate.reorient(83, -27, 0, (-0.63, -0.01, -0.79), 14.36),
            run_time=2
        )
        frame.clear_updaters()
        dot_cloud.set_color(GREEN_SCREEN)

        # Test
        frame.reorient(-26, -9, 0, (0.15, -0.46, -0.42), 15.13)
        self.play(frame.animate.reorient(0, 0, 0, (0.53, 0.16, -0.0), 0.22), run_time=8)
        self.play(frame.animate.reorient(3, 0, 0, (0.14, -0.02, 0.03), 0.22), run_time=8)

        # Build it up again from the other side
        self.play(
            plate.animate.set_opacity(0.2).set_anim_args(time_span=(1.6, 1.7)),
            frame.animate.reorient(162, -3, 0, (-0.89, 0.06, 0.03), 12.77),
            run_time=4,
        )
        dot_cloud.set_points([all_points[0], dist_point])
        plate.set_max_amp(2 * np.sqrt(dot_cloud.get_num_points()))
        self.add(dot_cloud)
        self.wait()
        self.play(
            UpdateFromAlphaFunc(
                dot_cloud,
                lambda m, a: m.set_points(
                    [*all_points[:int(1 + a * 29)], dist_point]
                )
            ),
            UpdateFromFunc(plate, lambda m: m.set_max_amp(2 * np.sqrt(dot_cloud.get_num_points()))),
            frame.animate.reorient(207, -8, 0, (-0.89, 0.06, 0.03), 12.77),
            run_time=12
        )
        self.wait(2)

        # Close up on cloud
        self.play(
            FadeOut(beam),
            FadeOut(dot_cloud),
            frame.animate.reorient(185, -39, 0, (-0.89, 0.06, 0.03), 12.77).set_anim_args(run_time=3),
        )
        dot_cloud.set_color(BLUE).set_glow_factor(1).set_radius(0.1)
        self.play(
            FadeOut(plate),
            FadeIn(dot_cloud),
            frame.animate.reorient(115, -16, 0, (0.33, 0.28, -0.52), 4.38),
            run_time=3
        )

        # Denser cloud
        self.play(
            UpdateFromAlphaFunc(
                dot_cloud,
                lambda m, a: m.set_points(
                    [*all_points[:int(interpolate(31, 500, a))], dist_point]
                ).set_glow_factor(interpolate(1, 0, a**0.25)).set_radius(interpolate(0.1, 0.02, a**0.25)).set_opacity(interpolate(1, 0.5, a**0.25)),
            ),
            run_time=4
        )
        self.play(
            UpdateFromAlphaFunc(
                dot_cloud,
                lambda m, a: m.set_points(
                    [*all_points[:int(interpolate(500, len(all_points), a**3))]]
                ).set_radius(interpolate(0.02, 0.01, a)).set_opacity(interpolate(0.5, 0.2, a)),
            ),
            run_time=5
        )

        # Add better updating film
        sheet_dots = self.create_dot_sheet(plate.get_width(), plate.get_height(), radius=0.025, z=plate.get_z())
        self.color_sheet_by_exposure(sheet_dots, dot_cloud.get_points()[:1000], wave_number=32)
        self.add(sheet_dots)

        self.play(
            frame.animate.reorient(-16, -45, 0, (-0.97, 1.52, -1.18), 8.67),
            run_time=2,
        )
        frame.clear_updaters()
        frame.add_ambient_rotation(3 * DEGREES)

        # Move dot cloud around
        self.play(
            dot_cloud.animate.shift(2 * IN),
            UpdateFromFunc(sheet_dots, lambda m: self.color_sheet_by_exposure(m, dot_cloud.get_points()[:1000], wave_number=32)),
            run_time=3,
        )
        self.wait(3)
        self.play(
            Rotate(dot_cloud, 120 * DEGREES, axis=UP),
            UpdateFromFunc(sheet_dots, lambda m: self.color_sheet_by_exposure(m, dot_cloud.get_points()[:1000], wave_number=32)),
            run_time=3,
        )
        self.wait(3)
        self.play(
            dot_cloud.animate.shift(3 * OUT),
            UpdateFromFunc(sheet_dots, lambda m: self.color_sheet_by_exposure(m, dot_cloud.get_points()[:1000], wave_number=32)),
            run_time=3,
        )
        self.wait(3)

        # Transform point into film
        frame.clear_updaters()
        frame.reorient(111, -13, 0, (-0.54, 0.04, -1.71), 5.72)
        pre_dots = dot_cloud.copy()
        pre_dots.set_points(dot_cloud.get_points()[:len(sheet_dots.get_points())])

        self.play(
            TransformFromCopy(pre_dots, sheet_dots, time_span=(2, 8)),
            frame.animate.reorient(17, -19, 0, (0.82, 0.57, -3.07), 7.99),
            run_time=12
        )
        self.play(
            dot_cloud.animate.shift(2 * IN),
            UpdateFromFunc(sheet_dots, lambda m: self.color_sheet_by_exposure(m, dot_cloud.get_points()[:1000], wave_number=32)),
            run_time=3,
        )
        self.wait()

    def color_sheet_by_exposure(self, sheet_dots, point_sources, wave_number=16, opacity=0.5):
        centers = sheet_dots.get_points()
        diffs = centers[:, np.newaxis, :] - point_sources[np.newaxis, :, :]
        distances = np.linalg.norm(diffs, axis=2)
        amplitudes = np.exp(distances * TAU * 1j * wave_number).sum(1)
        mags = abs(amplitudes)
        max_amp = 2 * np.sqrt(len(point_sources))
        opacities = opacity * np.clip(mags / max_amp, 0, 1)
        sheet_dots.set_opacity(opacities)
        return sheet_dots

    def create_dot_sheet(self, width=4, height=4, radius=0.05, z=0, make_3d=False):
        # Add dots
        dots = DotCloud()
        dots.set_color(WHITE)
        dots.to_grid(int(height / radius), int(width / radius))
        dots.set_shape(width, height)
        dots.set_radius(radius)
        dots.set_z(z)

        if make_3d:
            dots.make_3d()

        return dots
