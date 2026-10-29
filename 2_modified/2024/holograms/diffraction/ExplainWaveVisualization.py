# ==============================================================================
# Scene:      ExplainWaveVisualization
# Source:     videos/_2024/holograms/diffraction.py (lines 963-1113)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExplainWaveVisualization.py ExplainWaveVisualization -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `VectorField` changed its API in manimgl (it requires coordinate_system and `sample_coords`; it no longer accepts sample_points/width/height/x_density): the `make_vector_field` wrapper was added with an identity coordinate system
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


class ExplainWaveVisualization(DiffractionGratingScene):
    def construct(self):
        # Set up the wave
        full_width = 20
        frame = self.frame

        source = GlowDot(ORIGIN, color=WHITE)
        source.set_radius(0.5)
        wave = LightWaveSlice(source)
        wave.set_width(full_width)
        wave.move_to(ORIGIN)

        frame.reorient
        self.add(wave, source)

        # Talk through what's displayed
        def field_func(points):
            result = np.zeros_like(points)
            result[:, 2] = 0.5 * wave.wave_func(points)
            return result

        linear_field = make_vector_field(
            field_func,
            sample_points=np.linspace(ORIGIN, 10 * UP, 100),
            max_vect_len=1.0,
        )
        linear_field.always.update_vectors()
        linear_field.set_stroke(WHITE, width=1.5, opacity=0.75)
        full_field = make_vector_field(
            field_func,
            width=full_width,
            height=full_width,
            x_density=5,
            y_density=5,
            max_vect_len=0.5,
        )
        full_field.sample_points
        full_field.set_stroke(WHITE, width=1.5, opacity=0.25)
        full_field.always.update_vectors()

        self.play(
            frame.animate.reorient(71, 77, 0, (-0.62, 0.7, 0.19), 3.11),
            wave.animate.set_uniform(time_rate=0.5).set_anim_args(suspend_mobject_updating=False),
            VFadeIn(full_field, time_span=(0, 2)),
            run_time=6
        )
        self.wait(2)
        self.play(
            VFadeIn(linear_field),
            VFadeOut(full_field),
        )
        self.wait(5)
        self.wait_until(lambda: 15 / 30 < wave.uniforms["time"] % 1 < 16 / 30)
        self.play(
            wave.animate.pause().set_anim_args(suspend_mobject_updating=False),
        )
        self.wait()

        # Show example vectors
        sample_vect = Vector(OUT, thickness=1.0)
        sample_vect.set_fill(WHITE, 1, border_width=0.5)
        sample_vect.base_point = Dot(0.705 * UP, fill_color=BLUE, radius=0.02)

        def update_sample_vect(vect):
            point = vect.base_point.get_center()
            vect.put_start_and_end_on(point, point + 0.95 * field_func([point])[0])
            vect.set_perpendicular_to_camera(self.frame)

        update_sample_vect(sample_vect)

        self.play(
            linear_field.animate.set_stroke(opacity=0.2),
            GrowArrow(sample_vect, run_time=2),
            frame.animate.reorient(81, 84, 0, (-0.5, 0.69, 0.23), 1.65).set_anim_args(run_time=3)
        )
        self.wait()
        self.play(FadeIn(sample_vect.base_point, 0.1 * IN))
        self.wait()
        sample_vect.add_updater(update_sample_vect)
        self.play(sample_vect.base_point.animate.move_to(1.315 * UP).set_color(RED), run_time=3)
        self.wait()
        self.play(sample_vect.base_point.animate.move_to(1.01 * UP).set_color(GREY_E), run_time=2)
        self.wait()
        self.play(
            VFadeOut(sample_vect, time_span=(0, 2)),
            FadeOut(sample_vect.base_point, time_span=(0, 2)),
            linear_field.animate.set_stroke(opacity=0.75).set_anim_args(time_span=(0, 2)),
            wave.animate.set_uniform(time_rate=0.5).set_anim_args(suspend_mobject_updating=False),
            frame.animate.reorient(49, 79, 0, (-0.14, 1.34, 0.23), 2.78),
            run_time=5,
        )
        self.wait(2)

        # Show full 3d field
        full_field = make_vector_field(
            lambda p: 0.5 * field_func(p),
            x_density=4,
            y_density=4,
            z_density=2,
            depth=4,
            max_vect_len=0.5,
        )
        full_field.set_stroke(WHITE, width=1, opacity=0.25)
        full_field.always.update_vectors()

        added_waves = Group(
            wave.copy().rotate(PI / 2, UP).shift(z * RIGHT).set_opacity(0.1)
            for z in np.arange(-2, 2, 0.1)
        )

        self.play(
            # VFadeIn(full_field),
            VFadeOut(linear_field),
            FadeIn(added_waves, suspend_mobject_updating=False),
            frame.animate.reorient(48, 79, 0, (-0.42, 1.07, 0.35), 4.18).set_anim_args(run_time=8)
        )
        wave.save_state()
        wave.scale(0)
        self.play(
            Restore(wave, suspend_mobject_updating=False),
            FadeOut(added_waves, time_span=(0, 1), suspend_mobject_updating=False),
            run_time=3,
        )
        self.wait(2)

        # Show a sine wave
        line = Line(ORIGIN, 10 * UR)
        line.shift(source.get_center())
        line.set_stroke(TEAL, 2)
        graph = self.get_graph_over_wave(line, wave)
        graph.set_stroke(WHITE, 2)
        wave.set_z_index(1)
        source.set_z_index(1)

        linear_field = make_vector_field(
            field_func,
            sample_points=line.get_anchors()[::2],
            max_vect_len=1.0,
        )
        linear_field.set_stroke(WHITE, 0.75)
        linear_field.always.update_vectors()

        self.add(line, graph)
        self.play(
            ShowCreation(line, time_span=(0, 3)),
            ShowCreation(graph, time_span=(0, 3)),
            VFadeIn(linear_field, time_span=(0, 3), suspend_mobject_updating=False),
            frame.animate.reorient(0, 73, 0, (-0.03, 1.7, 0.2), 4.65),
            run_time=10
        )
        self.wait(8)
