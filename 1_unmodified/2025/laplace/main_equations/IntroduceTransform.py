# ==============================================================================
# Scene:      IntroduceTransform
# Source:     videos/_2025/laplace/main_equations.py (lines 672-1273)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/exponentials.py, _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl IntroduceTransform.py IntroduceTransform -w -m --fps 15
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



# ----- From _2025/laplace/main_equations.py -----

class IntroduceTransform(SPlane):
    long_ambient_graph_display = False

    def construct(self):
        # Write "Laplace Transform"
        text = Text("Laplace Transform", font_size=72)
        laplace_word = text["Laplace"][0]
        transform_word = text["Transform"][0]
        laplace_transform_word = VGroup(laplace_word, transform_word)
        transform_word_rect = SurroundingRectangle(transform_word, buff=SMALL_BUFF)
        randy = Randolph().flip()
        randy.next_to(laplace_transform_word, DR)
        q_marks = Tex(R"???", font_size=72).space_out_submobjects(1.5)
        q_marks.next_to(transform_word_rect, UP)
        q_marks.set_color(YELLOW)

        self.add(laplace_transform_word)
        self.wait()
        self.play(LaggedStart(
            VFadeIn(randy),
            randy.change("confused", transform_word),
            ShowCreation(transform_word_rect),
            laplace_word.animate.set_opacity(0.5),
            LaggedStartMap(FadeIn, q_marks, shift=0.5 * UP, lag_ratio=0.25),
            lag_ratio=0.1
        ))
        self.wait()

        # Show a function with an arrow
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        name_group = VGroup(laplace_transform_word, transform_word_rect, q_marks)
        name_group.target = name_group.generate_target(use_deepcopy=True)
        name_group.target[2].set_fill(opacity=0).move_to(transform_word_rect)
        name_group.target.scale(0.5).to_edge(UP)
        name_group.target[1].set_stroke(width=0)

        mapsto = Tex(R"\xmapsto{\qquad}", additional_preamble=R"\usepackage{mathtools}")
        mapsto.rotate(-90 * DEG)
        mapsto.set_fill(border_width=2)

        t_mob, _, ft_mob = func_group = VGroup(Tex(R"{t}", t2c=t2c), mapsto, Tex(R"f({t})", t2c=t2c))
        func_group.arrange(DOWN)
        func_name = Text("function")
        func_name.next_to(mapsto, LEFT, SMALL_BUFF)

        mapsto.save_state()
        mapsto.stretch(0, 1, about_edge=UP).set_fill(opacity=0)

        self.play(
            MoveToTarget(name_group),
            randy.change("pondering", func_group),
            FadeIn(func_name, lag_ratio=0.1),
        )
        self.play(
            Restore(mapsto),
            FadeIn(t_mob, 0.1 * UP)
        )
        self.play(LaggedStart(
            TransformFromCopy(t_mob, ft_mob[2], path_arc=45 * DEG, run_time=1),
            FadeTransform(func_name[0].copy(), ft_mob[0], path_arc=45 * DEG, run_time=1),
            Write(ft_mob[1::2]),
            lag_ratio=0.25,
        ))
        self.wait()

        # Show the meta-notion
        func_group.generate_target()
        func_group.target.arrange(DOWN)
        func_group.target.move_to(4 * LEFT)

        braces = VGroup(
            Brace(func_group.target, direction, SMALL_BUFF).scale(1.25, about_point=func_group.target.get_center())
            for direction in [LEFT, RIGHT]
        )
        braces.save_state()
        braces.set_opacity(0)
        for brace in braces:
            brace.replace(func_group, dim_to_match=1)

        short_func_name = Tex(R"f")
        short_func_name.next_to(func_group.target[1], LEFT, buff=0)

        right_arrow = Vector(3 * RIGHT, thickness=6)
        right_arrow.next_to(braces.saved_state, RIGHT, MED_LARGE_BUFF)

        self.play(LaggedStart(
            MoveToTarget(func_group),
            Restore(braces),
            LaggedStart(
                [FadeTransform(func_name[0], short_func_name)] + [
                    char.animate.set_opacity(0).replace(short_func_name)
                    for char in func_name[1:]
                ],
                lag_ratio=0.02,
                remover=True
            ),
            GrowArrow(right_arrow),
            lag_ratio=0.05
        ))
        self.play(transform_word.animate.scale(1.5).next_to(right_arrow, UP))
        self.play(Blink(randy))
        self.wait()

        # Show output function
        f_group = VGroup(braces, t_mob, short_func_name, mapsto, ft_mob)
        F_braces, s_mob, F_mob, right_mapsto, Fs_mob = F_group = VGroup(
            braces.copy(),
            Tex(R"{s}", t2c=t2c),
            Tex(R"F"),
            mapsto.copy(),
            Tex(R"F({s})", t2c=t2c),
        )
        for mob1, mob2 in zip(f_group, F_group):
            mob2.move_to(mob1)
        F_group[2].shift(SMALL_BUFF * LEFT)

        F_group.next_to(right_arrow, RIGHT, MED_LARGE_BUFF)

        self.play(
            LaggedStart(
                (TransformFromCopy(*pair, path_arc=-60 * DEG)
                for pair in zip(f_group, F_group)),
                lag_ratio=0.025,
                # run_time=1.5
                run_time=8
            ),
            randy.change("tease").scale(0.75).to_corner(DR),
        )
        self.wait()

        # Talk through parts
        rect = SurroundingRectangle(F_group[-1]["F"], buff=0.05)
        rect.set_stroke(RED, 3)
        vect = Vector(0.5 * UP, thickness=4)
        vect.set_color(RED)
        vect.next_to(rect, DOWN, SMALL_BUFF)

        self.play(laplace_word.animate.set_fill(opacity=1).scale(1.5).next_to(transform_word, UP, MED_SMALL_BUFF, LEFT))
        self.play(
            ShowCreation(rect),
            GrowArrow(vect),
            randy.change("pondering", rect),
        )
        self.wait()
        self.play(
            rect.animate.surround(f_group[-1][0], buff=0.05),
            MaintainPositionRelativeTo(vect, rect),
        )
        self.wait()
        self.play(Blink(randy))
        self.play(
            rect.animate.surround(f_group[1], buff=0.05).set_anim_args(path_arc=-90 * DEG),
            vect.animate.rotate(PI).next_to(f_group[1], UP, SMALL_BUFF).set_anim_args(path_arc=-90 * DEG),
        )
        self.wait()
        self.play(
            rect.animate.surround(F_group[1], buff=0.05).set_anim_args(path_arc=-90 * DEG),
            MaintainPositionRelativeTo(vect, rect),
            randy.animate.look_at(F_group),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(vect), FadeOut(rect))

        # Show Laplace Transform expression
        lt_def = Tex(R"\int^\infty_0 f({t}) e^{\minus {s}{t}} d{t}", t2c=t2c)
        lt_def.move_to(Fs_mob, LEFT)
        new_interior = VGroup(s_mob, F_mob, right_mapsto, lt_def)
        F_braces.generate_target()
        F_braces.target.set_height(new_interior.get_height() + MED_LARGE_BUFF, stretch=True)
        F_braces.target.match_y(right_arrow)
        F_braces.target[1].next_to(new_interior, RIGHT).match_y(F_braces.target[0])

        q_marks = Tex(R"???").set_color(YELLOW)
        q_marks.next_to(randy, UP, SMALL_BUFF).shift(0.25 * RIGHT + 0.5 * DOWN)

        self.play(
            FadeOut(Fs_mob),
            Write(lt_def),
            randy.change("pleading").scale(0.75, about_edge=DR),
            FadeIn(q_marks, 0.1 * UP, lag_ratio=0.1),
            MoveToTarget(F_braces),
            new_interior[:3].animate.match_x(lt_def).shift(0.1 * UP),
        )
        self.play(Blink(randy))
        self.wait()

        # Discuss expression
        rect = SurroundingRectangle(lt_def)
        rect.set_stroke(YELLOW, 2)

        s_vect = Vector(0.25 * DOWN)
        s_vect.set_fill(YELLOW)
        s_vect.next_to(lt_def["{s}"][0], UP, SMALL_BUFF)

        self.play(
            ShowCreation(rect),
            randy.change('confused')
        )
        self.wait()
        self.play(
            Transform(rect, s_vect.copy().match_style(rect)),
            FadeIn(s_vect, time_span=(0.75, 1)),
        )
        self.play(
            randy.change("pondering", s_vect),
            FadeOut(q_marks),
            FadeOut(rect),
        )
        self.play(Blink(randy))
        self.wait()

        # Show F(s) left hand side
        F_lhs = Tex(R"F({s}) = ", t2c=t2c)
        F_lhs.move_to(lt_def, LEFT)

        right_shift = F_lhs.get_width() * RIGHT

        self.play(
            TransformFromCopy(s_mob, F_lhs["{s}"][0]),
            TransformFromCopy(F_mob, F_lhs["F"][0]),
            Write(F_lhs[re.compile(r"\(|\)|=")]),
            lt_def.animate.shift(right_shift),
            MaintainPositionRelativeTo(s_vect, lt_def),
            F_braces[1].animate.shift(right_shift),
            new_interior[:3].animate.shift(right_shift + 0.1 * UP),
            randy.animate.shift(0.5 * DOWN),
            self.frame.animate.shift(0.5 * DOWN),
        )

        # Reference the naming convention
        F_rect = SurroundingRectangle(F_lhs[0], buff=0.05)
        F_rect.set_stroke(RED, 2)

        self.play(
            ShowCreation(F_rect),
            s_vect.animate.next_to(F_rect, UP, SMALL_BUFF).set_color(RED)
        )
        self.wait()
        self.play(
            F_rect.animate.surround(ft_mob[0], buff=0.05),
            s_vect.animate.next_to(ft_mob[0], UP, SMALL_BUFF),
            randy.animate.look_at(ft_mob)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(F_rect), FadeOut(s_vect))

        # Clear the board
        lt_group = VGroup(F_lhs, lt_def)

        self.remove(lt_group)
        everything = Group(*self.get_mobjects())
        everything.sort(lambda p: np.dot(p, UL))

        self.play(
            LaggedStartMap(FadeOut, everything, shift=0.1 * DOWN, lag_ratio=0.1),
            lt_group.animate.center().set_height(2),
            self.frame.animate.to_default_state(),
            run_time=2,
        )

        # Highlight inner part
        outer_part = VGroup(lt_def[R"\int^\infty_0"][0], lt_def[R"d{t}"][0])
        inner_part = lt_def[R"f({t}) e^{\minus {s}{t}}"][0]

        rect = SurroundingRectangle(inner_part, buff=SMALL_BUFF)
        outer_rects = VGroup(SurroundingRectangle(piece, buff=SMALL_BUFF) for piece in outer_part)
        VGroup(rect, outer_rects).set_stroke(RED, 2)

        self.play(
            ShowCreation(rect),
            outer_part.animate.set_fill(opacity=0.2),
            F_lhs.animate.set_fill(opacity=0.2),
        )
        self.wait()
        self.play(
            # TransformFromCopy(rect.replicate(2), outer_rects),
            rect.animate.surround(outer_part, buff=SMALL_BUFF),
            outer_part.animate.set_fill(opacity=1),
            inner_part.animate.set_fill(opacity=0.5),
        )
        self.wait()

        # Put at the top
        lt_group = VGroup(F_lhs, outer_part, inner_part)
        lt_group.target = lt_group.generate_target()
        lt_group.target.set_height(1.2).to_edge(UP, buff=MED_SMALL_BUFF)
        lt_group.target[:2].set_fill(opacity=0.2)
        lt_group.target[2].set_fill(opacity=1)

        lt_group.target.set_fill(opacity=1)

        self.play(
            MoveToTarget(lt_group),
            # rect.animate.surround(lt_group.target[2]).set_stroke(width=1),
            rect.animate.surround(lt_group.target).set_stroke(width=0),
        )
        self.wait()
        self.play(
            rect.animate.surround(lt_def["s"][0], buff=0.05).set_stroke(YELLOW)
        )
        self.wait()

        # Show s as a complex number
        plane = ComplexPlane((-3, 3), (-3, 3))
        plane.next_to(lt_group, DOWN)
        plane.add_coordinate_labels(font_size=16)

        s_dot = Group(TrueDot(), GlowDot()).set_color(YELLOW)
        s_dot.move_to(plane.n2p(2 + 1j))
        s_label = Tex(R"s").set_color(YELLOW)
        s_label.always.next_to(s_dot[0], UR, SMALL_BUFF)

        self.play(
            Write(plane, lag_ratio=1e-2),
            TransformFromCopy(lt_def["s"][0], s_label),
            FadeInFromPoint(s_dot, rect.get_center()),
            FadeOut(rect),
        )
        self.wait()

        # Wander
        final_z = -2 + 1j
        n_iterations = 12
        for n in range(12):
            z = complex(*np.random.uniform(-3, 3, 2))
            if n == n_iterations - 1:
                z = final_z
            self.play(s_dot.animate.move_to(plane.n2p(z)).set_anim_args(path_arc=45 * DEG))
            self.wait()

        # Plug in cos(t)
        lt_def.refresh_bounding_box()
        lt_of_cos = Tex(lt_def.get_tex().replace("f({t})", R"\cos({t})"), t2c=t2c)
        lt_of_cos.move_to(lt_def, LEFT)
        cos_lt_group = VGroup(
            F_lhs,
            VGroup(lt_of_cos[R"\int^\infty_0"][0], lt_of_cos[R"d{t}"][0]),
            lt_of_cos[R"\cos({t}) e^{\minus {s}{t}}"][0]
        )
        cos_lt_group[1].set_fill(opacity=0.2)

        imag_circles = VGroup(
            Dot(plane.n2p(z)).set_stroke(YELLOW, 1).set_fill(opacity=0.25)
            for z in [1j, -1j]
        )

        f_term = lt_def["f"][-1]
        cos_term = lt_of_cos[R"\cos"][0]
        f_rect = SurroundingRectangle(f_term, buff=0.05)
        f_rect.set_stroke(PINK, 2)

        self.play(ShowCreation(f_rect))
        self.play(
            TransformMatchingTex(
                lt_def,
                lt_of_cos,
                matched_pairs=[(f_term, cos_term)],
                run_time=1
            ),
            f_rect.animate.surround(cos_term, buff=0.05),
            F_lhs.animate.shift((lt_of_cos.get_width() - lt_def.get_width()) * 0.5 * LEFT),
            *map(ShowCreation, imag_circles),
        )
        self.play(FadeOut(f_rect))
        self.wait()

        # Create the graph
        frame = self.frame
        frame.to_default_state()
        cos_lt_group.fix_in_frame()
        self.add(cos_lt_group)

        graph = get_complex_graph(
            plane,
            lambda s: s / (s**2 + 1),
            resolution=(501, 501),
            mesh_resolution=(31, 31)
        )
        graph.stretch(0.25, 2, about_point=plane.n2p(0))

        # Show the graph
        self.play(
            cos_lt_group.animate.to_edge(LEFT, buff=MED_SMALL_BUFF).set_fill(opacity=1),
            ShowCreation(graph[0]),
            Write(graph[1], stroke_width=1, time_span=(2, 4)),
            frame.animate.reorient(-28, 74, 0, OUT, 8.37),
            run_time=4,
        )
        frame.clear_updaters()
        frame.add_ambient_rotation()
        for z in [1j, -1j]:
            self.play(s_dot.animate.move_to(plane.n2p(z)), run_time=2)
            self.wait(2)

        # Long ambient graph rotation (one branch here)
        if self.long_ambient_graph_display:
            self.remove(cos_lt_group)
            self.wait(19)
            self.add(imag_circles, graph)
            self.play(FadeOut(graph), FadeOut(imag_circles))
            frame.clear_updaters()
            s_plane = plane
            s_plane.save_state()
            s_plane.set_height(3.5)
            s_plane.to_corner(UR, buff=MED_SMALL_BUFF).shift(LEFT)
            s_plane.background_lines.set_stroke(BLUE, 1, 1)
            s_plane.target = s_plane.copy()

            s_dot.target = s_dot.generate_target()
            s_dot.target.move_to(s_plane.n2p(0.2 + 2j))

            s_plane.restore()
            self.play(
                frame.animate.to_default_state(),
                MoveToTarget(s_plane),
                MoveToTarget(s_dot),
                run_time=2
            )

        # Remove graphs
        self.remove(plane, graph, s_dot, s_label, imag_circles)
        frame.to_default_state()
        frame.clear_updaters()

        # Ignore the integral
        interior = cos_lt_group[2]
        interior_rect = SurroundingRectangle(interior, buff=0.05)
        interior_rect.set_stroke(TEAL, 2)

        self.add(interior)
        self.play(
            ShowCreation(interior_rect),
            cos_lt_group[:2].animate.set_fill(opacity=0.2),
        )
        self.wait()

        # Replace break down cos(t) with exponentials
        arrow = Vector(DOWN)
        arrow.match_color(interior_rect)
        arrow.next_to(interior_rect, DOWN, SMALL_BUFF)
        expanded = Tex(
            R"\frac{1}{2} \left(e^{i{t}} + e^{\minus i{t}} \right) e^{\minus{s}{t}}",
            t2c={"i": WHITE, "-i": WHITE, **t2c},
        )
        expanded.next_to(arrow, DOWN, MED_LARGE_BUFF)
        expanded_brace = Brace(expanded, UP, SMALL_BUFF)
        expanded_brace.set_color(TEAL)

        index = -4
        self.play(
            FadeTransform(interior[:index].copy(), expanded[:index]),
            TransformFromCopy(interior[index:], expanded[index:]),
            GrowArrow(arrow),
            FadeInFromPoint(expanded_brace, arrow.get_start()),
        )
        self.wait()

        # Focus on just part
        eit, est = pair = VGroup(expanded["e^{i{t}}"][0], expanded[R"e^{\minus{s}{t}}"][0])
        pair_rects = VGroup(SurroundingRectangle(p, buff=0.05) for p in pair)
        pair_rects.set_stroke(BLUE, 2)
        pair_copy = pair.copy()

        self.add(pair_copy),
        self.play(
            expanded.animate.set_fill(opacity=0.5),
            ShowCreation(pair_rects, lag_ratio=0.5)
        )
        self.wait()

        # Combine
        combined_term = Tex(R"e^{(i - {s}){t}}", t2c=t2c)
        combined_term.next_to(pair, DOWN, LARGE_BUFF)
        comb_arrows = VGroup(Arrow(p, combined_term, buff=0.25, thickness=2) for p in pair)
        comb_arrows.set_fill(BLUE)

        self.play(
            TransformMatchingShapes(pair.copy(), combined_term),
            *map(GrowArrow, comb_arrows),
            run_time=1
        )
        self.wait()

        # Pull up s-plane and output plane
        s_plane = plane
        s_plane.set_height(3.5)
        s_plane.to_corner(UR, buff=MED_SMALL_BUFF).shift(LEFT)
        s_plane.background_lines.set_stroke(BLUE, 1, 1)

        s_tracker = ComplexValueTracker(0.2 + 2j)
        t_tracker = ValueTracker(0)
        get_s = s_tracker.get_value
        get_t = t_tracker.get_value

        def get_ims():
            return 1j - get_s()

        s_dot.add_updater(lambda m: m.move_to(s_plane.n2p(get_s())))

        exp_plane = self.get_exp_plane()
        exp_plane.set_height(3.5)
        exp_plane.next_to(s_plane, DOWN, MED_LARGE_BUFF)
        output_label = self.get_output_dot_and_label(
            exp_plane,
            get_s=get_ims,
            get_t=get_t,
            s_tex="(i - {s})"
        )
        output_path = self.get_output_path(exp_plane, get_t, get_ims)

        self.play(FadeIn(s_plane), FadeIn(s_dot), FadeIn(s_label))
        self.play(
            FadeIn(exp_plane),
            FadeTransform(combined_term.copy(), output_label[1]),
            FadeIn(output_label[0]),
        )
        self.add(output_path)
        self.play(t_tracker.animate.set_value(2 * TAU), rate_func=linear, run_time=10)
        self.play(s_tracker.animate.increment_value(-0.3), rate_func=there_and_back, run_time=4)
        self.play(s_tracker.animate.set_value(0.2), run_time=4)
        self.play(s_tracker.animate.set_value(1j), run_time=4)
        self.wait()

        # Let t play
        eq_i_rhs = Tex(R"= i")
        eq_i_rhs.next_to(s_label, RIGHT, SMALL_BUFF).shift(0.04 * UP)
        self.play(Write(eq_i_rhs), run_time=1)

        t_tracker.set_value(0)
        self.play(t_tracker.animate.set_value(20), run_time=20, rate_func=linear)

        # Show s = i
        down_arrow = Vector(0.75 * DOWN)
        down_arrow.next_to(combined_term, DOWN, SMALL_BUFF)
        arrow_label = Tex(R"{s} = i", font_size=24, t2c=t2c)
        arrow_label.next_to(down_arrow, RIGHT, buff=0)
        const = Tex(R"e^{0{t}}", t2c=t2c)
        const.next_to(down_arrow, DOWN, SMALL_BUFF)
        eq_1 = Tex(R"= 1")
        eq_1.next_to(const, RIGHT, SMALL_BUFF, aligned_edge=DOWN)

        self.play(
            GrowArrow(down_arrow),
            FadeIn(arrow_label),
            FadeIn(const, DOWN),
        )
        self.wait()
        self.play(Write(eq_1, run_time=1))
        self.wait()

        # Move around s
        s_tracker.clear_updaters()
        t_tracker.set_value(100)
        output_label.clear_updaters()

        self.play(
            FadeOut(eq_i_rhs),
            FadeOut(output_label),
        )

        self.play()
        for _ in range(6):
            self.play(
                s_tracker.animate.set_value(complex(random.uniform(-0.1, 0.5), random.uniform(-3, 3))),
                run_time=2
            )
            self.wait()
        self.play(s_tracker.animate.set_value(1j), run_time=2)
        self.remove(output_path)

        self.wait()

        # State the goal
        big_rect = SurroundingRectangle(expanded[:-4])
        big_rect.set_stroke(BLUE, 2)
        goal = Text("Goal:\nReveal these terms", alignment="LEFT")
        goal.next_to(big_rect, DOWN, aligned_edge=LEFT)

        self.play(
            ReplacementTransform(pair_rects, VGroup(big_rect)),
            LaggedStartMap(FadeOut, VGroup(comb_arrows, combined_term, down_arrow, arrow_label, const, eq_1)),
            FadeOut(Group(exp_plane, s_plane, s_label, s_dot)),
            expanded.animate.set_fill(opacity=1),
        )
        self.play(FadeIn(goal, lag_ratio=0.1))
        self.wait()
        self.play(
            FadeOut(goal),
            big_rect.animate.surround(expanded),
        )
        self.wait()

        # Highlight the integral again
        self.add(expanded)
        self.remove(pair_copy)
        self.play(
            LaggedStartMap(FadeOut, VGroup(interior_rect, arrow, expanded_brace, expanded, big_rect)),
            cos_lt_group.animate.set_fill(opacity=1),
        )
        self.wait()
