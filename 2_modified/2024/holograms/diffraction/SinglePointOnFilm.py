# ==============================================================================
# Scene:      SinglePointOnFilm
# Source:     videos/_2024/holograms/diffraction.py (lines 862-960)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SinglePointOnFilm.py SinglePointOnFilm -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Private images from Grant's Dropbox (SinglePointHologram.png) replaced with regenerable placeholders
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/SinglePointHologram.png  (placeholder; script: _lib/assets/generated/2024/holograms/make_holograms_assets.py)
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


class SinglePointOnFilm(DiffractionGratingScene):
    def construct(self):
        # Reference image
        img = ImageMobject("SinglePointHologram")
        img.set_height(FRAME_HEIGHT)
        img.fix_in_frame()
        img.set_opacity(0.75)
        # self.add(img)

        # Create object and reference wave
        # Much of this copied from CreateZonePlate below
        frame = self.frame
        frame.set_field_of_view(42 * DEGREES)
        axes = ThreeDAxes()
        self.set_floor_plane("xz")

        wave_width = 100
        wave_number = 2
        frequency = 1

        source_point = GlowDot(color=WHITE, radius=0.5)
        source_point.move_to([0., -0.75, 4.62])
        obj_wave = LightWaveSlice(source_point)
        obj_wave.set_decay_factor(0.7)

        obj_wave.set_width(wave_width)
        obj_wave.rotate(PI / 2, RIGHT, about_point=ORIGIN)
        obj_wave.move_to(source_point)
        obj_wave.set_wave_number(wave_number)
        obj_wave.set_frequency(frequency)

        # Add film
        plate_border = Rectangle(4, 4)
        plate_border.set_fill(BLACK, 0)
        plate_border.set_stroke(WHITE, 2)
        plate_body = Square3D()
        plate_body.set_color(BLACK, 0.9)
        plate_body.replace(plate_border, stretch=True)
        plate_body.set_shading(0.1, 0.1, 0)

        plate = Group(plate_body, plate_border)
        plate.center()

        film_label = Text("Film")
        film_label.next_to(plate, UP)
        film_label.set_backstroke(BLACK, 3)
        film_label.set_z_index(1)

        # Spherical waves
        wave_stack = Group(
            obj_wave.copy().rotate(PI / 2, OUT).set_opacity(0.1)
            for x in range(30)
        )
        wave_stack.set_opacity(0.07)
        wave_stack.arrange_to_fit_width(4)
        wave_stack.sort(lambda p: -p[0])
        wave_stack.move_to(obj_wave)

        # Label object wave
        source_label = Text("Object (idealized point)", font_size=36)
        source_label.next_to(source_point, UR, buff=MED_LARGE_BUFF)
        source_label.shift(0.25 * UL)
        source_label.set_backstroke(BLACK, 2)
        source_arrow = Arrow(source_label["Object"].get_bottom(), source_point.get_center(), buff=0.1)
        source_arrow.set_perpendicular_to_camera(self.frame)
        source_label.add(source_arrow)
        source_label.rotate(PI / 2, DOWN, about_point=source_point.get_center())
        obj_point = TrueDot()
        obj_point.move_to(source_point)

        obj_wave_label = Text("Object wave")
        obj_wave_label.rotate(PI / 2, LEFT)
        obj_wave_label.next_to(source_point, IN, buff=0.1)
        obj_wave_label.set_backstroke(BLACK, 2)

        frame.reorient(-88, -12, 0, (0.22, -0.81, 4.62), 13.76)
        self.add(plate, film_label)
        self.add(obj_wave, wave_stack, obj_point, source_point)
        self.add(source_label)
        self.wait()

        # Slowly reorient
        self.play(
            frame.animate.reorient(-14, -11, 0, (0.27, 0.14, 3.59), 6.17),
            Rotate(source_label, PI / 2, UP, about_point=source_point.get_center()),
            Rotate(wave_stack, PI / 2, UP, about_point=source_point.get_center()),
            run_time=10
        )

        # Look from above
        self.play(
            FadeOut(wave_stack),
            FadeOut(source_label),
            FadeOut(plate),
            FadeOut(film_label),
            obj_wave.animate.set_decay_factor(0.5),
            frame.animate.reorient(0, -90, 0, source_point.get_center(), 4).set_anim_args(run_time=4)
        )
        self.wait(2)
