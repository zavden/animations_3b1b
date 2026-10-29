# ==============================================================================
# Scene:      BreakDownLaplaceTransform
# Source:     videos/_2025/laplace/integration.py (lines 1403-1624)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/exponentials.py
#
# Run from this folder:
#     manimgl BreakDownLaplaceTransform.py BreakDownLaplaceTransform -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/exponentials.py -----

S_COLOR = YELLOW


class SPlane(InteractiveScene):
    tex_to_color_map = {"s": YELLOW, "t": BLUE, R"\omega": PINK}
    s_plane_x_range = (-2, 2)
    s_label_font_size = 36
    s_label_config = dict(
        hide_zero_components_on_complex=True,
        include_sign=True,
        num_decimal_places=1,
    )

    def construct(self):
        # Trackers
        s_tracker = self.s_tracker = ComplexValueTracker(-1)
        t_tracker = self.t_tracker = ValueTracker(0)
        get_s = s_tracker.get_value
        get_t = t_tracker.get_value

        # Add s plane
        s_plane = self.get_s_plane()
        s_dot, s_label = self.get_s_dot_and_label(s_plane, get_s)
        self.add(s_plane, s_dot, s_label)

        # Add exp plane
        exp_plane = self.get_exp_plane()
        exp_plane_label = self.get_exp_plane_label(exp_plane)
        output_dot, output_label = self.get_output_dot_and_label(exp_plane, get_s, get_t)
        output_path = self.get_output_path(exp_plane, get_t, get_s)

        self.add(exp_plane, exp_plane_label, output_path, output_dot, output_label)

        # Add e^{st} graph
        axes = self.get_graph_axes()
        graph = self.get_dynamic_exp_graph(axes, get_s)
        v_line = self.get_graph_v_line(axes, get_t, get_s)

        self.add(axes, graph, v_line)

        # Move s around, end at i
        s_tracker.set_value(-1)
        self.play(s_tracker.animate.set_value(0.2), run_time=4)
        self.play(s_tracker.animate.set_value(0), run_time=2)
        self.play(s_tracker.animate.set_value(1j), run_time=3)
        self.wait()

        # Let time tick forward
        frame = self.frame
        self.play_time_forward(
            3 * TAU,
            added_anims=[frame.animate.set_x(3).set_height(12).set_anim_args(time_span=(6, 15))],
        )
        self.wait()
        self.play(
            t_tracker.animate.set_value(0),
            frame.animate.set_x(1.5).set_height(10),
            run_time=3
        )

        # Set s to 2i, then add vectors
        t2c = {"2i": YELLOW, **self.tex_to_color_map}
        exp_2it_label = Tex(R"e^{2i t}", t2c=t2c)
        exp_2it_label.move_to(exp_plane_label, RIGHT)

        self.play(s_tracker.animate.set_value(2j), run_time=2)
        self.play(
            FadeOut(exp_plane_label, 0.5 * UP),
            FadeIn(exp_2it_label, 0.5 * UP),
        )
        self.play_time_forward(TAU)

        # Show the derivative
        exp_plane.target = exp_plane.generate_target()
        exp_plane.target.align_to(axes.c2p(0, 0), LEFT)

        deriv_expression = Tex(R"\frac{d}{dt} e^{2i t} = 2i \cdot e^{2i t}", t2c=t2c)
        deriv_expression.next_to(exp_plane.target, RIGHT, aligned_edge=UP)

        self.play(
            LaggedStart(
                ReplacementTransform(exp_2it_label, deriv_expression["e^{2i t}"][0], path_arc=-90 * DEG),
                MoveToTarget(exp_plane),
                Write(deriv_expression[R"\frac{d}{dt}"]),
                lag_ratio=0.2
            ),
            frame.animate.reorient(0, 0, 0, (1, 0, 0.0), 9.25),
        )
        self.play(LaggedStart(
            Write(deriv_expression["="]),
            TransformFromCopy(*deriv_expression["e^{2i t}"], path_arc=-90 * DEGREES),
            FadeTransform(deriv_expression["e^{2i t}"][0][1:3].copy(), deriv_expression[R"2i"][1], path_arc=-90 * DEG),
            Write(deriv_expression[R"\cdot"]),
            lag_ratio=0.25,
            run_time=1.5
        ))
        self.add(deriv_expression)
        self.wait()

        # Step through derivative parts
        v_part, p_part, i_part, two_part = parts = VGroup(
            deriv_expression[R"\frac{d}{dt} e^{2i t}"][0],
            deriv_expression[R"e^{2i t}"][1],
            deriv_expression[R"i"][1],
            deriv_expression[R"2"][1],
        )
        colors = [GREEN, BLUE, YELLOW, YELLOW]
        labels = VGroup(Text("Velocity"), Text("Position"), Tex(R"90^{\circ}"), Text("Stretch"))
        for part, color, label in zip(parts, colors, labels):
            part.rect = SurroundingRectangle(part, buff=0.05)
            part.rect.set_stroke(color, 2)
            label.set_color(color)
            label.next_to(part.rect, DOWN)
            part.label = label

        p_vect, v_vect = vectors = self.get_pv_vectors(exp_plane, get_t, get_s)
        for vector in vectors:
            vector.suspend_updating()
        p_vect_copy = p_vect.copy().clear_updaters()

        self.play(
            ShowCreation(v_part.rect),
            FadeIn(v_part.label),
            GrowArrow(v_vect),
        )
        self.wait()
        self.play(
            ReplacementTransform(v_part.rect, p_part.rect),
            FadeTransform(v_part.label, p_part.label),
            GrowArrow(p_vect),
        )
        self.wait()
        self.play(
            ReplacementTransform(p_part.rect, i_part.rect),
            FadeTransform(p_part.label, i_part.label),
            p_vect_copy.animate.rotate(90 * DEG, about_point=exp_plane.n2p(0)).shift(p_vect.get_vector())
        )
        self.wait()
        self.play(
            ReplacementTransform(i_part.rect, two_part.rect),
            FadeTransform(i_part.label, two_part.label),
            Transform(p_vect_copy, v_vect, remover=True)
        )
        self.wait()
        self.play(FadeOut(two_part.rect), FadeOut(two_part.label))

        vectors.resume_updating()
        self.play_time_forward(TAU)

        # Label this angular frequency with omega
        imag_exp = Tex(R"e^{i \omega t}", t2c=self.tex_to_color_map, font_size=60)
        imag_exp.move_to(deriv_expression, LEFT)

        self.play(
            FadeOut(deriv_expression, 0.5 * UP),
            FadeIn(imag_exp, 0.5 * UP),
        )
        t_tracker.set_value(0)
        output_path.suspend_updating()
        self.play(s_tracker.animate.set_value(1.5j), run_time=3)
        output_path.resume_updating()
        self.play_time_forward(TAU * 4 / 3)

        # Move to other complex values, end at -0.5 + i
        t_max_tracker = ValueTracker(20 * TAU)
        new_output_path = self.get_output_path(exp_plane, t_max_tracker.get_value, get_s)
        output_path.match_updaters(new_output_path)
        t_tracker.set_value(0)

        self.play(
            FadeOut(imag_exp, time_span=(0, 1)),
            s_tracker.animate.set_value(-0.2 + 1.5j),
            run_time=2
        )
        self.play(s_tracker.animate.set_value(-0.2 + 1j), run_time=2)
        self.play(s_tracker.animate.set_value(-0.5 + 1j), run_time=2)
        self.play_time_forward(TAU)

        # Split up the exponential to e^{-0.5t} * e^{it}
        t2c = {"-0.5": YELLOW, "i": YELLOW, "t": BLUE}
        lines = VGroup(
            Tex(R"e^{(-0.5 + i)t}", t2c=t2c),
            Tex(R"\left(e^{-0.5t} \right) \left(e^{it} \right)", t2c=t2c)
        )
        lines.arrange(DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        lines.next_to(exp_plane, RIGHT, LARGE_BUFF, aligned_edge=UP)

        dec_brace = Brace(lines[1][R"\left(e^{-0.5t} \right)"], DOWN, SMALL_BUFF)
        rot_brace = Brace(lines[1][R"\left(e^{it} \right)"], DOWN, SMALL_BUFF)
        dec_label = dec_brace.get_text("Decay")
        rot_label = rot_brace.get_text("Rotation")

        self.play(
            FadeIn(lines[0], time_span=(0.5, 1)),
            FadeTransform(s_label[-1].copy(), lines[0]["-0.5 + i"])
        )
        self.wait()
        self.play(
            TransformMatchingTex(lines[0].copy(), lines[1], run_time=1, lag_ratio=0.01)
        )
        self.wait()
        self.play(
            GrowFromCenter(dec_brace),
            FadeIn(dec_label)
        )
        self.wait()
        self.play(
            ReplacementTransform(dec_brace, rot_brace),
            FadeTransform(dec_label, rot_label),
        )
        self.wait()
        self.play(
            FadeOut(rot_brace),
            FadeOut(rot_label),
            t_tracker.animate.set_value(0).set_anim_args(run_time=3)
        )

        # Show multiplication by s
        s_vect = Arrow(s_plane.n2p(0), s_plane.n2p(get_s()), buff=0, fill_color=YELLOW)
        one_vect = Arrow(s_plane.n2p(0), s_plane.n2p(1), buff=0, fill_color=BLUE)
        arc = Line(
            s_plane.n2p(0.3),
            s_plane.n2p(0.3 * get_s()),
            path_arc=s_vect.get_angle(),
            buff=0.1
        )
        arc.add_tip(length=0.25, width=0.25)
        times_s_label = Tex(R"\times s")
        times_s_label.next_to(arc.pfp(0.5), UR, SMALL_BUFF)

        self.play(LaggedStart(
            FadeIn(one_vect),
            FadeIn(arc),
            FadeIn(times_s_label),
            FadeIn(s_vect),
        ))
        self.wait()
        self.play(
            TransformFromCopy(one_vect, s_vect, path_arc=s_vect.get_angle()),
            run_time=2
        )
        self.wait()
        self.play(
            TransformFromCopy(one_vect, p_vect),
            TransformFromCopy(s_vect, v_vect),
            run_time=2
        )

        # Show spiraling inward
        self.play_time_forward(2 * TAU)

        self.play(FadeOut(VGroup(arc, times_s_label, lines)))
        t_tracker.set_value(0)

        s_vect.add_updater(lambda m: m.put_start_and_end_on(s_plane.n2p(0), s_plane.n2p(get_s())))
        self.add(s_vect)

        # Tour various values on the s plane
        values = [
            -0.1 + 2j,
            -0.1 - 2j,
            -0.1 + 0.5j,
            +0.05 + 0.5j,
            -0.5 + 0.5j,
            -0.1 + 0.5j,
        ]
        for value in values:
            self.play(s_tracker.animate.set_value(value), run_time=5)
            if value == values[0]:
                self.play_time_forward(TAU)
                self.t_tracker.set_value(0)

        self.play_time_forward(4 * TAU)

    def get_s_plane(self):
        s_plane = ComplexPlane(self.s_plane_x_range, self.s_plane_x_range)
        s_plane.set_width(7)
        s_plane.to_edge(LEFT, buff=SMALL_BUFF)
        s_plane.add_coordinate_labels(font_size=16)
        return s_plane

    def get_s_dot_and_label(self, s_plane, get_s):
        s_dot = Group(
            Dot(radius=0.05, fill_color=YELLOW),
            GlowDot(color=YELLOW),
        )
        s_dot.add_updater(lambda m: m.move_to(s_plane.n2p(get_s())))

        s_label = Tex(R"s = +0.5", font_size=self.s_label_font_size)
        s_rhs = s_label.make_number_changeable("+0.5", **self.s_label_config)
        s_rhs.f_always.set_value(get_s)
        s_label.set_color(S_COLOR)
        s_label.set_backstroke(BLACK, 5)
        s_label.always.next_to(s_dot[0], UR, SMALL_BUFF)

        return Group(s_dot, s_label)

    def get_exp_plane(self, x_range=(-2, 2)):
        exp_plane = ComplexPlane(x_range, x_range)
        exp_plane.background_lines.set_stroke(width=1)
        exp_plane.faded_lines.set_stroke(opacity=0.25)
        exp_plane.set_width(4)
        exp_plane.to_corner(DR).shift(0.5 * LEFT)

        return exp_plane

    def get_exp_plane_label(self, exp_plane, font_size=60):
        label = Tex(R"e^{st}", font_size=font_size, t2c=self.tex_to_color_map)
        label.set_backstroke(BLACK, 5)
        label.next_to(exp_plane.get_corner(UL), DL, 0.2)
        return label

    def get_output_dot_and_label(self, exp_plane, get_s, get_t, label_direction=UR, s_tex="s"):
        output_dot = Group(
            TrueDot(color=GREEN),
            GlowDot(color=GREEN)
        )
        output_dot.add_updater(lambda m: m.move_to(exp_plane.n2p(np.exp(get_s() * get_t()))))

        output_label = Tex(Rf"e^{{{s_tex} \cdot 0.00}}", font_size=36, t2c=self.tex_to_color_map)
        t_label = output_label.make_number_changeable("0.00")
        t_label.set_color(BLUE)
        s_term = output_label[s_tex][0][0]
        t_label.set_height(s_term.get_height() * 1.2, about_edge=LEFT)
        t_label.f_always.set_value(get_t)
        t_label.always.match_y(s_term, DOWN)
        output_label.always.next_to(output_dot, label_direction, buff=SMALL_BUFF, aligned_edge=LEFT, index_of_submobject_to_align=0),
        output_label.set_backstroke(BLACK, 3)

        return Group(output_dot, output_label)

    def get_graph_axes(
        self,
        x_range=(0, 24),
        y_range=(-2, 2),
        width=15,
        height=2,
    ):
        axes = Axes(x_range, y_range, width=width, height=height)
        x_axis_label = Tex(R"t", font_size=36, t2c=self.tex_to_color_map)
        y_axis_label = Tex(R"\text{Re}\left[e^{st}\right]", font_size=36, t2c=self.tex_to_color_map)
        x_axis_label.next_to(axes.x_axis.get_right(), UP, buff=0.15)
        y_axis_label.next_to(axes.y_axis.get_top(), UP, SMALL_BUFF)
        axes.add(x_axis_label)
        axes.add(y_axis_label)
        axes.next_to(ORIGIN, RIGHT, MED_LARGE_BUFF)
        axes.to_edge(UP, buff=0.5)
        x_axis_label.shift_onto_screen(buff=MED_LARGE_BUFF)
        return axes

    def get_dynamic_exp_graph(self, axes, get_s, delta_t=0.1, stroke_color=TEAL, stroke_width=3):
        graph = Line().set_stroke(stroke_color, stroke_width)
        t_samples = np.arange(*axes.x_range[:2], 0.1)

        def update_graph(graph):
            s = get_s()
            values = np.exp(s * t_samples)
            xs = values.astype(np.complex128).real
            graph.set_points_smoothly(axes.c2p(t_samples, xs))

        graph.add_updater(update_graph)
        return graph

    def get_graph_v_line(self, axes, get_t, get_s):
        v_line = Line(DOWN, UP)
        v_line.set_stroke(WHITE, 2)
        v_line.f_always.put_start_and_end_on(
            lambda: axes.c2p(get_t(), 0),
            lambda: axes.c2p(get_t(), np.exp(get_s() * get_t()).real),
        )
        return v_line

    def get_output_path(self, exp_plane, get_t, get_s, delta_t=1 / 30, color=TEAL, stroke_width=2):
        path = VMobject()
        path.set_points([ORIGIN])
        path.set_stroke(color, stroke_width)

        def get_path_points():
            t_range = np.arange(0, get_t(), delta_t)
            if len(t_range) == 0:
                t_range = np.array([0])
            values = np.exp(t_range * get_s())
            return np.array([exp_plane.n2p(z) for z in values])

        path.f_always.set_points_smoothly(get_path_points)
        return path

    def play_time_forward(self, time, added_anims=[]):
        self.t_tracker.set_value(0)
        self.play(
            self.t_tracker.animate.set_value(time).set_anim_args(rate_func=linear),
            *added_anims,
            run_time=time,
        )

    def get_pv_vectors(self, exp_plane, get_t, get_s, thickness=3, colors=[BLUE, YELLOW]):
        p_vect = Vector(RIGHT, fill_color=colors[0], thickness=thickness)
        v_vect = Vector(RIGHT, fill_color=colors[1], thickness=thickness)
        p_vect.add_updater(lambda m: m.put_start_and_end_on(
            exp_plane.n2p(0),
            exp_plane.n2p(np.exp(get_t() * get_s()))
        ))
        v_vect.add_updater(lambda m: m.put_start_and_end_on(
            exp_plane.n2p(0),
            exp_plane.n2p(get_s() * np.exp(get_t() * get_s()))
        ).shift(p_vect.get_vector()))

        return VGroup(p_vect, v_vect)

    ###

    def setup_for_square_frame(self):
        # For an insert
        axes.next_to(s_plane, UP, LARGE_BUFF, aligned_edge=LEFT)
        exp_plane.match_height(s_plane).next_to(s_plane, RIGHT, buff=1.5)
        exp_plane_label.set_height(1).next_to(exp_plane, RIGHT, aligned_edge=UP)
        output_label.set_fill(opacity=0).set_stroke(opacity=0)
        self.add(exp_plane_label)

        axes[:-2].stretch(2.5, 1, about_edge=DOWN)
        axes.x_axis.ticks.stretch(1 / 2.5, 1)
        axes[-2].next_to(axes.x_axis.get_right(), UP, MED_SMALL_BUFF)
        axes[-1].next_to(axes.y_axis.get_top(), RIGHT, MED_SMALL_BUFF)

        self.frame.reorient(0, 0, 0, (1.0, 2.68, 0.0), 16.00)

    def old_material(self):
        # Collapse the graph
        output_dot = GlowDot(color=GREEN)
        output_dot.move_to(axes.x_axis.n2p(1))
        output_label = Tex(R"e^{s \cdot 0.00}", **tex_kw, font_size=36)
        t_tracker.set_value(0)
        t_label = output_label.make_number_changeable("0.00")
        t_label.set_color(BLUE)
        t_label.match_height(output_label["s"], about_edge=LEFT)
        t_label.f_always.set_value(get_t)
        output_label.add_updater(lambda m: m.next_to(output_dot, UP, SMALL_BUFF, LEFT).shift(0.2 * DR))

        graph.clear_updaters()
        self.remove(axes)
        self.play(LaggedStart(
            FadeOut(VGroup(axes.x_axis, x_axis_label, graph)),
            AnimationGroup(
                Rotate(axes.y_axis, -90 * DEG),
                TransformMatchingTex(y_axis_label, output_label, run_time=1.5),
            ),
            FadeIn(output_dot),
            lag_ratio=0.5
        ))



# ----- From _2025/laplace/integration.py -----

def z_to_color(z, sat=0.5, lum=0.5):
    angle = math.atan2(z.imag, z.real)
    return Color(hsl=(angle / TAU, sat, lum))


def get_complex_graph(
    s_plane,
    func,
    min_real=None,
    pole_buff=1e-3,
    color_by_phase=True,
    opacity=0.7,
    shading=(0.1, 0.1, 0.1),
    resolution=(301, 301),
    saturation=0.5,
    luminance=0.5,
    mesh_resolution=(61, 61),
    mesh_stroke_style=dict(
        color=WHITE,
        width=1,
        opacity=0.15
    )
):
    u_range = list(s_plane.x_range[:2])
    v_range = list(s_plane.y_range[:2])

    if min_real is not None:
        u_range[0] = min_real + pole_buff

    unit_size = s_plane.x_axis.get_unit_size()
    graph = ParametricSurface(
        lambda u, v: [
            *s_plane.c2p(u, v)[:2],
            unit_size * abs(func(complex(u, v)))
        ],
        u_range=u_range,
        v_range=v_range,
        resolution=resolution
    )
    graph.set_shading(*shading)

    if color_by_phase:
        graph.color_by_uv_function(
            lambda u, v: z_to_color(func(complex(u, v)), sat=saturation, lum=luminance)
        )

    graph.set_opacity(opacity)
    graph.set_sort_to_camera()

    # Add mesh
    mesh = SurfaceMesh(graph, resolution=mesh_resolution)
    mesh.set_stroke(**mesh_stroke_style)

    return Group(graph, mesh)


class IntegrateComplexExponential(SPlane):
    staggered_path_colors = [MAROON_B, MAROON_C]
    t_max = 100  # For dynamic path and vector sum.  Change to 100 for final render
    initial_s = 0.2 + 1j
    s_label_config = dict(
        hide_zero_components_on_complex=False,
        include_sign=True,
        num_decimal_places=1,
    )

    def setup(self):
        super().setup()
        # Trackers
        self.s_tracker = ComplexValueTracker(self.initial_s)
        self.t_tracker = ValueTracker(0)
        get_s = self.s_tracker.get_value
        get_t = self.t_tracker.get_value

        def exp_func(t):
            return np.exp(-get_s() * t)

        self.exp_func = exp_func

    def construct(self):
        # Trackers
        s_tracker = self.s_tracker
        t_tracker = self.t_tracker
        exp_func = self.exp_func
        t2c = self.tex_to_color_map

        get_s = self.s_tracker.get_value
        get_t = self.t_tracker.get_value

        # Add s plane
        s_plane, s_dot, s_label, s_plane_label = s_group = self.get_s_group()
        self.add(*s_group)

        # Add exp plane
        exp_plane = self.get_exp_plane()
        exp_plane.set_width(6)
        exp_plane.next_to(s_plane, RIGHT, buff=1.0)
        exp_plane.add_coordinate_labels(font_size=16)
        exp_plane.axes.set_stroke(width=1)
        exp_plane_label = Tex(R"e^{\minus st}", font_size=72, t2c=t2c)
        exp_plane_label.next_to(exp_plane, UP)

        output_dot, output_label = self.get_output_dot_and_label(exp_plane, lambda: -get_s(), get_t, label_direction=DR, s_tex=R"\minus s")
        output_label.set_z_index(1)
        output_label_added_shift = Point(ORIGIN)
        output_label.add_updater(lambda m: m.shift(output_label_added_shift.get_center()))

        self.add(exp_plane, exp_plane_label, output_dot, output_label)

        # Show inital path
        path = always_redraw(lambda: self.get_output_path(exp_plane, exp_func, 0, 20))

        self.play(
            ShowCreation(path, suspend_mobject_updating=True),
            t_tracker.animate.set_value(path.t_range[1]),
            rate_func=linear,
            run_time=10,
        )
        self.play(
            s_tracker.animate.set_value(0.2 - 1j),
            rate_func=there_and_back,
            run_time=6,
        )
        self.play(
            s_tracker.animate.set_value(-0.2 + 1j),
            rate_func=there_and_back,
            run_time=6,
        )

        path.suspend_updating()

        # Fadeable transition to the start
        path_ghost = path.copy().set_stroke(opacity=0.4)
        self.wait()
        t_tracker.set_value(0)
        self.remove(path)
        self.add(path_ghost)
        self.wait()

        # Show [0, 1]
        subpath_0 = self.get_output_path(exp_plane, exp_func, 0, 1, stroke_color=self.staggered_path_colors[0])
        avg_vect0 = self.get_mean_vector(exp_plane, exp_func, 0, 1)
        many_points = self.get_sample_dots(subpath_0)
        avg_dot0 = TrueDot(avg_vect0.get_end(), color=RED)

        int_tex0 = Tex(R"\int^1_0 e^{\minus st} dt", t2c=t2c, font_size=48)
        int_tex0.next_to(exp_plane.n2p(1), UP, MED_SMALL_BUFF)
        int_tex0.set_backstroke(BLACK, 5)

        self.play(FadeIn(int_tex0, 0.25 * UP))
        self.play(
            t_tracker.animate.set_value(1),
            ShowCreation(subpath_0),
            rate_func=linear,
            run_time=2
        )
        self.wait()
        self.play(ShowCreation(many_points))
        self.wait()
        self.play(ReplacementTransform(many_points, avg_dot0))
        self.wait()
        self.play(
            GrowArrow(avg_vect0),
            int_tex0.animate.set_height(0.75).next_to(avg_vect0.get_center(), UR, buff=SMALL_BUFF)
        )
        self.play(FadeOut(avg_dot0))
        self.wait()

        # Bring in integral plane
        lil_exp_plane = self.get_exp_plane(x_range=(-1, 1))
        lil_exp_plane.set_width(3)
        lil_exp_plane.move_to(exp_plane, UR).shift(0.5 * UP + 0.75 * LEFT)
        lil_exp_plane.save_state()
        lil_exp_plane.axes.set_stroke(width=1)

        int_plane = self.get_exp_plane()
        int_plane.set_width(3)
        int_plane.next_to(lil_exp_plane, DOWN, MED_LARGE_BUFF)
        int_plane.axes.set_stroke(width=1)
        int_plane.add_coordinate_labels(font_size=12)

        to_upper = lil_exp_plane.get_center() - exp_plane.get_center()
        to_lower = int_plane.get_center() - exp_plane.get_center()

        int_plane_label = Tex(R"\int^\infty_0 e^{\minus st} dt", t2c=t2c, font_size=48)
        int_plane_label.next_to(int_plane, LEFT, aligned_edge=UP)

        lower_avg_vect0 = self.get_mean_vector(int_plane, exp_func, 0, 1, thickness=1, fill_color=self.staggered_path_colors[0])

        self.play(
            exp_plane.animate.move_to(lil_exp_plane.saved_state).set_opacity(0),
            FadeIn(lil_exp_plane, to_upper),
            VGroup(path_ghost, subpath_0, avg_vect0).animate.shift(to_upper),
            int_tex0.animate.scale(0.5, about_point=exp_plane.n2p(0)).shift(to_lower),
            TransformFromCopy(avg_vect0, lower_avg_vect0),
            FadeIn(int_plane),
            exp_plane_label.animate.next_to(lil_exp_plane, LEFT, aligned_edge=UP),
        )
        self.wait()

        # Add the next few arrows
        avg_vects = VGroup(avg_vect0)
        lower_avg_vects = VGroup(lower_avg_vect0)
        subpaths = VGroup(subpath_0)
        int_texs = VGroup(int_tex0)
        shifts = [
            0.8 * LEFT + 0.1 * DOWN,
            LEFT,
            0.2 * LEFT + 0.4 * UP,
            0.4 * UP,
        ]

        def get_subpath(n):
            result = self.get_output_path(exp_plane, exp_func, n, n + 1, stroke_width=3)
            result.set_stroke(self.staggered_path_colors[n % 2])
            return result

        for n in range(1, 5):
            subpath_n = get_subpath(n)
            sample_points = self.get_sample_dots(subpath_n)
            avg_vect, lower_avg_vect = [
                self.get_mean_vector(plane, exp_func, n, n + 1, thickness=thickness)
                for plane, thickness in [(exp_plane, 3), (int_plane, 1)]
            ]
            lower_avg_vect.set_fill(self.staggered_path_colors[n % 2], border_width=0.5)
            lower_avg_vect.set_stroke(width=0)
            lower_avg_vect.put_start_on(lower_avg_vects[-1].get_end())
            avg_dot = sample_points.copy().set_points([avg_vect.get_end()])

            int_tex = Tex(Rf"\int_{n}^{n + 1} e^{{\minus s t}} dt", t2c=t2c)
            int_tex.match_height(int_tex0)
            int_tex.scale(1.0 - 0.15 * n)
            int_tex.next_to(lower_avg_vect.get_center(), rotate_vector(lower_avg_vect.get_vector(), 90 * DEG), buff=SMALL_BUFF)

            self.play(
                t_tracker.animate.set_value(n + 1),
                ShowCreation(subpath_n),
                output_label_added_shift.animate.move_to(shifts[n - 1]),
                ShowCreation(sample_points),
                run_time=2,
                rate_func=linear,
            )
            self.play(
                avg_vects[-1].animate.set_fill(opacity=0.5).set_stroke(width=0),
                GrowArrow(avg_vect),
                Transform(sample_points, avg_dot),
            )
            self.play(
                FadeOut(sample_points),
                TransformFromCopy(avg_vect, lower_avg_vect),
                FadeIn(int_tex),
            )

            avg_vects.add(avg_vect)
            lower_avg_vects.add(lower_avg_vect)
            subpaths.add(subpath_n)
            int_texs.add(int_tex)

        # Show numerous more
        for n in range(5, 20):
            subpath = get_subpath(n)
            avg_vect = self.get_mean_vector(exp_plane, exp_func, n, n + 1, thickness=3)
            lower_avg_vect = self.get_mean_vector(int_plane, exp_func, n, n + 1, thickness=1)
            lower_avg_vect.set_fill(self.staggered_path_colors[n % 2], border_width=0.5)
            lower_avg_vect.set_stroke(width=0)
            lower_avg_vect.put_start_on(lower_avg_vects[-1].get_end())

            anims = [
                ShowCreation(subpath, rate_func=linear),
                t_tracker.animate.set_value(n + 1).set_anim_args(rate_func=linear),
                FadeIn(avg_vect),
            ]
            if n == 5:
                anims.append(avg_vects.animate.set_opacity(0.25).set_stroke(width=0))
            else:
                anims.append(avg_vects[-1].animate.set_opacity(0.25).set_stroke(width=0))
                anims.append(TransformFromCopy(avg_vects[-1], lower_avg_vects[-1]))
            self.play(*anims)

            avg_vects.add(avg_vect)
            lower_avg_vects.add(lower_avg_vect)
            subpaths.add(subpath)

            self.add(avg_vects, subpaths, *lower_avg_vects[:-1])

        # Show the full integral
        int_dot = Group(TrueDot(radius=0.025), GlowDot())
        int_dot.set_color(MAROON_B)
        int_dot.move_to(int_plane.n2p(1 / get_s()))
        int_rect = SurroundingRectangle(int_plane_label)
        int_rect.set_stroke(YELLOW, 2)

        self.play(
            LaggedStart(
                (FadeTransform(int_tex, int_plane_label)
                for int_tex in int_texs),
                lag_ratio=0.025,
                group_type=Group,
            ),
            *map(FadeOut, [output_label, output_dot, avg_vects]),
        )
        self.play(ShowCreation(int_rect))
        self.wait()
        self.play(
            int_rect.animate.surround(int_dot[0], buff=0),
            FadeIn(int_dot),
        )
        self.play(FadeOut(int_rect))
        self.wait()

        # Make the diagram dynamic
        staggered_path = self.get_dynamic_output_path(exp_plane, exp_func)
        int_pieces = self.get_dynamic_vector_sum(int_plane, exp_func)
        int_dot.add_updater(lambda m: m.move_to(int_plane.n2p(1.0 / get_s())))

        dynamic_pieces = Group(staggered_path, int_pieces)

        self.play(FlashAround(Group(s_label, s_dot), time_width=1.5, run_time=2))
        self.remove(path_ghost, subpaths, lower_avg_vects)
        self.add(staggered_path, int_pieces, int_dot)

        # Move around the path
        s_rect = int_rect.copy()

        self.play(s_tracker.animate.set_value(0.2 - 1j), run_time=6)
        self.wait()
        self.play(s_tracker.animate.set_value(1), run_time=4)
        s_rect.surround(Group(s_label))
        self.play(ShowCreation(s_rect))
        self.play(s_rect.animate.surround(int_dot[0], buff=0))
        self.play(FadeOut(s_rect))
        self.wait()

        # Approach zero, then go vertical
        frame = self.frame
        self.play(
            s_tracker.animate.set_value(0.1).set_anim_args(rate_func=bezier([0, 1, 1, 1])),
            frame.animate.reorient(0, 0, 0, (2.75, 0, 0.0), 11).set_anim_args(time_span=(2, 8)),
            run_time=8,
        )
        self.wait()
        self.play(
            s_tracker.animate.set_value(0.1 + 2j),
            frame.animate.to_default_state(),
            run_time=10
        )
        self.play(s_tracker.animate.set_value(0.1 - 2j), run_time=5)
        self.wait()
        self.play(s_tracker.animate.set_value(0.2 + 1j), run_time=5)
        self.wait()

        # Emphasize output
        int_vect = self.get_vector(int_plane, 1 / get_s(), thickness=2, fill_color=WHITE)
        int_vect.set_stroke(width=0).set_fill(border_width=0.5)
        rect = SurroundingRectangle(int_plane_label)
        rect.set_stroke(YELLOW, 2)
        int_vect_outline = int_vect.copy().set_fill(opacity=0).set_stroke(WHITE, 1)

        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            rect.animate.surround(int_dot[0], buff=0),
            int_pieces.animate.set_fill(opacity=0.5),
        )
        self.wait()
        self.play(
            GrowArrow(int_vect),
            FadeOut(rect),
            FadeOut(int_dot),
        )
        self.wait()

        # Plot it
        frame = self.frame
        s_plane_group = Group(s_plane, s_dot, s_label, s_plane_label)
        s_label.set_flat_stroke(True)
        s_plane.set_flat_stroke(False)
        s_plane_group.save_state()
        s_plane_group.center()
        self.remove(s_plane_group)

        for mob in self.get_mobjects():
            mob.fix_in_frame()
            mob.set_z_index(2)

        right_rect = FullScreenRectangle()
        right_rect.set_fill(BLACK, 1).set_stroke(width=0)
        right_rect.set_width(lil_exp_plane.get_width() + 2, about_edge=RIGHT, stretch=True)
        v_line = DashedLine(right_rect.get_corner(DL), right_rect.get_corner(UL))
        v_line.set_stroke(WHITE, 1)
        right_pannel = VGroup(right_rect, v_line)
        right_pannel.fix_in_frame()
        right_pannel.set_z_index(1)
        self.add(right_pannel)

        def get_output_magnitude(s):
            return abs(1.0 / s)

        z_line = Line(ORIGIN, OUT)
        z_line.set_stroke(WHITE, 2)

        unit_size = s_plane.x_axis.get_unit_size()
        z_line.add_updater(lambda m: m.put_start_and_end_on(
            s_plane.n2p(get_s()),
            s_plane.n2p(get_s()) + unit_size * get_output_magnitude(get_s()) * OUT,
        ))

        out_dot = Group(TrueDot(), GlowDot())
        out_dot.set_color(TEAL)
        out_dot.f_always.move_to(z_line.get_end)

        traced_graph = TracedPath(z_line.get_end, stroke_color=TEAL)
        traced_graph.update()

        int_vect.add_updater(
            lambda m: m.put_start_and_end_on(
                int_plane.n2p(0),
                int_plane.n2p(1.0 / get_s()),
            )
        )

        pre_z_line = Line(int_vect.get_start(), int_vect.get_end())
        pre_z_line.set_stroke(WHITE, 5)
        pre_z_line.set_z_index(2)

        new_exp_plane_label = exp_plane_label.copy().scale(0.5).next_to(lil_exp_plane, RIGHT, aligned_edge=UP)
        new_int_plane_label = int_plane_label.copy().scale(0.5).next_to(int_plane, RIGHT, SMALL_BUFF, aligned_edge=UP)

        s_plane_group.restore()
        self.play(
            frame.animate.reorient(-3, 68, 0, (1.43, 0.51, -0.28), 6.50),
            s_plane_group.animate.center(),
            ReplacementTransform(pre_z_line, z_line),
            FadeOut(exp_plane_label, time_span=(1, 2)),
            FadeIn(new_exp_plane_label, time_span=(1, 2)),
            FadeOut(int_plane_label, time_span=(1, 2)),
            FadeIn(new_int_plane_label, time_span=(1, 2)),
            VFadeIn(v_line, time_span=(2, 3)),
            run_time=3,
        )
        self.play(
            FadeIn(out_dot, time_span=(0, 1)),
            frame.animate.reorient(8, 64, 0, (1.43, 0.51, -0.28), 6.50),
            run_time=3
        )

        self.add(traced_graph)
        self.play(
            s_tracker.animate.set_value(0.2 - 2j),
            frame.animate.reorient(25, 87, 0, (3.18, 1.73, 2.63), 11.08).set_anim_args(time_span=(1, 7.5)),
            run_time=10
        )
        self.play(s_tracker.animate.set_value(0.4 - 2j))
        self.play(
            s_tracker.animate.set_value(0.4 + 2j),
            frame.animate.reorient(44, 81, 0, (3.16, 1.71, 2.63), 11.08),
            run_time=5,
        )
        self.play(s_tracker.animate.set_value(0.6 + 2j))
        self.play(
            s_tracker.animate.set_value(0.6 - 2j),
            frame.animate.reorient(66, 89, 0, (3.31, 2.07, 2.96), 9.69),
            run_time=5,
        )
        self.play(s_tracker.animate.set_value(0.8 - 2j))
        self.play(
            s_tracker.animate.set_value(0.8 + 2j),
            frame.animate.reorient(22, 84, 0, (2.56, 1.53, 1.72), 10.14),
            run_time=5
        )
        self.play(s_tracker.animate.set_value(1.0 + 2j))
        self.play(
            s_tracker.animate.set_value(1.0 - 2j),
            frame.animate.reorient(22, 84, 0, (2.56, 1.53, 1.72), 10.14),
            run_time=5
        )
        self.wait()

        traced_graph.suspend_updating()

        # Add the graph
        graph = get_complex_graph(s_plane, lambda s: 1.0 / s, min_real=0)[0]
        graph.set_shading(0.1, 0.1, 0)
        graph.save_state()
        graph.set_color(GREY_B)
        mesh = SurfaceMesh(graph, resolution=(11, 21))
        mesh.set_stroke(WHITE, 0.5, 0.5)
        for line in mesh:
            if line.get_z(IN) < 0:
                mesh.remove(line)

        self.play(
            ShowCreation(graph),
            ShowCreation(mesh, lag_ratio=1e-2, time_span=(1, 4)),
            VFadeOut(traced_graph),
            frame.animate.reorient(34, 74, 0, (2.02, 1.44, 1.88), 9.87),
            out_dot.animate.set_color(WHITE),
            run_time=4
        )

        self.play(
            s_tracker.animate.set_value(0.1 - 0.1j),
            frame.animate.reorient(38, 82, 0, (2.84, 2.62, 4.72), 14.21).set_anim_args(time_span=(0, 6)),
            run_time=10
        )
        self.wait()
        self.play(s_tracker.animate.set_value(0.5 - 0.1j), run_time=5)
        self.play(frame.animate.reorient(26, 72, 0, (2.33, 1.59, 1.91), 10.76), run_time=3)
        self.wait()
        self.play(
            s_tracker.animate.set_value(0.5 - 1j),
            run_time=3
        )
        self.wait()

        # Explain color
        hue_circle = Circle(radius=1.5 * int_plane.x_axis.get_unit_size())
        hue_circle.set_color_by_proportion(lambda h: Color(hsl=(h, 0.5, 0.5)))
        hue_circle.set_stroke(width=5)
        hue_circle.move_to(int_plane)
        hue_circle.fix_in_frame().set_z_index(2)

        brace = LineBrace(int_vect, direction=UP, buff=0)
        brace.set_fill(border_width=1)
        brace.set_z_index(2).fix_in_frame()

        self.play(GrowFromCenter(brace))
        self.wait()
        self.play(FadeOut(brace))

        self.play(ShowCreation(hue_circle, run_time=2))
        self.wait()
        self.play(
            Restore(graph, time_span=(0, 1)),
            frame.animate.reorient(29, 72, 0, (1.79, 1.9, 1.65), 11.21),
            run_time=4,
        )
        self.play(s_tracker.animate.set_value(0.5 + 1j), run_time=5)
        self.wait()

        # Show negative real part
        left_plane = Rectangle()
        left_plane.set_stroke(width=0).set_fill(RED, 0.5)
        left_plane.replace(s_plane, stretch=True)
        left_plane.stretch(0.5, 0, about_edge=LEFT)
        left_plane.save_state()
        left_plane.stretch(0, 0, about_edge=RIGHT)

        staggered_path.set_clip_plane(RIGHT, -v_line.get_x())
        int_pieces.set_clip_plane(RIGHT, -v_line.get_x())

        self.play(
            frame.animate.reorient(-38, 70, 5, (3.17, 1.96, -0.36), 9.16),
            FadeOut(hue_circle),
            Restore(left_plane, time_span=(3, 5)),
            run_time=5
        )
        self.wait()

        # Move to negative real
        self.play(
            s_tracker.animate.set_value(-0.5),
            VFadeOut(z_line, time_span=(0, 1.5)),
            FadeOut(out_dot, time_span=(0, 1.5)),
            VFadeOut(int_vect, time_span=(0, 1.0)),
            run_time=3
        )
        self.play(s_tracker.animate.set_value(-0.1 - 1j).set_anim_args(run_time=3))
        self.play(
            *(
                plane.animate.scale(0.1, about_point=plane.n2p(0))
                for plane in [exp_plane, lil_exp_plane, int_plane]
            ),
        )
        self.play(
            ShowCreation(staggered_path, suspend_mobject_updating=True),
            ShowIncreasingSubsets(int_pieces, suspend_mobject_updating=True),
            run_time=4
        )
        self.play(
            UpdateFromAlphaFunc(
                s_tracker,
                lambda m, a: m.set_value(complex(
                    -0.1 - math.sin(PI * a),
                    interpolate(-1, 1, a)
                ))
            ),
            run_time=8
        )
        self.play(
            *(
                plane.animate.scale(10, about_point=plane.n2p(0)).set_anim_args(time_span=(2, 4))
                for plane in [exp_plane, lil_exp_plane, int_plane]
            ),
            s_tracker.animate.set_value(1j),
            run_time=4
        )
        self.play(FadeIn(z_line), FadeIn(out_dot))
        self.wait()

        # Show imaginary input
        self.remove(staggered_path, int_pieces)
        int_pieces.set_fill(opacity=1)
        t_tracker.set_value(0)
        output_dot.fix_in_frame().set_z_index(2)
        output_label.add_updater(lambda m: m.fix_in_frame().set_z_index(2))
        self.play(
            FadeIn(output_dot),
            VFadeIn(output_label),
            left_plane.animate.set_fill(opacity=0.2),
        )
        max_n = 25
        self.play(
            ShowCreation(staggered_path[:max_n].set_z_index(2)),
            ShowIncreasingSubsets(int_pieces[:max_n].set_z_index(2), int_func=np.floor),
            t_tracker.animate.set_value(max_n).set_anim_args(time_span=(max_n / (max_n + 1), max_n)),
            rate_func=linear,
            run_time=max_n
        )
        self.play(
            VFadeOut(output_label),
            FadeOut(output_dot),
            t_tracker.animate.set_value(max_n + 1).set_anim_args(rate_func=linear),
            ShowIncreasingSubsets(int_pieces[max_n:].set_z_index(2)),
            FadeIn(staggered_path[max_n:].set_z_index(2))
        )

        # Show the limiting value
        self.add(staggered_path, int_pieces)
        self.add(int_vect)
        self.play(
            s_tracker.animate.set_value(0.1 + 1j),
            int_pieces.animate.set_fill(opacity=0.75),
            VFadeIn(int_vect),
            FadeOut(left_plane),
            run_time=2
        )
        rect = SurroundingRectangle(int_vect).set_z_index(2)
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait()
        self.play(
            s_tracker.animate.set_value(1j),
            run_time=5
        )
        self.wait()

        # Move along imaginary line
        boundary = TracedPath(z_line.get_end, stroke_color=RED, stroke_width=3)

        self.add(boundary, out_dot)
        self.play(s_tracker.animate.set_value(2j), run_time=3)
        self.play(s_tracker.animate.set_value(0.1j), run_time=3)
        self.play(s_tracker.animate.set_value(1j), run_time=3)
        boundary.clear_updaters()
        self.play(FadeOut(boundary))

        # Show this as 1 / s
        int_equation = Tex(R"\int^\infty_0 e^{\minus st} dt = \frac{1}{s}", t2c=t2c)
        int_equation.to_edge(UP).shift(LEFT)
        int_equation.fix_in_frame()
        lhs_mover = new_int_plane_label.copy()

        self.play(
            frame.animate.reorient(0, 85, 1, (5.32, 3.46, 3.69), 13.49),
            s_tracker.animate.set_value(0.2 + 1j),
            run_time=3,
        )
        self.play(
            lhs_mover.animate.replace(int_equation[:-4]),
            Write(int_equation[-4:], time_span=(0.75, 1.75)),
        )
        self.remove(lhs_mover)
        self.add(int_equation)
        self.wait()

        # Look closely at s = i again
        int_plane_rect = SurroundingRectangle(int_plane)
        int_plane_rect.fix_in_frame()
        int_plane_rect.set_stroke(YELLOW, 5).insert_n_curves(100)
        int_plane_rect.set_z_index(3)
        int_plane_rect.scale(0.5, about_edge=DOWN).scale(1.1)

        i_eq = Tex(R"\frac{1}{i} = -i")
        i_eq.next_to(int_equation[-3:], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        i_eq.fix_in_frame()

        left_arrow = Vector(LEFT).set_color(YELLOW)
        left_arrow.next_to(s_plane.n2p(0.4 + 1j), DOWN)

        self.play(s_tracker.animate.set_value(0.2 - 1j), run_time=6)
        self.play(
            s_tracker.animate.set_value(0.5 + 1j),
            frame.animate.reorient(-49, 79, 0, (6.24, 2.45, -0.13), 10.06),
            run_time=4
        )
        self.play(
            GrowArrow(left_arrow, time_span=(0, 1)),
            VShowPassingFlash(int_plane_rect, time_width=1.5, time_span=(4, 7)),
            Write(i_eq, time_span=(10, 12)),
            s_tracker.animate.set_value(1j),
            run_time=15
        )
        self.wait()
        self.play(
            frame.animate.reorient(0, 85, 1, (5.32, 3.46, 3.69), 13.49),
            FadeOut(i_eq),
            FadeOut(left_arrow),
            run_time=3
        )

        # Ambient s movement
        for z in [0.2 - 1j, 1 - 1j, 1 + 1j, 0.2 + 1j]:
            self.play(s_tracker.animate.set_value(z), run_time=6)

        # Talk again about the left plane
        full_plane = Rectangle().set_stroke(width=0).set_fill(RED, 0.5)
        full_plane.replace(s_plane, stretch=True)
        full_plane.set_fill(GREEN, 0.5)

        left_plane = full_plane.copy()
        left_plane.set_fill(RED, 0.5)
        left_plane.stretch(0.5, 0, about_edge=LEFT)
        left_plane.save_state()
        left_plane.stretch(0, 0, about_edge=RIGHT)

        equation_rect = SurroundingRectangle(int_equation)
        equation_rect.set_stroke(YELLOW, 2)
        equation_rect.fix_in_frame()

        self.play(
            Restore(left_plane),
            frame.animate.reorient(-36, 79, 4, (7.71, 2.4, 1.86), 15.36),
            run_time=3
        )
        self.wait()
        self.play(ShowCreation(equation_rect))
        self.wait()
        self.play(equation_rect.animate.surround(int_equation[R"\frac{1}{s}"], buff=SMALL_BUFF))
        self.wait()
        self.play(
            ReplacementTransform(left_plane, full_plane)
        )
        self.wait()

        # Describe continuation
        lhs_rect = SurroundingRectangle(int_equation[:-4])
        rhs_rect = SurroundingRectangle(int_equation[-3:])
        VGroup(lhs_rect, rhs_rect).fix_in_frame().set_stroke(YELLOW, 2)

        def pole_func(s):
            if s != 0:
                return 1.0 / s
            return 100

        extended_graph = get_complex_graph(s_plane, pole_func)
        extended_mesh = SurfaceMesh(extended_graph, resolution=(21, 21))
        extended_mesh.remove(*(line for line in extended_mesh if line.get_z(IN) < 0))
        extended_mesh.set_stroke(WHITE, 0.5, 0.15)
        extended_mesh.shift(1e-2 * OUT)

        self.add(extended_graph, graph, extended_mesh, mesh)
        self.play(
            FadeOut(graph, 1e-2 * IN),
            FadeIn(extended_graph),
            FadeOut(mesh),
            FadeIn(extended_mesh),
            frame.animate.reorient(0, 85, 0, (5.32, 3.46, 3.69), 13.49).set_anim_args(run_time=5),
            FadeOut(full_plane),
        )
        self.play(
            frame.animate.reorient(-17, 62, 9, (6.29, -0.4, 3.75), 13.87),
            FadeOut(equation_rect),
            run_time=5
        )
        curr_s = complex(get_s())
        self.play(
            UpdateFromAlphaFunc(s_tracker, lambda m, a: m.set_value(curr_s * np.exp(a * TAU * 1j))),
            run_time=30,
        )
        self.wait()

        # Discuss pole (Mostly with overlays)
        self.play(
            frame.animate.reorient(-36, 83, 1, (5.84, -1.06, 3.19), 10.63),
            s_tracker.animate.set_value(0.1 + 0.1j),
            run_time=20
        )
        self.play(
            frame.animate.reorient(0, 0, 0, (1.95, 0.95, -0.0), 15.34),
            s_tracker.animate.set_value(1e-3).set_anim_args(time_span=(0, 5)),
            extended_mesh.animate.set_stroke(opacity=0),
            VFadeOut(int_vect, time_span=(0, 7)),
            run_time=10,
        )
        self.play(frame.animate.reorient(0, 83, 0, (5.18, 4.04, 3.15), 14.50), run_time=10)

    def get_s_group(self):
        s_plane = self.get_s_plane()
        s_plane.set_width(6)
        s_plane.to_corner(DL)
        s_plane.axes.set_stroke(width=1)

        s_dot, s_label = self.get_s_dot_and_label(s_plane, get_s=self.s_tracker.get_value)
        s_plane_label = Tex(R"s", t2c=self.tex_to_color_map, font_size=72)
        s_plane_label.next_to(s_plane, UP)

        s_group = Group(s_plane, s_dot, s_label, s_plane_label)
        return s_group

    def get_output_path(self, plane, func, t_min=0, t_max=20, stroke_color=TEAL, stroke_width=2, step_size=1e-1):
        return ParametricCurve(
            lambda t: plane.n2p(func(t)),
            t_range=[t_min, t_max, step_size],
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )

    def get_vector(self, plane, value, backstroke_width=2, **kwargs):
        vect = Arrow(plane.n2p(0), plane.n2p(value), buff=0, **kwargs)
        vect.set_backstroke(BLACK, width=backstroke_width)
        return vect

    def get_mean_vector(self, plane, func, t_min, t_max, thickness=3, fill_color=RED, n_samples=1000, **kwargs):
        x_range = np.linspace(t_min, t_max, n_samples)
        x_mean = np.mean(func(x_range))
        return self.get_vector(plane, x_mean, thickness=thickness, fill_color=fill_color, **kwargs)
        return vect

    def get_sample_dots(self, subpath, n_samples=20, radius=0.05, glow_factor=0.5, color=RED):
        return DotCloud(
            [subpath.pfp(a) for a in np.linspace(0, 1, n_samples)],
            radius=radius,
            glow_factor=glow_factor,
            color=color
        )

    def get_dynamic_output_path(self, plane, func, stroke_width=3, step_size=1e-2):
        t_range = list(range(0, self.t_max))
        t_samples = [np.arange(t, t + 1 + step_size, step_size) for t in t_range]
        path = VGroup(VMobject() for t in t_range)

        def update_path(path):
            for piece, samples in zip(path, t_samples):
                piece.set_points_as_corners(plane.n2p(func(samples)))
            return path

        path.add_updater(update_path)
        for piece, color in zip(path, it.cycle(self.staggered_path_colors)):
            piece.set_stroke(color, stroke_width)

        return path

    def get_dynamic_vector_sum(self, plane, func, thickness=1, backstroke_width=0, n_samples=100, border_width=0.5):
        t_range = list(range(0, self.t_max))
        vects = VGroup(
            self.get_vector(
                plane, 1,
                thickness=thickness,
                backstroke_width=backstroke_width,
                fill_color=color,
            )
            for t, color in zip(t_range, it.cycle(self.staggered_path_colors))
        )
        vects.set_fill(border_width=border_width)
        t_samples = [np.linspace(t, t + 1, n_samples) for t in t_range]

        def update_vects(vects):
            avg_values = [0] + [func(samples).mean() for samples in t_samples]
            end_values = np.cumsum(avg_values)
            end_points = plane.n2p(end_values)
            for vect, p0, p1 in zip(vects, end_points, end_points[1:]):
                vect.put_start_and_end_on(p0, p1)
            return vect

        vects.add_updater(update_vects)

        return vects


class BreakDownLaplaceTransform(IntegrateComplexExponential):
    func_tex = R"e^{1.5 {t}}"
    initial_s = 2 + 1j
    s_plane_x_range = (-3, 3)
    s_label_font_size = 24
    t_max = 100  # For dynamic path and vector sum.  Change to 100 for final render
    # pole_value = 1.5
    pole_value = -0.2 + 1.5j

    def construct(self):
        self.add_core_pieces()

        frame = self.frame
        s_tracker = self.s_tracker
        exp_plane, int_plane = self.output_planes

        # Talk through the parts
        frame.reorient(0, 52, 0, (-0.69, 0.41, 0.56), 10.93)
        int_rect = SurroundingRectangle(int_plane.label)
        int_rect.set_stroke(YELLOW, 2)
        int_rect.fix_in_frame()

        self.play(
            frame.animate.reorient(20, 68, 0, (-0.45, 0.24, 0.17), 6.28),
            s_tracker.animate.set_value(1.6 - 1j),
            ShowCreation(int_rect, time_span=(4, 5)),
            run_time=8
        )
        self.play(int_rect.animate.surround(exp_plane.label))
        self.draw_upper_plot(draw_time=8)
        self.play(
            s_tracker.animate.set_value(1.6),
            frame.animate.reorient(24, 65, 0, (-0.35, 1.85, 1.61), 11.20),
            run_time=5
        )
        self.play(
            s_tracker.animate.set_value(1.501),
            run_time=5
        )

        # Alternate pan to pole
        self.clear()
        to_add = Group(self.s_group, self.graph_tracer, self.graph)
        to_add.shift(-self.s_group[0].n2p(0))
        self.add(to_add)

        frame.reorient(-35, 84, 0, (-1.14, 1.42, 4.73), 14.55)
        self.s_tracker.set_value(1 + 1j)
        self.play(
            frame.animate.reorient(0, 43, 0, (-0.42, 0.6, 2.1), 9.91),
            self.s_tracker.animate.set_value(1.5001),
            run_time=10
        )

    def add_core_pieces(self):
        # Planes and their contenst
        s_group = self.get_s_group()
        s_plane = s_group[0]
        s_plane.faded_lines.set_opacity(0)

        output_planes = self.get_output_planes()
        exp_plane, int_plane = output_planes

        right_rect = FullScreenRectangle()
        right_rect.set_fill(BLACK, 1)
        right_rect.set_width(RIGHT_SIDE[0] - output_planes.get_left()[0] + SMALL_BUFF, stretch=True, about_edge=RIGHT)

        # Dynamic pieces
        output_path = self.get_dynamic_output_path(exp_plane, self.inner_func)
        vect_sum = self.get_dynamic_vector_sum(int_plane, self.inner_func)
        integral_vect = self.get_integral_vect(int_plane)

        for mob in [output_path, vect_sum, integral_vect]:
            mob.set_clip_plane(RIGHT, -exp_plane.get_x(LEFT))

        graph_tracer = self.get_graph_tracer(s_plane)

        graph = get_complex_graph(s_plane, self.transformed_func)

        # Add everything
        right_group = VGroup(right_rect, output_planes, output_path, vect_sum)
        right_group.fix_in_frame()
        right_group.set_scale_stroke_with_zoom(True)

        self.add(
            s_group,
            graph_tracer,
            graph,
            right_rect,
            output_planes,
            output_path,
            vect_sum,
            integral_vect,
        )

        self.s_group = s_group
        self.output_planes = output_planes
        self.output_path = output_path
        self.vect_sum = vect_sum
        self.integral_vect = integral_vect
        self.graph_tracer = graph_tracer
        self.graph = graph

    def get_integral_vect(self, int_plane):
        vect = Vector(RIGHT, fill_color=WHITE, thickness=2)
        dot = GlowDot(color=PINK)
        origin = int_plane.n2p(0)

        vect.add_updater(lambda m: m.put_start_and_end_on(
            origin, int_plane.n2p(self.transformed_func(self.s_tracker.get_value()))
        ))
        dot.f_always.move_to(vect.get_end)

        group = Group(vect, dot)
        group.fix_in_frame()
        return group

    def get_graph_tracer(self, s_plane):
        v_line = Line(ORIGIN, OUT).set_stroke(WHITE, 3)
        graph_dot = Group(TrueDot(), GlowDot())
        graph_dot.set_color(TEAL)

        group = Group(v_line, graph_dot)
        s_plane_unit = s_plane.x_axis.get_unit_size()

        def update_tracer(group):
            s = self.s_tracker.get_value()
            s_point = s_plane.n2p(s)
            int_value = self.transformed_func(s)

            line, dot = group
            line.put_start_and_end_on(s_point, s_point + s_plane_unit * abs(int_value) * OUT)
            dot.move_to(line.get_end())

        group.add_updater(update_tracer)
        return group

    def get_output_planes(self, width=3, edge_buff=2.5):
        exp_plane = self.get_exp_plane(x_range=(-1, 1))
        exp_plane.set_width(width)
        exp_plane.axes.set_stroke(width=1)
        exp_plane.to_corner(UP, MED_LARGE_BUFF)
        exp_plane.to_edge(RIGHT, buff=edge_buff)

        int_plane = self.get_exp_plane()
        int_plane.set_width(width)
        int_plane.move_to(exp_plane).to_edge(DOWN)
        int_plane.axes.set_stroke(width=1)
        int_plane.add_coordinate_labels(font_size=12)

        kw = dict(t2c=self.tex_to_color_map)
        exp_plane.label = Tex(self.func_tex, R"e^{\minus {s} {t}}", **kw)
        exp_plane.label.next_to(exp_plane, RIGHT, aligned_edge=UP)

        int_plane.label = Tex(R"\int^\infty_0 " + self.func_tex + R"e^{\minus {s} {t}} d{t}", **kw)
        int_plane.label.scale(0.6)
        int_plane.label.next_to(int_plane, RIGHT, aligned_edge=UP)

        planes = VGroup(exp_plane, int_plane)
        for plane in planes:
            plane.add(plane.label)

        return planes

    def func(self, t):
        return np.exp(1.5 * t)

    def inner_func(self, t):
        return self.func(t) * np.exp(-self.s_tracker.get_value() * t)

    def transformed_func(self, s):
        return np.divide(1.0, (s - self.pole_value))

    def draw_upper_plot(self, draw_time=12, rate_multiple=2):
        exp_plane = self.output_planes[0]
        n_pieces = int(rate_multiple * draw_time)
        path_copy = VMobject()
        path_copy.fix_in_frame()
        path_copy.start_new_path(self.output_path[0].get_start())
        for part in self.output_path[:n_pieces]:
            path_copy.append_vectorized_mobject(part)

        tracing_vect = Vector(fill_color=YELLOW)
        tracing_vect.add_updater(lambda m: m.put_start_and_end_on(
            exp_plane.n2p(0),
            path_copy.get_end(),
        ))
        tracing_vect.fix_in_frame()

        vect_sum_copy = self.vect_sum.copy()[:n_pieces]
        vect_sum_copy.clear_updaters()
        self.remove(self.output_path, self.vect_sum, self.integral_vect)

        self.add(tracing_vect)
        self.play(
            ShowCreation(path_copy),
            ShowIncreasingSubsets(self.vect_sum[:n_pieces], int_func=np.ceil),
            run_time=draw_time,
            rate_func=linear
        )
        self.remove(path_copy, tracing_vect)
        self.add(self.output_path, self.vect_sum, self.integral_vect)
        self.wait()

    def show_simple_pole(self):
        # Clean the board
        frame = self.frame
        for line in self.graph[1]:
            if line.get_z(OUT) > 100 or line.get_z(IN) < -100:
                line.set_stroke(opacity=0)
        self.clear()
        self.add(self.s_group, self.graph, self.graph_tracer)
        self.graph_tracer[0].set_stroke(width=1)

        # Move
        frame.reorient(-30, 83, 0, (-4.35, 1.2, 2.52), 11.47)
        self.play(
            frame.animate.reorient(0, 0, 0, (-5.17, -0.19, 0.0), 9.88).set_field_of_view(20 * DEG),
            self.s_tracker.animate.set_value(self.pole_value + 1e-5),
            run_time=10
        )
        self.wait()
