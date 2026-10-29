# ==============================================================================
# Scene:      CreateZonePlate
# Source:     videos/_2024/holograms/diffraction.py (lines 1116-1603)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CreateZonePlate.py CreateZonePlate -w -m --fps 15
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


class CreateZonePlate(DiffractionGratingScene):
    samples = 4

    def construct(self):
        # Create object and reference wave
        frame = self.frame
        axes = ThreeDAxes()
        self.set_floor_plane("xz")

        wave_width = 100
        wave_number = 4
        frequency = 1

        ref_wave = self.get_plane_wave(direction=IN)
        ref_wave.set_opacity(0.75)
        ref_source = ref_wave.point_sources
        source_point = GlowDot(OUT, color=WHITE, radius=0.5)
        obj_wave = LightWaveSlice(source_point)
        obj_wave.set_decay_factor(0.7)

        for wave in [obj_wave, ref_wave]:
            wave.set_width(wave_width)
            wave.rotate(PI / 2, RIGHT, about_point=ORIGIN)
            wave.center()
            wave.set_wave_number(wave_number)
            wave.set_frequency(frequency)

        frame.reorient(-32, -21, 0, (-0.74, 0.32, -0.49), 7.08)

        def get_all_sources():
            return np.vstack([
                obj_wave.point_sources.get_points(),
                ref_wave.point_sources.get_points()
            ])

        # Add film
        plate = Rectangle(16, 9)
        plate.set_height(4)
        plate.set_stroke(WHITE, 1, 0.5).set_fill(BLACK, 0.0)
        plate.set_shading(0.1, 0.1, 0)
        plate.apply_depth_test()
        plate_body = Square3D()
        plate_group = Group(plate_body, plate)

        plate_body.set_color(BLACK, 0.9)
        plate_body.set_shape(plate.get_width(), plate.get_height())
        plate_body.move_to(plate.get_center() + 1e-2 * IN)

        exposure = LightIntensity(DotCloud(get_all_sources()))
        exposure.set_decay_factor(0)
        exposure.set_wave_number(wave_number)
        exposure.replace(plate, stretch=True).shift(1e-2 * OUT)
        exposure.set_color(WHITE, 0.85)

        film = Group(plate, exposure)
        film.set_height(4)
        film.set_z(-2)

        film_label = Text("Film")
        film_label.next_to(plate, UP)
        film_label.set_backstroke(BLACK, 3)
        film_label.set_z_index(1)

        # Label object wave
        source_label = Text("Object (idealized point)", font_size=24)
        source_label.next_to(source_point, UR, buff=0)
        source_label.shift(0.25 * UL)
        source_label.set_backstroke(BLACK, 2)
        source_arrow = Arrow(source_label["Object"].get_bottom(), source_point.get_center(), buff=0.1)
        source_arrow.always.set_perpendicular_to_camera(self.frame)
        obj_point = TrueDot()
        obj_point.move_to(source_point)

        obj_wave_label = Text("Object wave")
        obj_wave_label.rotate(PI / 2, LEFT)
        obj_wave_label.next_to(source_point, IN, buff=0.1)
        obj_wave_label.set_backstroke(BLACK, 2)

        frame.reorient(41, -9, 0, (-0.72, 0.27, -0.49), 6.75)
        self.add(plate_group, obj_wave, film_label)
        plate_body.move_to(plate.get_center() + 1e-2 * IN)
        self.play(
            FadeIn(source_point),
            FadeIn(source_label),
            GrowArrow(source_arrow),
            frame.animate.reorient(-4, -10, 0, (-0.74, 0.32, -0.49), 7.08).set_anim_args(run_time=5)
        )
        self.play(
            TransformMatchingStrings(source_label, obj_wave_label),
            FadeOut(source_arrow),
            frame.animate.reorient(0, -47, 0, (-0.74, 0.32, -0.49), 7.08).set_anim_args(run_time=3),
        )
        self.wait(3)

        # Label reference wave
        ref_wave.match_width(film, stretch=True)
        ref_wave.move_to(film, IN)
        ref_wave_label = Text("Reference wave")
        ref_wave_label.rotate(PI / 2, LEFT)
        ref_wave_label.next_to(obj_wave_label, OUT, buff=1.5)
        ref_wave_label.set_backstroke(BLACK, 2)

        wave_fronts = Group(
            plate.copy().set_color([BLUE, RED][z % 2], 0.15).shift(0.5 * z * OUT)
            for z in range(4, 16)
        )
        for front in wave_fronts:
            front.add_updater(lambda m, dt: m.shift(dt * (frequency / wave_number) * IN))

        self.play(
            FadeOut(obj_wave, 0.1 * DOWN),
            FadeOut(obj_wave_label),
            FadeOut(source_point),
            FadeIn(ref_wave, 0.1 * DOWN),
            FadeIn(ref_wave_label),
            frame.animate.reorient(0, -40, 0, (-0.16, 0.01, -0.24), 7.08).set_anim_args(run_time=4),
        )
        self.play(
            FadeIn(wave_fronts, time_span=(0, 2), lag_ratio=0.05),
            frame.animate.reorient(0, -37, 0, (-0.16, 0.01, -0.24), 7.08),
            run_time=8
        )
        self.play(FadeOut(wave_fronts, run_time=2, lag_ratio=0.1))
        self.add(ref_source)

        # Put reference at an angle
        angle = 60 * DEGREES
        direction = rotate_vector(OUT, angle, axis=UP)
        dist = ref_wave.get_depth()
        ref_wave.save_state()
        ref_wave.point_sources.save_state()
        ref_wave.target = ref_wave.generate_target()
        p0 = film.get_left()
        p1 = film.get_right()
        p2 = p0 + dist * direction
        p3 = p1 + dist * direction
        ref_wave.target.set_points([p2, p0, p3, p1])

        self.play(
            MoveToTarget(ref_wave, run_time=2),
            Rotate(ref_wave.point_sources, angle, axis=UP, about_point=ORIGIN),
            Rotate(ref_wave_label, angle, axis=UP, about_point=film.get_center()),
            run_time=10,
            rate_func=lambda t: there_and_back_with_pause(t, 0.5)
        )
        self.wait(8)

        # Also show the object wave from this perspective
        self.remove(ref_wave, ref_wave_label)
        self.add(obj_wave, obj_wave_label, source_point)
        obj_wave_label.shift(0.25 * OUT)
        self.wait(8)

        # Show combined wave
        comb_label = Text("Combined wave")
        comb_label.rotate(PI / 2, LEFT)
        comb_label.next_to(ref_wave_label, UP)
        comb_label.set_backstroke(BLACK, 3)
        comb_wave = obj_wave.copy()
        comb_wave.point_sources = DotCloud([
            *(source_point.get_center() for x in range(2)),
            *np.linspace(20 * OUT + 4 * LEFT, 20 * OUT + 4 * RIGHT, 25)
        ])
        comb_wave.set_decay_factor(0.8)
        comb_wave.set_max_amp(1.5)

        self.remove(obj_wave, obj_wave_label)
        self.add(comb_wave, comb_label, source_point)
        self.wait(8)

        # Preview exposure
        self.add(exposure, comb_wave, comb_label)
        self.play(FadeIn(exposure, run_time=3))
        self.wait(8)

        # Change to side view
        self.play(
            FadeOut(comb_label),
            comb_wave.animate.set_opacity(0.1),
            FadeOut(film_label),
            FadeOut(exposure),
            frame.animate.reorient(80, -2, 0, (-0.64, 0.23, -0.93), 4.34),
            run_time=5
        )

        # Add graphs to middle
        ref_source.get_center()
        ref_source.move_to(source_point.get_center() + ((1000 // wave_number) * wave_number) * OUT)
        ref_wave.set_uniform(time=obj_wave.uniforms["time"])

        obj_color, ref_color = colors = [TEAL, YELLOW]
        obj_line, ref_line = lines = VGroup(
            Line(source_point.get_center(), film.get_center()).set_stroke(color, 1, 0.5)
            for color in colors
        )
        ref_line.scale(2, about_point=ref_line.get_end())
        ref_line.shift(0.02 * RIGHT)

        obj_graph, ref_graph = graphs = VGroup(
            self.get_graph_over_wave(line, wave, scale_factor=sf, direction=UP, color=color)
            for line, color, wave, sf in zip(lines, colors, [obj_wave, ref_wave], [0.15, 0.1])
        )
        graphs.set_stroke(width=2, opacity=1)

        obj_label = Text("Object wave", font_size=24).rotate(PI / 2, UP)
        ref_label = Text("Reference wave", font_size=24).rotate(PI / 2, UP)
        obj_label.set_color(obj_color).next_to(obj_graph, UP, aligned_edge=OUT)
        obj_label.shift(0.1 * IN)
        ref_label.set_color(ref_color).next_to(ref_graph, DOWN)
        ref_label.match_z(obj_label).shift(OUT)

        obj_wave.set_opacity(0)
        obj_wave.set_decay_factor(0.5)
        ref_wave.set_opacity(0)

        comb_wave.set_z_index(1)

        self.add(obj_wave, ref_wave)
        self.play(
            ShowCreation(obj_line),
            ShowCreation(obj_graph),
            FadeIn(obj_label, lag_ratio=0.1),
            run_time=2
        )
        self.wait(3)
        self.play(
            ShowCreation(ref_line),
            ShowCreation(ref_graph),
            FadeIn(ref_label, lag_ratio=0.1),
        )
        self.wait(4)

        # Show middle exposure
        round_exposure = self.get_round_exposure(exposure, radius=0.25)

        self.play(
            GrowFromCenter(round_exposure),
            frame.animate.reorient(53, -15, 0, (-0.83, 0.12, -0.62), 5.25).set_anim_args(run_time=3),
        )

        # Look off center
        exposure.replace(plate, stretch=True)
        exposure.set_shape(0.5 * plate.get_width(), 0.25)
        exposure.move_to(plate.get_center(), LEFT).shift(1e-2 * OUT)
        full_exposure = exposure.copy()
        full_exposure.replace(plate, stretch=True)
        full_exposure.shift(2e-2 * OUT)
        exposure.save_state()
        exposure.stretch(0, 0, about_edge=LEFT)

        O_point = obj_label[0].get_center()
        obj_label.add_updater(
            lambda m: m.rotate(
                angle_of_vector((m[-1].get_center() - m[0].get_center())[0::2]) - angle_of_vector(obj_line.get_vector()[0::2]),
                axis=UP,
            ).shift(O_point - m[0].get_center())
        )

        trg_point = VectorizedPoint(plate.get_center())
        obj_line.add_updater(lambda m: m.put_start_and_end_on(source_point.get_center(), trg_point.get_center()))
        ref_line.add_updater(lambda m: m.move_to(trg_point.get_center() + 0.02 * RIGHT, IN))

        self.play(
            obj_wave.animate.pause(),
            ref_wave.animate.pause(),
            comb_wave.animate.pause(),
        )
        self.play(
            trg_point.animate.move_to(film.get_right()),
            round_exposure.animate.shift(0.01 * OUT),
            MaintainPositionRelativeTo(ref_label, ref_line),
            Restore(exposure),
            frame.animate.reorient(35, -14, 0, (1.01, 0.23, -2.8), 8.40),
            run_time=12
        )
        self.wait(2)

        # Look to halfwavelength point
        trg_x = 0.9
        mid_line = Line(source_point.get_center(), plate.get_center())
        mid_line.set_stroke(TEAL, 2)
        mid_line_label = Tex("D", font_size=30).rotate(PI / 2, LEFT)
        mid_line_label.next_to(mid_line, LEFT)
        d_line_label = Tex(R"D + \frac{\lambda}{2}", font_size=30).rotate(PI / 2, LEFT)
        VGroup(mid_line_label, d_line_label).set_fill(TEAL, 1)

        self.play(
            FadeOut(obj_label),
            FadeOut(ref_label),
            FadeOut(ref_line),
            FadeOut(ref_graph),
            frame.animate.reorient(0, -62, 0, (-0.27, -1.26, -1.17), 7.38),
            trg_point.animate.move_to(plate.get_center() + trg_x * RIGHT),
            run_time=3
        )
        d_line_label.next_to(obj_line.get_center(), RIGHT, buff=SMALL_BUFF)
        self.play(
            FadeIn(mid_line),
            FadeIn(mid_line_label),
            FadeIn(d_line_label),
        )
        self.wait(2)
        self.play(
            frame.animate.reorient(84, -9, 0, (-0.26, -0.27, -1.86), 3.23),
            FadeOut(VGroup(mid_line, mid_line_label, d_line_label)),
            FadeIn(ref_line),
            FadeIn(ref_graph),
            obj_wave.animate.unpause(),
            ref_wave.animate.unpause(),
            comb_wave.animate.unpause(),
            run_time=5,
        )
        self.wait(5)

        # Show the circle
        circle = Circle(radius=trg_x)
        circle.move_to(film)
        circle.set_stroke(GREY_D, 1)

        tail = TracingTail(circle.get_end, stroke_color=BLUE_D, stroke_width=(0, 3))

        self.add(tail)
        self.wait()
        self.add(circle, tail)
        round_exposure.set_width(0.25)
        self.play(
            frame.animate.reorient(41, -15, 0, (-0.54, -0.17, -1.78), 4.65),
            ShowCreation(circle),
            UpdateFromFunc(trg_point, lambda m, c=circle: m.move_to(c.get_end())),
            round_exposure.animate.set_width(3),
            FadeOut(exposure, time_span=(0, 1)),
            run_time=4
        )
        self.play(FadeOut(circle, run_time=2))
        self.remove(tail)
        self.wait(2)

        # Grow rings fully
        exposure.replace(plate, stretch=True).shift(0.01 * OUT)

        self.add(exposure, round_exposure)
        self.play(
            FadeOut(round_exposure, run_time=2),
            FadeIn(exposure, run_time=2),
            comb_wave.animate.set_opacity(0.5).set_anim_args(time_span=(6, 8)),
            frame.animate.reorient(0, -23, 0, (-0.14, 0.01, -2.23), 6.52).set_anim_args(run_time=8)
        )

        # Just kinda hang for a bit
        time0 = self.time
        frame.add_updater(lambda m, t0=time0, sc=self: m.set_theta(math.sin(0.1 * (sc.time - t0)) * 30 * DEGREES))
        self.play(trg_point.animate.move_to(film.get_left()), run_time=10)
        self.play(trg_point.animate.move_to(film.get_right()), run_time=20)
        self.wait(5)
        frame.clear_updaters()

        # Change wavelength
        trg_wave_number = 16

        for wave in [obj_wave, ref_wave, comb_wave, exposure]:
            wave.set_wave_number(trg_wave_number)
            wave.set_frequency(0.25 * trg_wave_number)

        ref_line.insert_n_curves(1000)
        obj_line.insert_n_curves(1000)
        ref_graph.set_stroke(width=1)
        obj_graph.set_stroke(width=1)

        self.wait(4)
        self.play(
            FadeOut(VGroup(ref_line, ref_graph, obj_line, obj_graph)),
            FadeOut(comb_wave)
        )

        # Bring objet closer in
        self.play(
            frame.animate.reorient(-85, -9, 0, (0.65, -0.24, -0.14), 6.52),
            run_time=4
        )
        exposure.point_sources.set_points([OUT, 1001 * OUT])
        exposure.point_sources.set_radius(0)

        mid_line = Line()
        mid_line.set_stroke(TEAL, 2)

        def get_film_point():
            x, y, _ = source_point.get_center()
            z = film.get_z()
            return np.array([x, y, z])

        mid_line.add_updater(lambda m: m.set_points_as_corners([source_point.get_center(), get_film_point()]))

        def get_dist_label():
            label = DecimalNumber(mid_line.get_length(), font_size=24)
            label.set_backstroke(BLACK, 3)
            label.rotate(PI / 2, DOWN)
            label.next_to(mid_line, UP, SMALL_BUFF)
            return label

        dist_label = always_redraw(get_dist_label)

        self.play(
            ShowCreation(mid_line, suspend_mobject_updating=True),
            VFadeIn(dist_label),
        )

        for vect in [2 * IN, 4 * OUT, 2 * IN]:
            self.play(
                source_point.animate.shift(vect),
                exposure.point_sources.animate.shift(vect),
                run_time=3
            )
            self.wait()

        # Move in 3d
        axes = ThreeDAxes()
        axes.match_width(film)
        axes.move_to(film)
        mid_line.set_z_index(1)
        dist_label.clear_updaters()

        self.play(
            Write(axes, lag_ratio=0.01),
            frame.animate.reorient(-44, -21, 0, (0.09, -0.06, -1.4), 7.22),
            exposure.animate.set_opacity(0.5),
            FadeOut(dist_label),
            run_time=3
        )

        frame.add_ambient_rotation(2 * DEGREES)
        exposure.point_sources.add_updater(lambda m: m.move_to(source_point, IN))
        points = [RIGHT, RIGHT + IN, 3 * LEFT + IN, 3 * LEFT + 2 * OUT, 2 * OUT + 3 * RIGHT + 2 * UP, UR, OUT]
        for point in points:
            self.play(source_point.animate.move_to(point), run_time=2)
            self.wait()
        frame.clear_updaters()
        self.play(
            FadeOut(axes),
            FadeOut(mid_line),
            FadeOut(source_point),
        )

        # Shine the reference through it
        ref_wave.set_opacity(0.75)
        ref_wave.set_wave_number(4.0)
        ref_wave.set_frequency(1.0)
        ref_wave.unpause()

        self.add(exposure, ref_wave)
        self.play(
            FadeIn(ref_wave, time_span=(0, 2)),
            frame.animate.reorient(0, -24, 0, (0.08, -0.07, -1.39), 7.22),
            run_time=5
        )
        self.wait(4)

        # Go to other side
        frame.reorient(-171, -18, 0, (0.12, -0.21, -1.33), 9.31)
        self.remove(film)
        self.add(exposure, plate)
        self.play(
            frame.animate.reorient(0, -16, 0, (-3.06, -0.18, -3.19), 1.49),
            run_time=10,
        )
        self.wait(4)

    def get_round_exposure(self, exposure, radius=1.0, n_pieces=128):
        d_theta = TAU / n_pieces
        vects = [rotate_vector(RIGHT, theta) for theta in np.linspace(0, TAU, n_pieces + 1)]
        result = Group(
            exposure.copy().set_points([ORIGIN, v1, v2])
            for v1, v2 in zip(vects, vects[1:])
        )
        result.set_width(radius)
        result.move_to(exposure)
        return result

        self.add(round_exposure)

    def get_3d_waves(self, wave, x_range=(-4, 4, 0.5), opacity=0.25):
        waves = Group(
            wave.copy().rotate(PI / 2, OUT).move_to(x * RIGHT)
            for x in np.arange(*x_range)
        )
        waves.set_opacity(opacity)
        cam_point = self.frame.get_implied_camera_location()
        waves.sort(lambda p: -get_norm(p - cam_point))
        return waves
