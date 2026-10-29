# ==============================================================================
# Scene:      PlaneWaveThroughZonePlate
# Source:     videos/_2024/holograms/diffraction.py (lines 2829-3487)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PlaneWaveThroughZonePlate.py PlaneWaveThroughZonePlate -w -m --fps 15
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


class PlaneWaveThroughZonePlate(DiffractionGratingScene):
    def construct(self):
        # Set up the zone plate and object
        frame = self.frame
        wave_number = 4
        frequency = 2.0

        obj_dot = Group(GlowDot(), TrueDot())
        obj_dot.move_to(4 * RIGHT)
        obj_dot.set_color(WHITE)

        zone_sources = DotCloud([obj_dot.get_center(), 1002 * RIGHT])
        plate = LightIntensity(zone_sources)
        plate.set_shape(9, 16)
        plate.rotate(PI / 2, UP)
        plate.set_height(8)
        plate.set_color(WHITE, 0.7)
        plate.set_wave_number(24)
        plate.set_decay_factor(0)
        plate_top = plate.copy()
        plate_top.rotate(PI / 2, DOWN)
        plate_top.set_width(0.075, stretch=True)
        plate_top.move_to(plate)

        ref_wave = self.get_plane_wave(LEFT)
        ref_wave.set_shape(10, plate.get_height())
        ref_wave.set_frequency(frequency)
        ref_wave.set_color(BLUE_C, 0.5)
        ref_wave.set_wave_number(wave_number)
        ref_wave.move_to(plate, LEFT)

        frame.reorient(19, 77, 0, ORIGIN, 8.00)
        self.add(plate)
        self.add(obj_dot)

        # Add Number plane
        plane = NumberPlane(x_range=(-10, 10, 1), y_range=(-8, 8, 1.0))
        plane.become(NumberPlane(x_range=(-10, 10, 1), y_range=(-8, 8, 1.0)))
        plane.fade(0.5)
        plane.apply_depth_test()
        self.add(plate, plane)

        self.play(
            frame.animate.reorient(58, 73, 0, ORIGIN, 8.00),
            Write(plane, stroke_width=3, lag_ratio=0.01, time_span=(2, 6)),
            run_time=6
        )

        # Draw a line
        film_point = 2 * UP
        line = Line(film_point, obj_dot.get_center())
        line.set_stroke(TEAL, 3)

        self.play(
            ShowCreation(line),
            frame.animate.reorient(0, 0, 0),
            FadeIn(plate_top),
            run_time=3,
        )
        self.wait()

        # Where the object had been
        dash_circle = DashedVMobject(Arc(angle=(23 / 24) * TAU), num_dashes=12)
        dash_circle.set_stroke(YELLOW, 3)
        dash_circle.replace(obj_dot).set_width(0.2)
        had_been_words = Text("Where the object\nhad been", font_size=36)
        had_been_words.next_to(dash_circle, UP, buff=0, aligned_edge=LEFT)

        self.play(
            FadeOut(obj_dot),
            Write(dash_circle, stroke_width=3, run_time=1),
            Write(had_been_words, run_time=1),
        )
        self.wait()
        self.play(FadeOut(had_been_words))

        # Show angle
        theta = -line.get_angle()
        arc = Arc(PI - theta, theta, radius=1)
        arc.shift(obj_dot.get_center())
        h_line = Line(ORIGIN, obj_dot.get_center())
        h_line.set_stroke(WHITE, 2)
        theta_prime_sym = Tex(R"\theta'")
        theta_prime_sym.set_max_height(0.8 * arc.get_height())
        theta_prime_sym.next_to(arc.pfp(0.4), LEFT, SMALL_BUFF)

        self.play(
            TransformFromCopy(line, h_line),
            ShowCreation(arc),
            Write(theta_prime_sym),
        )
        self.wait()

        # Set up terms for the calculations for the spacing
        # TODO, consider adding many little lines for all the fringes
        self.remove(plate)
        v_line = Line(ORIGIN, film_point)

        d_lines = Line(LEFT, RIGHT).replicate(2).set_width(0.3)
        d_lines.set_stroke(WHITE, 2)
        d_lines.arrange(DOWN, buff=0.1)
        d_lines.move_to(film_point, DOWN)
        lil_brace = Brace(Line(ORIGIN, 0.25 * UP), LEFT)
        lil_brace.match_height(d_lines)
        lil_brace.next_to(d_lines, LEFT, buff=0.05)
        big_brace = Brace(Group(d_lines[1], Point(ORIGIN)), LEFT, buff=0)
        big_brace.match_width(lil_brace, about_edge=RIGHT, stretch=True)

        kw = dict(font_size=42)
        L_label = Tex("L", **kw).next_to(h_line, DOWN, 2 * SMALL_BUFF)
        x_label = Tex("x", **kw).next_to(big_brace, LEFT, SMALL_BUFF)
        d_label = Tex("d", **kw).next_to(lil_brace, LEFT, SMALL_BUFF, aligned_edge=DOWN)
        L_label.set_color(BLUE)
        x_label.set_color(RED)
        VGroup(L_label, x_label, d_label).set_backstroke(BLACK, 5)

        terms = VGroup(
            d_lines, lil_brace, big_brace,
            L_label, x_label, d_label
        )

        # Limit to reference beam at just one point
        equations_tex = [
            R"\lambda = \sqrt{L^2 + (x + d)^2} - \sqrt{L^2 + x^2}",
            R"= \sqrt{L^2 + x^2 + 2xd + d^2} - \sqrt{L^2 + x^2}",
            R"\approx \sqrt{L^2 + x^2 + 2xd} - \sqrt{L^2 + x^2}",
            R"\approx \frac{1}{2\sqrt{L^2 + x^2}} 2xd",
            R"= d \cdot \frac{x}{\sqrt{L^2 + x^2}}",
            R"= d \cdot \sin(\theta')",
        ]
        equations = VGroup(
            Tex(eq, t2c={R"\lambda": YELLOW, "L": BLUE, "x": RED}, font_size=36)
            for eq in equations_tex
        )
        equations.arrange(DOWN, buff=0.65, aligned_edge=LEFT)
        equations.move_to(9.5 * LEFT + 5.65 * UP, UL)
        equations.set_backstroke(BLACK, 10)

        annotations = VGroup(
            Text("The distances between adjacent fringes and\nthe object should differ by one wavelength"),
            TexText(R"$d^2$ is small compared to $xd$"),
            TexText(R"Linear approximation:\\ \quad \\$\sqrt{X + \epsilon} \approx \sqrt{X} + \frac{1}{2\sqrt{X}} \epsilon$"),
        )
        annotations.scale(0.75)
        for annotation, i in zip(annotations, [0, 1, 3]):
            eq = equations[i]
            annotation.next_to(eq, RIGHT, buff=1.5)
            if i == 2:
                annotation.next_to(eq, DR)
            arrow = Arrow(annotation.get_left(), eq.get_right())
            annotation.add(arrow)
            annotation.set_color(GREY_A)
        annotations[2][:-1].align_to(annotations[2][-1], UP)

        braces = VGroup(
            Brace(equations[0][R"\sqrt{L^2 + (x + d)^2}"], UP, SMALL_BUFF),
            Brace(equations[0][R"\sqrt{L^2 + x^2}"], UP, SMALL_BUFF),
        )
        brace_texts = VGroup(
            TexText(R"Dist. to fringe\\at height $(x + d)$", font_size=24).next_to(braces[0], UP, SMALL_BUFF),
            TexText(R"Dist. to fringe\\at height $x$", font_size=24).next_to(braces[1], UP, SMALL_BUFF),
        )

        self.play(
            FadeIn(terms, lag_ratio=0.1, time_span=(0, 2)),
            Write(equations, time_span=(2, 5)),
            frame.animate.reorient(0, 0, 0, (-2, 2.5, 0.0), 9).set_anim_args(run_time=3),
        )
        self.wait()
        self.play(LaggedStart(
            FadeIn(annotations[0]),
            FadeIn(braces),
            FadeIn(brace_texts),
        ))
        self.wait()
        self.play(FadeIn(annotations[1]))
        self.play(FadeIn(annotations[2]))
        self.wait()

        # Reduce down to the key conclusion
        key_equation = Tex(R"d \cdot \sin(\theta') = \lambda", **kw)
        key_equation.next_to(line, UP, MED_LARGE_BUFF)
        key_equation.scale(1.25)
        key_equation.shift(RIGHT + 0.5 * UP)

        box = SurroundingRectangle(key_equation, buff=MED_SMALL_BUFF)
        box.set_fill(BLACK, 1)
        box.set_stroke(YELLOW, 1)

        terms.remove(d_label, lil_brace, d_lines)

        self.add(d_label, lil_brace, d_lines)
        self.play(
            ReplacementTransform(equations[-1][0], key_equation[9], time_span=(0, 2)),
            ReplacementTransform(equations[-1][1:], key_equation[:9], time_span=(0, 2)),
            ReplacementTransform(equations[0][0], key_equation[10], time_span=(0, 2)),
            FadeOut(equations[0][1:], time_span=(1.0, 1.5)),
            FadeOut(equations[1:-1], lag_ratio=0.01, time_span=(1.0, 2.5)),
            FadeOut(annotations, lag_ratio=0.01),
            FadeOut(terms, lag_ratio=0.1, time_span=(1.0, 3.0)),
            FadeOut(h_line),
            FadeOut(braces),
            FadeOut(brace_texts),
            frame.animate.reorient(0, 0, 0, (0, 1, 0), 6).set_anim_args(time_span=(1, 3.5)),
        )
        self.add(box, key_equation)
        self.play(
            Write(box),
            FlashAround(key_equation, buff=MED_SMALL_BUFF, time_width=1.5, run_time=2),
        )
        self.wait()

        # Smaller slit width
        lil_brace.generate_target()
        lil_brace.target.flip().next_to(d_lines, RIGHT, buff=0.025)

        arrow = Vector(0.3 * DL, thickness=2)
        arrow.next_to(lil_brace.target, UR, buff=0)

        new_plate_top = plate_top.copy()
        new_plate_top.set_wave_number(50)
        new_plate_top.save_state()
        new_plate_top.stretch(0, 0)

        self.play(
            d_label.animate.next_to(arrow.get_start(), UR, 0.5 * SMALL_BUFF),
            GrowArrow(arrow),
            MoveToTarget(lil_brace)
        )
        self.play(
            d_lines.animate.stretch(0.25, 1, about_edge=DOWN),
            lil_brace.animate.scale(0.25, about_edge=DL).set_stroke(WHITE, 1),
            arrow.animate.put_start_and_end_on(arrow.get_start(), arrow.get_end() + 0.05 * LEFT + 0.05 * DOWN),
            plate_top.animate.stretch(0, 0),
            Restore(new_plate_top),
            run_time=2
        )
        self.wait()
        self.remove(new_plate_top)
        plate_top.become(new_plate_top)

        # Shine reference beam in
        ref_wave = self.get_beam()
        ref_wave.move_to(film_point, LEFT)

        out_beams = self.get_triple_beam(film_point, obj_dot.get_center())

        self.play(GrowFromPoint(ref_wave, film_point + 8 * RIGHT, run_time=2, rate_func=linear))
        self.play(*(
            GrowFromPoint(beam[1], film_point, run_time=2, rate_func=linear)
            for beam in out_beams
        ))
        self.wait(4)

        # Note the matching angle
        upper_arc = arc.copy()
        upper_arc.shift(film_point - obj_dot.get_center())
        theta_sym = Tex(R"\theta", font_size=42)
        theta_sym.next_to(upper_arc.pfp(0.4), LEFT, SMALL_BUFF)

        self.play(
            ShowCreation(upper_arc),
            Write(theta_sym),
        )
        self.wait(4)

        # Write the diffraction equation
        key_equation.set_backstroke(BLACK, 8)
        key_equation.generate_target()
        box.generate_target()
        diff_eq = Tex(R"d \cdot \sin(\theta) = \lambda")
        key_equation.target.match_height(diff_eq)
        key_equation.target.next_to([6.5, 5.5, 0], DL, SMALL_BUFF)
        diff_eq.next_to(key_equation.target, DOWN, MED_LARGE_BUFF)

        box.target.surround(VGroup(key_equation.target, diff_eq))
        box.target.set_opacity(0)

        diff_eq_label = VGroup(
            Text("Diffraction\nequation", font_size=36),
            Vector(RIGHT),
        )
        diff_eq_label.arrange(RIGHT)
        diff_eq_label.next_to(diff_eq, LEFT)

        VGroup(diff_eq, diff_eq_label).set_backstroke(BLACK, 8)

        theta_sym_copy = theta_sym.copy()
        theta_sym_copy.set_backstroke()

        self.play(
            frame.animate.reorient(0, 0, 0, (0.0, 2, 0.0), 8.00),
            MoveToTarget(box),
            MoveToTarget(key_equation),
            Transform(theta_sym_copy, diff_eq[R"\theta"][0]),
            run_time=2
        )
        self.play(
            Write(diff_eq),
            FadeIn(diff_eq_label[0], lag_ratio=0.1),
            GrowArrow(diff_eq_label[1]),
        )
        self.remove(theta_sym_copy)
        self.wait(2)

        # Write implication
        implication = VGroup(Tex(R"\Downarrow"), Tex(R"\theta = \theta'"))
        implication.arrange(DOWN)
        implication.next_to(diff_eq, DOWN)
        implication.set_backstroke(width=5)

        self.play(Write(implication))
        self.wait()
        self.play(
            Transform(theta_sym.copy(), theta_prime_sym, remover=True),
            Transform(upper_arc.copy(), arc, remover=True),
            run_time=2
        )
        self.wait(4)

        # Move film point around
        film_dot = Point(film_point)

        line.f_always.put_start_and_end_on(film_dot.get_center, obj_dot.get_center)

        ref_wave.always.match_y(film_dot)

        def update_out_beams(beams):
            beams.become(self.get_triple_beam(
                film_dot.get_center(),
                obj_dot.get_center(),
            ))
            for beam in beams:
                beam[1].set_uniform(time=self.time)

        out_beams.clear_updaters()
        out_beams.add_updater(update_out_beams)

        self.add(out_beams)
        self.play(film_dot.animate.move_to(film_point))

        arc.add_updater(lambda m: m.become(
            Arc(PI, line.get_angle()).shift(obj_dot.get_center())
        ))
        upper_arc.add_updater(lambda m: m.match_points(arc).shift(
            film_dot.get_center() - obj_dot.get_center()
        ))
        theta_prime_sym.add_updater(
            lambda m: m.set_height(min(0.8 * arc.get_height(), 0.35)).next_to(arc.pfp(0.6), LEFT, SMALL_BUFF)
        )
        theta_sym.add_updater(lambda m: m.replace(theta_prime_sym[0]).shift(
            film_dot.get_center() - obj_dot.get_center()
        ))

        d_group = VGroup(d_label, arrow, d_lines, lil_brace)

        self.play(
            FadeOut(d_group, time_span=(0, 1)),
            film_dot.animate.set_y(1),
            run_time=3
        )
        self.play(film_dot.animate.set_y(3.5), run_time=5)
        self.play(film_dot.animate.set_y(0.5), run_time=6)
        self.play(film_dot.animate.set_y(3.5), run_time=6)

        # Show zone plate and observer
        equaiton_group = VGroup(box, key_equation, diff_eq, diff_eq_label, implication)

        randy = Randolph(height=2)
        randy.move_to(4 * LEFT, DOWN)

        plate.set_opacity(0.5)
        plate.set_wave_number(plate_top.uniforms["wave_number"])

        self.add(plate, plane)
        self.play(
            FadeOut(equaiton_group, lag_ratio=0.1, time_span=(0, 2)),
            film_dot.animate.set_y(1.0),
            FadeOut(plate_top, time_span=(0, 1)),
            FadeIn(randy, time_span=(1, 3)),
            frame.animate.reorient(-33, 43, 0, (-2.43, 0.5, -0.12), 9.60),
            run_time=5
        )
        self.play(randy.change("pondering", obj_dot))
        self.play(Blink(randy))
        self.wait(3)

        # Show full reference wave
        big_ref_wave = self.get_3d_ref_wave(plate)

        self.add(big_ref_wave, plate)
        self.play(
            FadeIn(big_ref_wave),
            FadeOut(ref_wave),
            frame.animate.reorient(-40, 67, 0, (-2.43, 0.5, -0.12), 9.60).set_anim_args(run_time=3)
        )
        self.wait(2)

        # Show many beams off the plate
        mid_line_points = DotCloud().to_grid(25, 1)
        mid_line_points.replace(plate, dim_to_match=1)
        mid_line_points.rotate(PI)
        plate_points = DotCloud().to_grid(15, 11)
        dense_plate_points = DotCloud().to_grid(60, 40)
        for dot_cloud in [plate_points, dense_plate_points]:
            dot_cloud.rotate(PI / 2, UP)
            dot_cloud.replace(plate, stretch=True)

        mid_lines_out = self.get_radiating_lines(mid_line_points, obj_dot)
        lines_out = self.get_radiating_lines(plate_points, obj_dot)
        dense_lines_out = self.get_radiating_lines(dense_plate_points, obj_dot)
        ghost_lines = self.get_ghost_lines(mid_line_points, obj_dot)
        dense_ghost_lines = self.get_ghost_lines(dense_plate_points, obj_dot)

        out_beams.clear_updaters()
        self.play(
            FadeOut(out_beams),
            FadeOut(VGroup(theta_sym, theta_prime_sym, upper_arc, arc, line)),
            ShowCreation(lines_out, lag_ratio=0.01, run_time=4),
            frame.animate.reorient(-93, 62, 0, (-2.43, 0.5, -0.12), 9.60).set_anim_args(run_time=5)
        )
        self.play(
            FadeOut(lines_out, time_span=(1, 2)),
            FadeOut(big_ref_wave),
            FadeIn(mid_lines_out, time_span=(1, 2)),
            frame.animate.to_default_state(),
            run_time=3,
        )
        self.play(LaggedStartMap(ShowCreation, ghost_lines, lag_ratio=0.01))
        self.wait()
        self.play(Blink(randy))
        self.wait()

        # Move character around
        def get_view_point():
            eye_point = randy.eyes[1].get_center()
            obj_point = obj_dot.get_center()
            vect = obj_point - eye_point
            alpha = 1.0 - (obj_point[0] / vect[0])
            return eye_point + alpha * vect

        def update_lines(lines):
            view_point = get_view_point()
            min_dist = 2.5 * get_norm(lines[0].get_start() - lines[1].get_start())
            for line in lines:
                dist = get_norm(line.get_start() - view_point)
                alpha = clip(inverse_interpolate(min_dist, 0, dist), 0, 1)
                line.set_stroke(opacity=interpolate(0, 1, alpha))

        screen_dot = GlowDot(radius=0.5)
        screen_dot.f_always.move_to(get_view_point)

        mid_lines_out.add_updater(update_lines)
        ghost_lines.add_updater(update_lines)

        randy.always.look_at(obj_dot)

        self.play(FadeIn(screen_dot))
        self.add(mid_lines_out, ghost_lines)
        for y in [-2.8, 2.2]:
            self.play(randy.animate.set_y(y), run_time=4)

        # Movement in 3d
        dense_lines_out.clear_updaters()
        dense_ghost_lines.clear_updaters()
        dense_lines_out.add_updater(update_lines)
        dense_ghost_lines.add_updater(update_lines)

        glass = Rectangle()
        glass.rotate(PI / 2, UP)
        glass.replace(plate, stretch=True)
        glass.set_stroke(WHITE, 1)
        glass.set_fill(BLACK, 0.25)

        self.remove(plate)
        self.add(glass, randy)
        self.play(
            FadeIn(glass, time_span=(0, 1)),
            FadeOut(mid_lines_out, time_span=(1, 2)),
            FadeOut(ghost_lines, time_span=(1, 2)),
            FadeIn(dense_lines_out, time_span=(1, 2)),
            FadeIn(dense_ghost_lines, time_span=(1, 2)),
            randy.animate.rotate(PI / 2, RIGHT).shift(0.2 * (IN + DOWN)),
            frame.animate.reorient(-48, 71, 0, (0.53, -0.56, 0.06), 10.86),
            run_time=3
        )

        frame.add_ambient_rotation(1 * DEGREES)
        for (y, z) in [(-3, 2), (-2, -1.5), (-1, 1), (2, 2), (1.1, 1.1)]:
            self.play(randy.animate.set_y(y).set_z(z), run_time=3)

        # Reintroduce the beams
        frame.clear_updaters()
        dense_lines_out.clear_updaters()
        dense_ghost_lines.clear_updaters()
        self.play(
            FadeOut(dense_lines_out, time_span=(0, 1)),
            FadeOut(dense_ghost_lines, time_span=(0, 1)),
            FadeOut(screen_dot, time_span=(0, 1)),
            FadeOut(glass, time_span=(2, 3)),
            FadeIn(plate_top, time_span=(2.0, 3)),
            randy.animate.rotate(PI / 2, LEFT).move_to(4 * LEFT, DOWN),
            frame.animate.reorient(0, 0, 0, ORIGIN, FRAME_HEIGHT),
            run_time=3
        )
        self.play(GrowFromPoint(ref_wave, ref_wave.get_right(), rate_func=linear))
        out_beams.clear_updaters()
        self.play(GrowFromPoint(out_beams, film_dot.get_center(), rate_func=linear))
        out_beams.add_updater(update_out_beams)
        self.wait(3)

        # Move film point
        self.play(
            film_dot.animate.match_y(randy.eyes),
            run_time=2
        )
        self.wait(6)
        self.play(
            randy.animate.move_to(2.4 * LEFT),
            run_time=2
        )

        # Highlight other first order beam
        self.remove(out_beams)
        out_beams = self.get_triple_beam(film_dot.get_center(), obj_dot.get_center())
        self.add(out_beams)
        self.play(
            out_beams[0][1].animate.set_opacity(0.25),
            out_beams[1][1].animate.set_opacity(0.25),
        )
        randy.clear_updaters()
        self.play(randy.change("confused", film_point))
        self.play(Blink(randy))
        self.wait(4)
        self.play(FadeOut(randy))

        # Add all other first order beams
        out_beams.add_updater(update_out_beams)
        out_beams.add_updater(lambda m: m[0][1].set_opacity(0.25))
        out_beams.add_updater(lambda m: m[1][1].set_opacity(0.25))

        conj_lines = VGroup(
            Line(point, obj_dot.get_center())
            for point in mid_line_points.get_points()
        )
        conj_lines.flip(UP, about_point=ORIGIN)
        conj_lines.set_stroke(YELLOW, 1)
        conj_lines.sort(lambda p: -p[1])

        self.add(out_beams)
        self.play(film_dot.animate.set_y(4), run_time=4)
        self.play(
            film_dot.animate.set_y(-4),
            FadeIn(conj_lines, lag_ratio=0.25, run_time=4),
            run_time=5,
        )
        self.play(film_dot.animate.set_y(3.5), run_time=8)
        self.play(film_dot.animate.set_y(2), run_time=8)
        self.wait()
        self.play(FadeOut(conj_lines))

        # Show higher order beams
        theta = -angle_of_vector(obj_dot.get_center() - film_dot.get_center())
        wave_number = 250
        wavelength = 1.0 / wave_number
        spacing = wavelength / math.sin(theta)
        n_sources = 32
        sources = DotCloud().to_grid(n_sources, 1)
        sources.set_height(spacing * (n_sources - 1))
        sources.move_to(film_dot)
        out_wave = LightWaveSlice(sources)
        out_wave.set_color(BLUE_A)
        out_wave.set_shape(20, 20)
        out_wave.move_to(ORIGIN, RIGHT)
        out_wave.set_wave_number(wave_number)
        out_wave.set_frequency(1.0)
        out_wave.set_decay_factor(0)
        out_wave.set_max_amp(10)

        self.play(
            FadeOut(out_beams),
            GrowFromPoint(out_wave, film_dot.get_center()),
            frame.animate.reorient(0, 0, 0, (-0.1, 1.85, 0.0), 11.08).set_anim_args(run_time=4),
        )
        self.wait(4)

    def get_radiating_lines(self, point_cloud, obj_dot, length=20, stroke_color=YELLOW, stroke_width=1):
        lines = VGroup()
        for point in point_cloud.get_points():
            line = Line(obj_dot.get_center(), point)
            line.set_length(length)
            line.shift(point - line.get_start())
            line.set_stroke(stroke_color, stroke_width)
            lines.add(line)
        return lines

    def get_ghost_lines(self, point_cloud, obj_dot, dash_length=0.15, stroke_color=WHITE, stroke_width=1):
        lines = VGroup(
            DashedLine(point, obj_dot.get_center(), dash_length=dash_length)
            for point in point_cloud.get_points()
        )
        lines.set_stroke(stroke_color, stroke_width)
        return lines

    def get_3d_ref_wave(self, plate, n_planes=50, spacing=1.0, speed=1.0, opacity=0.25):
        planes = Square3D().replicate(n_planes)
        planes.rotate(PI / 2, UP)
        planes.replace(plate, stretch=True)
        planes.arrange(RIGHT, buff=spacing)
        planes.move_to(RIGHT, LEFT)
        for n, plane in enumerate(planes):
            plane.set_color([BLUE, RED][n % 2])
            plane.set_opacity(opacity)

        def update_planes(planes, dt):
            for plane in planes:
                plane.shift(dt * LEFT * speed)
                x = plane.get_x()
                if x < 1:
                    plane.set_opacity(opacity * x)
                if x < 0.1:
                    plane.next_to(planes, RIGHT, buff=spacing)
                    plane.set_opacity(opacity)
            planes.sort(lambda p: -p[0])
            return planes

        planes.add_updater(update_planes)

        return planes

    def get_triple_beam(self, film_point, obj_point, **kwargs):
        theta = PI - angle_of_vector(film_point - obj_point)
        beams = Group(
            self.get_beam(angle=angle, **kwargs)
            for angle in [-theta, 0, theta]
        )
        beams.shift(film_point)
        beams.deactivate_depth_test()
        return beams

    def get_beam(self, height=0.1, width=15, n_sources=8, source_height=0.15, wave_number=20, frequency=2.3, color=BLUE_A, opacity=0.75, angle=0):
        mini_sources = DotCloud().to_grid(n_sources, 1)
        mini_sources.set_height(source_height)
        mini_sources.set_radius(0).set_opacity(0)
        mini_sources.move_to(0.75 * RIGHT)
        wave = LightWaveSlice(
            mini_sources,
            wave_number=wave_number,
            frequency=frequency,
            color=color,
            opacity=opacity,
            decay_factor=0.25,
            max_amp=0.4 * n_sources,
        )
        wave.set_shape(width, height)
        wave.move_to(ORIGIN, RIGHT)
        beam = Group(mini_sources, wave)
        beam.rotate(angle, about_point=ORIGIN)
        return beam
