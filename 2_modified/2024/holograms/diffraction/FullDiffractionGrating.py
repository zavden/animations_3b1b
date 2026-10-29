# ==============================================================================
# Scene:      FullDiffractionGrating
# Source:     videos/_2024/holograms/diffraction.py (lines 2107-2826)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FullDiffractionGrating.py FullDiffractionGrating -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `self.checkpoint`/`self.revert_to_checkpoint` no longer exist in Scene: `self.get_state()` is saved and restored with `restore_state` (without rewinding time/num_plays)
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


class FullDiffractionGrating(DiffractionGratingScene):
    def construct(self):
        # Set up the grating
        full_width = 100
        wave_number = 2 + 0.1 * PI  # Make it irrational
        frequency = 1
        slit_dist = 1.0

        frame = self.frame
        frame.reorient(-28, 76, 0, (0, 3.29, -0.61), 8.17)

        wall = self.get_wall_with_slits(32, spacing=slit_dist, depth=2.0, total_width=full_width)
        wall.move_to(0.5 * IN, IN)

        in_wave = self.get_plane_wave()
        in_wave.set_wave_number(wave_number)
        in_wave.set_frequency(frequency)
        in_wave.set_shape(full_width, full_width)
        in_wave.set_opacity(0.85)
        in_wave.move_to(ORIGIN, UP)

        sources = self.get_point_sources_from_wall(wall)
        out_wave = LightWaveSlice(sources, wave_number=wave_number, frequency=frequency)
        out_wave.set_shape(full_width, full_width)
        out_wave.set_opacity(0.25)
        out_wave.set_max_amp(2)
        out_wave.move_to(ORIGIN, DOWN)

        self.add(wall)
        self.add(in_wave)
        self.add(out_wave)

        # Label the distance apart
        piece = wall[16]
        brace = Brace(piece, UP)
        brace.rotate(PI / 2, RIGHT)
        brace.next_to(piece, OUT, SMALL_BUFF)
        dist_label = Tex(R"d", font_size=60)
        dist_label.rotate(PI / 2, RIGHT)
        dist_label.next_to(brace, OUT, SMALL_BUFF)
        VGroup(brace, dist_label).set_backstroke(BLACK, 5)

        self.play(
            GrowFromCenter(brace),
            FadeIn(dist_label, 0.25 * OUT),
            frame.animate.reorient(11, 72, 0, (-1.12, 5.34, -0.64), 11.13).set_anim_args(run_time=8),
        )
        dist_label.add(brace)

        # Show model as an array of point sources
        sources.set_radius(0.5)
        wall.save_state()
        wall.target = wall.generate_target()
        wall.target.stretch(0.05, dim=2, about_point=ORIGIN)
        wall.target.stretch(0.5, dim=1, about_point=ORIGIN)

        dist_label.set_z_index(1)
        self.play(
            frame.animate.reorient(0, 12, 0, (0, 4.45, -0.62), 11.20),
            dist_label.animate.rotate(PI / 2, LEFT).next_to(piece, UP, SMALL_BUFF),
            MoveToTarget(wall, time_span=(3, 5)),
            FadeIn(sources, time_span=(1, 3)),
            out_wave.animate.set_opacity(1).set_anim_args(suspend_mobject_updating=False),
            in_wave.animate.set_opacity(0.25).set_anim_args(suspend_mobject_updating=False),
            run_time=8,
        )
        self.wait(4)

        # Show the N graphs
        point_tracker = GlowDot(color=YELLOW, radius=1)
        point_tracker.move_to(8 * UP)

        def update_lines(lines):
            for line, source_point in zip(lines, sources.get_points()):
                line.put_start_and_end_on(source_point, point_tracker.get_center())

        lines = Line().replicate(sources.get_num_points())
        lines.set_stroke(YELLOW, 2)
        lines.add_updater(update_lines)

        individual_sources = Group(
            sources.copy().set_points(sources.get_points()[i:i + 1])
            for i in range(sources.get_num_points())
        )

        waves = Group(
            out_wave.copy().set_sources(src).set_opacity(0)
            for src in individual_sources
        )
        waves.scale(0)

        graphs = VGroup(
            self.get_graph_over_wave(line, wave, scale_factor=0.25)
            for line, wave in zip(lines, waves)
        )

        self.play(
            out_wave.animate.set_opacity(0.2).set_anim_args(suspend_mobject_updating=False),
            FadeOut(dist_label),
            FadeIn(point_tracker),
        )
        self.wait()
        self.add(lines, graphs, out_wave)
        self.add(waves)
        self.play(
            ShowCreation(lines, lag_ratio=0.01, time_span=(0, 2)),
            ShowCreation(graphs, lag_ratio=0.01, suspend_mobject_updating=False, time_span=(0, 2)),
            frame.animate.reorient(1, 57, 0, (-0.17, 5.75, 0.32), 14.54),
            run_time=5
        )
        self.wait(3)
        self.play(
            FadeOut(lines),
            FadeOut(graphs),
            FadeOut(point_tracker),
            out_wave.animate.set_opacity(0.85).set_anim_args(suspend_mobject_updating=False),
            frame.animate.reorient(0, 42, 0, (0, 5.4, 0.45), 13.00),
            run_time=3,
        )
        self.remove(waves)

        # Zoom out to large
        out_wave.set_width(500, about_edge=DOWN)
        self.play(
            frame.animate.reorient(0, 0, 0, (0, 95, 0), 200),
            out_wave.animate.set_max_amp(1).set_anim_args(suspend_mobject_updating=False),
            run_time=20
        )

        # Let it run for a few cycles, we'll use this as an underlay for parts that follow
        self.wait(4)

        # Highlight the higher order beams
        in_wave.scale(0)
        out_wave.scale(0)

        beam_point = GlowDot(color=WHITE, radius=3)
        beam_point.move_to(1000 * UP)
        beam_outlines = Line().replicate(2)
        center_beam_line = Line()
        VGroup(beam_outlines, center_beam_line).set_stroke(WHITE, 50)
        beam_outlines[0].f_always.put_start_and_end_on(sources.get_left, beam_point.get_center)
        beam_outlines[1].f_always.put_start_and_end_on(sources.get_right, beam_point.get_center)
        center_beam_line.f_always.put_start_and_end_on(sources.get_center, beam_point.get_center)

        theta = math.asin(1.0 / wave_number / slit_dist)  # Diffraction equation!

        self.play(ShowCreation(beam_outlines, lag_ratio=0))
        self.wait(3)
        self.play(
            Rotate(beam_point, -theta, about_point=ORIGIN),
            run_time=1
        )
        self.wait()
        self.play(
            Rotate(beam_point, 2 * theta, about_point=ORIGIN),
            run_time=1
        )
        self.wait(8)

        # Ask about the angle
        v_line = Line(ORIGIN, get_norm(beam_point.get_center()) * UP)
        d_line = Line(ORIGIN, beam_point.get_center())
        VGroup(v_line, d_line).set_stroke(WHITE, 50)

        arc = og_big_arc = Arc(PI / 2 + theta, -theta, radius=30)
        arc.set_stroke(WHITE, 50)
        theta_sym = Tex(R"\theta")
        theta_sym.set_width(arc.get_width() / 2)
        theta_sym.next_to(arc, UP, buff=2).shift(LEFT)

        self.remove(beam_outlines)
        self.play(
            TransformFromCopy(beam_outlines[0], d_line),
            TransformFromCopy(beam_outlines[1], d_line),
        )
        self.play(
            TransformFromCopy(d_line, v_line),
            ShowCreation(arc),
            Write(theta_sym),
        )
        self.wait(3)

        # Analyze central beam
        beam_point.rotate(-theta, about_point=ORIGIN)
        point_tracker.move_to(180 * UP)
        point_tracker.set_radius(8)

        L_line = Line(ORIGIN, point_tracker.get_center())
        x_line = Line(sources.get_center(), sources.get_left())
        hyp = Line(sources.get_left(), point_tracker.get_center())
        VGroup(L_line, hyp).set_stroke(YELLOW, width=50)
        x_line.set_stroke(WHITE, 50)

        L_label = Tex("L", font_size=800)
        x_label = Tex("x", font_size=800)
        hyp_label = Tex(R"\sqrt{L^2 + x^2}", font_size=800)

        L_label.next_to(L_line.pfp(0.4), RIGHT, buff=2)
        L_label.match_color(L_line)
        x_label.next_to(x_line, UP, buff=3)
        hyp_label.next_to(hyp.pfp(0.4), LEFT, buff=2)
        hyp_label.match_color(hyp)

        self.play(
            FadeIn(beam_outlines),
            FadeOut(d_line),
            FadeOut(v_line),
            FadeOut(arc),
            FadeOut(theta_sym),
        )
        self.wait(2)
        self.play(
            FadeIn(point_tracker),
            out_wave.animate.set_opacity(0.5).set_anim_args(suspend_mobject_updating=False)
        )
        self.play(
            ShowCreation(L_line),
            VFadeIn(L_label),
            FadeOut(beam_outlines),
        )
        self.wait()
        self.play(
            TransformFromCopy(L_line, hyp),
            ShowCreation(x_line),
            TransformMatchingStrings(L_label.copy(), hyp_label),
            FadeIn(x_label, shift=3 * LEFT),
        )

        # Show the approximation (In another scene)
        self.wait(4)

        # Show all the different lines
        self.play(FadeOut(VGroup(L_label, x_label, hyp_label, x_line, L_line, hyp)))
        lines.set_stroke(YELLOW, 30)
        lines.update()

        self.play(LaggedStartMap(ShowCreationThenFadeOut, lines, lag_ratio=0.25, run_time=8))

        # Analyze a point off the center
        new_angle = theta
        lines.set_stroke(width=10)
        arc = Arc(PI / 2 - new_angle, new_angle, radius=30)
        arc.set_stroke(WHITE, 50)
        theta_sym = Tex(R"\theta")
        theta_sym.set_width(0.45 * arc.get_width())
        theta_sym.next_to(arc.get_center(), UP, buff=2).shift(RIGHT)
        d_line = v_line.copy().rotate(-new_angle, about_edge=DOWN)
        question = Text("What about\nover here?")
        question.set_height(15)
        question.rotate(frame.get_phi(), RIGHT)
        question.always.next_to(point_tracker, DR, buff=-2)

        self.play(
            Rotate(point_tracker, -new_angle, about_point=ORIGIN),
            VFadeIn(question),
            run_time=3
        )
        self.play(ShowCreation(d_line))
        self.play(
            TransformFromCopy(d_line, v_line),
            ShowCreation(arc),
            Write(theta_sym)
        )
        self.wait(2)
        self.play(
            ShowCreation(lines, lag_ratio=0.01, run_time=2, suspend_mobject_updating=True),
            FadeOut(VGroup(v_line, d_line, arc, theta_sym))
        )
        self.wait(4)
        self.play(
            point_tracker.animate.move_to(1.15 * point_tracker.get_center()),
            run_time=2
        )

        # Zoom in near the slits again
        self.play(
            frame.animate.reorient(0, 0, 0, (0.0, 2.75, 0.0), 8),
            lines.animate.set_stroke(width=5),
            out_wave.animate.set_opacity(0.1).set_anim_args(suspend_mobject_updating=False),
            in_wave.animate.set_opacity(0.1).set_anim_args(suspend_mobject_updating=False),
            sources.animate.set_radius(0.35),
            run_time=6,
        )
        self.wait(4)

        # Show individual lines
        lines.suspend_updating()
        line1 = lines[15].copy()
        line2 = lines[16].copy()
        line2.set_stroke(WHITE)
        for line in [line1, line2]:
            line.set_length(8, about_point=line.get_start())
            line.set_stroke(opacity=1)
            line.save_state()

        lines.target = lines.generate_target()
        lines.target.set_stroke(width=1, opacity=0.5)

        long_label = Text("Is this longer...")
        short_label = Text("...than this?")
        long_label.match_color(line1)
        long_label.next_to(line1.get_center(), LEFT)
        short_label.next_to(line2.get_center(), RIGHT)

        self.play(
            MoveToTarget(lines),
            ShowCreation(line1, time_span=(0.5, 1.5)),
            FadeIn(long_label, time_span=(0.5, 1.5))
        )
        self.wait()
        self.play(
            ShowCreation(line2),
            TransformMatchingStrings(long_label.copy(), short_label),
        )
        self.wait()

        # Zoom out and pivot
        for line in [line1, line2]:
            line.put_start_and_end_on(line.get_start(), point_tracker.get_center())

        tail = TracingTail(line.get_start, time_traced=3.0, stroke_width=(0, 10))
        point_label = TexText(R"Point we're\\analyzing")
        point_label.set_height(1.5 * question.get_height())
        point_label.move_to(question, UL)
        self.remove(question)
        self.add(point_label)

        self.play(
            frame.animate.reorient(0, 0, 0, (14.74, 92.42, 0.0), 209.77),
            line2.animate.set_stroke(width=50),
            run_time=3
        )
        self.add(tail)
        self.wait(2)
        self.play(
            Rotate(
                line2, -30 * DEGREES,
                about_point=point_tracker.get_center(),
                rate_func=lambda t: wiggle(t, 2),
                run_time=8,
            )
        )
        self.wait(2)
        self.play(
            frame.animate.reorient(0, 0, 0, (0, 1.5, 0.0), 6.0),
            line2.animate.set_stroke(width=5),
            VFadeOut(tail),
            FadeOut(point_label),
            FadeOut(in_wave, suspend_mobject_updating=False),
            FadeOut(out_wave, suspend_mobject_updating=False),
            run_time=3,
        )

        # Rotate again, as a perp
        tail.add_updater(lambda m: m.set_stroke(width=(0, 5)))
        self.add(tail)
        self.play(
            Rotate(
                line2, -1 * DEGREES,
                about_point=point_tracker.get_center(),
                # rate_func=lambda t: wiggle(t, 2),
                rate_func=there_and_back,
                run_time=5,
            )
        )
        self.wait(3)
        self.remove(tail)

        # Drop perpendicular
        p1 = line1.get_start()
        p2 = line2.get_start()
        to_point = rotate_vector(UP, -theta)
        foot = p1 + math.sin(theta) * to_point

        diff_label_group = always_redraw(lambda: self.get_diff_label_group(
            p1=sources.get_points()[15],
            p2=sources.get_points()[16],
            theta=PI / 2 - line1.get_angle()
        ))
        diff_label_group.suspend_updating()
        triangle, elbow, altitude, arc, small_theta_sym, diff_segment, brace, d_label = diff_label_group

        self.play(
            ShowCreation(altitude),
            FadeOut(VGroup(long_label, short_label)),
            frame.animate.reorient(0, 0, 0, (0.5, 0.88, 0.0), 3.8),
            sources.animate.set_radius(0.2),
        )
        self.play(ShowCreation(elbow))
        self.wait()

        # Compare lengths
        for line in line1, line2:
            line.set_length(5, about_point=line.get_start())
        matched_segment = line2.copy().shift(altitude.get_vector())
        matched_segment.set_color(TEAL)
        label1 = TexText(R"Length of shorter line $\rightarrow$", font_size=24)
        label1.next_to(p2, UR, buff=SMALL_BUFF)
        label1.rotate(PI / 2 - theta, about_point=p2)
        label1.shift(0.1 * to_point)
        label2 = label1.copy()
        label2.match_color(matched_segment)
        label2.shift(matched_segment.get_start() - line2.get_start())

        diff_label = Text("Difference", font_size=24)
        diff_label.next_to(brace.get_center(), LEFT, buff=0.2).shift(0.15 * UP)
        diff_label.set_color(RED)
        diff_segment.set_stroke(RED, 5)

        self.play(
            Write(label1, stroke_width=1),
            ShowCreation(line2),
            run_time=1,
        )
        self.wait()
        self.play(
            TransformFromCopy(line2, matched_segment),
            line1.animate.set_stroke(width=1)
        )
        self.wait()
        self.play(LaggedStart(
            GrowFromCenter(brace),
            GrowFromCenter(diff_segment),
            Write(diff_label, stroke_width=1),
            lag_ratio=0.2
        ))
        self.wait()

        # Draw the appropriate right triangle
        d_sine_theta = Tex(R"d \cdot \sin(\theta)", font_size=24)
        d_sine_theta.move_to(diff_label, RIGHT)

        self.add(triangle, elbow, altitude, diff_segment)
        self.play(
            wall.animate.set_height(0.01, stretch=True),
            FadeIn(triangle),
            FadeOut(label1),
        )
        self.wait()
        self.play(FadeIn(d_label, 0.25 * DOWN))
        self.wait()
        self.play(
            TransformMatchingStrings(d_label.copy(), d_sine_theta, run_time=1),
            FadeOut(diff_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(d_sine_theta[R"\theta"][0], small_theta_sym),
            ShowCreation(arc),
        )
        self.wait()

        # Lock the leg to match wavelength
        self.remove(in_wave, out_wave)
        # CHANGE: Scene.checkpoint no longer exists in manimgl (it only remained in embed); the state is saved with get_state()
        checkpoint_state = self.get_state()

        lambda_label = Tex(R"= \lambda")
        lambda_label[1].set_color(TEAL)
        lambda_label.set_height(0.75 * d_sine_theta.get_height())
        lambda_label.add_updater(lambda m: m.next_to(brace.pfp(0.5), UL, buff=0.025))

        n_cycles = 8
        sine = FunctionGraph(lambda x: -math.sin(x), x_range=(0, n_cycles * TAU, 0.1))
        sine.set_stroke(TEAL, 1)
        sine.set_width(n_cycles * diff_segment.get_length())
        sine.add_updater(lambda m: m.put_start_and_end_on(
            diff_segment.get_start(), diff_segment.get_end()
        ).scale(n_cycles, about_point=diff_segment.get_start()))

        lock_arrow = Vector(0.5 * DOWN, thickness=2).next_to(brace, UP, buff=0.05)
        lock_label = Text("Consider this\nlocked", font_size=16)
        lock_label.next_to(lock_arrow, UP, SMALL_BUFF)

        self.play(
            d_sine_theta.animate.scale(0.75).next_to(lambda_label, LEFT, buff=0.05).shift(0.025 * DOWN),
            FadeIn(lambda_label, 0.25 * RIGHT),
            FadeOut(line2),
            FadeOut(matched_segment),
            diff_segment.animate.set_stroke(width=2),
            frame.animate.reorient(0, 0, 0, (0.14, 0.48, 0.0), 3.17).set_anim_args(run_time=2),
        )
        self.play(ShowCreation(sine, rate_func=linear))
        self.wait()
        self.play(
            FadeIn(lock_label),
            GrowArrow(lock_arrow)
        )
        self.wait()
        self.play(FadeOut(VGroup(lock_arrow, lock_label)))

        # Show the other sine waves
        shift_value = p2 - p1
        other_sines = VGroup(sine.copy().shift(x * shift_value) for x in range(-2, 4) if x != 0)
        other_sines.clear_updaters()

        self.play(ShowCreation(other_sines, lag_ratio=0.25, run_time=4))
        self.wait()
        self.play(FadeOut(other_sines, lag_ratio=0.25, run_time=2))

        # Change the distance between points
        self.add(diff_label_group)
        diff_label_group.resume_updating()

        lines.resume_updating()
        line1.clear_updaters()
        line1.add_updater(lambda m: m.match_points(lines[15]))
        line1.resume_updating()

        def get_dist_point(wavelength):
            dist_to_point = get_norm(point_tracker.get_center())
            d = get_norm(sources.get_points()[1] - sources.get_points()[0])
            angle = math.asin(wavelength / d)
            return rotate_vector(UP, -angle) * dist_to_point

        self.add(lines, line1, diff_label_group, sine)
        wall_center = sources.get_points()[15]
        scale_factors = [0.5, 2.0, 1.5, 1.0 / 1.5][:-1]
        for scale_factor in scale_factors:
            arrows = VGroup(Vector(0.3 * RIGHT, thickness=1), Vector(0.3 * LEFT, thickness=1))
            arrows.arrange(RIGHT if scale_factor < 1 else LEFT, buff=0.25)
            arrows.always.move_to(d_label)
            self.play(
                UpdateFromFunc(point_tracker, lambda m: m.move_to(get_dist_point(1.0 / wave_number))),
                MaintainPositionRelativeTo(d_sine_theta, lambda_label),
                sources.animate.scale(scale_factor, about_point=wall_center),
                wall.animate.scale(scale_factor, about_point=wall_center),
                FadeIn(arrows, scale=scale_factor, suspend_mobject_updating=False, time_span=(0, 2)),
                run_time=5,
            )
            self.play(FadeOut(arrows))

        # Show double
        if False:  # This was just a temporary insert, not to be run in general
            d_angle2, d_angle3 = [
                angle_of_vector(get_dist_point(n / wave_number)) - angle_of_vector(get_dist_point((n + 1) / wave_number))
                for n in (1, 2)
            ]
            sine.clear_updaters()
            new_rhs = Tex(Rf"= 1.00 \lambda", t2c={R"\lambda": TEAL})
            new_rhs.set_height(0.8 * lambda_label.get_height())
            factor = new_rhs.make_number_changeable("1.00")
            factor_tracker = ValueTracker(1.0)
            new_rhs.f_always.set_value(factor_tracker.get_value)
            new_rhs.always.move_to(lambda_label, RIGHT)

            self.play(
                d_sine_theta.animate.next_to(new_rhs, LEFT, buff=0.05).shift(0.02 * DOWN),
                lambda_label.animate.set_opacity(0),
                FadeIn(new_rhs)
            )
            self.play(
                Rotate(point_tracker, -d_angle2, about_point=ORIGIN),
                Rotate(sine, -d_angle2, about_point=sine.get_start()),
                factor_tracker.animate.set_value(2.0),
                MaintainPositionRelativeTo(d_sine_theta, lambda_label),
                run_time=5,
            )
            self.wait()
            self.play(
                Rotate(point_tracker, -d_angle2, about_point=ORIGIN),
                Rotate(sine, -d_angle2, about_point=sine.get_start()),
                factor_tracker.animate.set_value(3.0),
                MaintainPositionRelativeTo(d_sine_theta, lambda_label),
                run_time=5,
            )
            self.wait()

        # Show the angle match
        # CHANGE: Scene.revert_to_checkpoint no longer exists; the saved state is restored with
        # restore_state(), without rewinding time or num_plays so as not to disorder the video being written
        checkpoint_state.time = self.time
        checkpoint_state.num_plays = self.num_plays
        self.restore_state(checkpoint_state)

        p4 = p2 + 2 * (p2 - p1)
        h_line = Line(p2, p1).scale(3, about_edge=RIGHT)
        h_line.set_stroke(WHITE, 0)
        angle_group = VGroup(triangle, arc, small_theta_sym, h_line).copy()
        angle_group[0].set_opacity(0)
        angle_group.target = angle_group.generate_target()
        angle_group.target.rotate(-PI / 2)
        angle_group.target.move_to(p4, DL)
        angle_group.target[2].rotate(PI / 2).shift(0.01 * UR)
        angle_group.target[3].set_stroke(WHITE, 3)
        angle_group.target.scale(2, about_edge=DL)

        self.play(
            MoveToTarget(angle_group),
            run_time=2
        )
        self.wait()

        # Write conclusion
        conclusion = VGroup(
            Text("Difference in distance:", font_size=36),
            Tex(R"d \cdot \sin(\theta)")
        )
        conclusion.arrange(DOWN)
        conclusion_box = SurroundingRectangle(conclusion, buff=MED_SMALL_BUFF)
        conclusion_box.set_stroke(WHITE, 1)
        conclusion_box.set_fill(BLACK, 1)
        conclusion_group = VGroup(conclusion_box, conclusion)
        conclusion_group.to_corner(UL, buff=SMALL_BUFF)
        conclusion_group.fix_in_frame()
        conclusion_group.set_fill(border_width=0)

        self.play(
            FadeIn(conclusion_box),
            FadeIn(conclusion[0]),
            TransformFromCopy(d_sine_theta, conclusion[1])
        )
        self.wait()
        self.play(FadeOut(conclusion_group))

        # Zoom out
        out_wave.set_sources(sources.copy().set_points(sources.get_points()[10:-10]))
        out_wave.set_sources(sources)
        out_wave.set_width(800).move_to(ORIGIN, DOWN)
        out_wave.set_opacity(0)
        lines.resume_updating()

        self.add(out_wave)
        self.play(
            FadeOut(diff_label_group, lag_ratio=0.1, time_span=(0, 1.5)),
            FadeOut(VGroup(d_sine_theta, matched_segment, line1, line2, angle_group), lag_ratio=0.1, time_span=(0, 1.5)),
            out_wave.animate.set_opacity(0.85).set_anim_args(suspend_mobject_updating=False, time_span=(0, 2)),
            frame.animate.reorient(0, 0, 0, (0, 200, 0.0), 400),
            sources.animate.set_radius(0.75),
            lines.animate.set_stroke(width=20).set_anim_args(suspend_mobject_updating=False),
            point_tracker.animate.scale(2.0, about_point=ORIGIN).set_anim_args(time_span=(0, 8)),
            run_time=20,
            rate_func=lambda t: t**6,
        )
        self.wait()

        # Add back arc label
        arc = always_redraw(lambda: Arc(
            PI / 2, angle_of_vector(point_tracker.get_center()) - PI / 2,
            radius=50,
            stroke_color=WHITE,
            stroke_width=100
        ))
        theta_sym.set_height(16)
        theta_sym.add_updater(lambda m, arc=arc: m.next_to(arc.pfp(0.7), UP, buff=6))
        theta_sym.suspend_updating()
        VGroup(v_line, d_line).set_stroke(WHITE, 150)
        d_line.add_updater(lambda m, pt=point_tracker: m.put_start_and_end_on(ORIGIN, 5 * pt.get_center()))
        self.play(
            ShowCreation(v_line),
            ShowCreation(d_line),
            ShowCreation(arc),
            Write(theta_sym, stroke_width=20),
            run_time=1
        )
        theta_sym.resume_updating()
        self.wait(4)

        # Change the slit distance zoomed out
        for scale_factor in scale_factors:
            self.play(
                UpdateFromFunc(point_tracker, lambda m: m.move_to(get_dist_point(1.0 / wave_number))),
                sources.animate.scale(scale_factor, about_point=wall_center),
                wall.animate.scale(scale_factor, about_point=wall_center),
                run_time=5,
            )
            self.wait()

        # Double and triple the angle
        for n in [1, 2]:
            d_angle = angle_of_vector(get_dist_point(n / wave_number)) - angle_of_vector(get_dist_point((n + 1) / wave_number))
            self.play(
                Rotate(point_tracker, -d_angle, about_point=ORIGIN),
                frame.animate.set_height(450),
                run_time=5
            )
            self.wait()

    def get_diff_label_group(self, p1, p2, theta):
        # Altitude
        to_point = rotate_vector(UP, -theta)
        dist = get_norm(p2 - p1)
        foot = p1 + dist * math.sin(theta) * to_point

        altitude = DashedLine(p2, foot, dash_length=get_norm(foot - p2) / 39.5)
        elbow = Elbow(width=0.1 * dist, angle=-theta - PI / 2).shift(foot)

        altitude.set_stroke(WHITE, 2)
        elbow.set_stroke(WHITE, 2)

        # Triangle
        triangle = Polygon(p1, foot, p2)
        triangle.set_stroke(width=0)
        triangle.set_fill(YELLOW, 0.5)
        d_label = Tex(R"d", font_size=24)
        d_label.next_to(triangle, DOWN, SMALL_BUFF)

        # Leg
        diff_segment = Line(p1, foot)
        diff_segment.set_stroke(RED, 2)
        brace = VMobject().set_points_as_corners([LEFT, UL, UR, RIGHT])
        brace.set_shape(diff_segment.get_length(), 0.1)
        brace.set_stroke(WHITE, 1)
        # brace = Brace(Line(ORIGIN, 0.75 * RIGHT), UP)
        # brace.set_shape(diff_segment.get_length(), 0.15)
        brace.rotate(PI / 2 - theta)
        brace.move_to(diff_segment).shift(0.1 * rotate_vector(to_point, PI / 2))

        # Angle label
        arc_rad = min(0.35 * dist, 0.35 * get_norm(foot - p2))
        arc = Arc(PI, -theta, radius=arc_rad).shift(p2)
        arc.set_stroke(WHITE, 2)
        small_theta_sym = Tex(R"\theta")
        small_theta_sym.set_height(0.8 * arc.get_height())
        small_theta_sym.next_to(arc.pfp(0.5), LEFT, buff=0.05)

        return VGroup(triangle, elbow, altitude, arc, small_theta_sym, diff_segment, brace, d_label)

    def old(self):
        # Old
        dist_label = DecimalNumber(num_decimal_places=1)
        dist_label.set_height(4)
        dist_label.add_updater(lambda m: m.next_to(L_line.get_center(), RIGHT, buff=2))
        dist_label.add_updater(lambda m: m.set_value(L_line.get_length()))
