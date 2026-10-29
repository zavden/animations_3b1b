# ==============================================================================
# Scene:      AlternateBreakDown
# Source:     videos/_2025/laplace/main_equations.py (lines 2199-2276)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/exponentials.py, _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl AlternateBreakDown.py AlternateBreakDown -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/exponentials.py -----

def get_exp_graph_icon(s, t_range=(0, 7), y_max=4, pos_real_scalar=0.1, neg_real_scalar=0.2, width=1, height=1):
    axes = Axes(
        t_range,
        (-y_max, y_max),
        width=width,
        height=height,
        axis_config=dict(tick_size=0.035, stroke_width=1)
    )
    scalar = pos_real_scalar if s.real > 0 else neg_real_scalar
    new_s = complex(s.real * scalar, s.imag)
    graph = axes.get_graph(lambda t: np.exp(new_s * t).real)
    graph.set_stroke(YELLOW, 2)
    rect = SurroundingRectangle(axes)
    rect.set_fill(BLACK, 1)
    rect.set_stroke(WHITE, 1)
    return VGroup(rect, axes, graph)



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

class TranslateToNewLanguage(InteractiveScene):
    graph_resolution = (301, 301)
    show_integral = True
    label_config = dict(
        font_size=72,
        t2c={"{t}": BLUE, "{s}": YELLOW}
    )

    def construct(self):
        # Set up a functions
        full_s_samples = self.get_s_samples()
        func_s_samples = [
            complex(-2, 2),
            complex(-2, -2),
            complex(0, 1),  # Changed
            complex(-1, 0),
            complex(0, -1),  # Changed
        ]
        func_weights = [-1, -1, 1j, 2, -1j]

        def func(t):
            return sum([
                (weight * np.exp(complex(0.1 * s.real, s.imag) * t)).real
                for s, weight in zip(func_s_samples, func_weights)
            ])

        # Graph
        axes, graph, graph_label = self.get_graph_group(func)

        # Show the S-plane pieces
        frame = self.frame
        frame.set_y(0.5)
        s_plane, exp_pieces, s_plane_name = self.get_s_plane_and_exp_pieces(full_s_samples)

        self.play(LaggedStart(
            FadeIn(axes),
            ShowCreation(graph),
            FadeIn(graph_label),
            FadeIn(s_plane_name, lag_ratio=0.1),
            LaggedStartMap(FadeIn, exp_pieces, lag_ratio=0.1),
        ))
        self.wait()

        # Narrow down specific pieces
        exp_pieces.save_state()
        exp_pieces.generate_target()
        key_pieces = VGroup()
        for piece, s_sample in zip(exp_pieces.target, full_s_samples):
            if s_sample not in func_s_samples:
                piece.fade(0.7)
            else:
                key_pieces.add(piece)

        weight_labels = VGroup(
            Tex(Rf"\times {w}", font_size=24).next_to(piece.get_top(), DOWN, SMALL_BUFF)
            for w, piece in zip([R"\minus 1", R"\minus 1", R"\minus i", "2", "i"], key_pieces)
        )
        self.play(
            MoveToTarget(exp_pieces),
            LaggedStartMap(FadeIn, weight_labels),
        )
        self.play(LaggedStart(
            (Transform(graph.copy(), piece[-1].copy().insert_n_curves(100), remover=True)
            for piece in key_pieces),
            lag_ratio=0.1,
            group_type=Group,
            run_time=2
        ))
        self.wait()

        # Reveal plane
        frame = self.frame
        arrow, fancy_L, Fs_label = self.get_arrow_to_Fs(graph_label)
        Fs_label.save_state()
        Fs_label.become(graph_label)

        def Func(s):
            result = sum([
                np.divide(w, (s - s0))
                for s0, w in zip(func_s_samples, func_weights)
            ])
            return min(100, result)

        lt_graph = get_complex_graph(s_plane, Func, resolution=self.graph_resolution)
        lt_graph.stretch(0.25, 2, about_point=s_plane.n2p(0))
        lt_graph.save_state()
        lt_graph.stretch(0, 2, about_point=s_plane.n2p(0))
        lt_graph.set_opacity(0)

        exp_pieces.target = exp_pieces.saved_state.copy()
        for piece in exp_pieces.target:
            piece.scale(0.35)

        self.add(exp_pieces, lt_graph, graph_label, arrow, Fs_label, Point(), weight_labels)
        self.play(
            FadeOut(s_plane_name),
            GrowArrow(arrow),
            Write(fancy_L),
            Restore(Fs_label, time_span=(1, 2), path_arc=-10 * DEG),
            FadeIn(s_plane),
            MoveToTarget(exp_pieces, lag_ratio=1e-3),
            FadeOut(weight_labels),
            Restore(lt_graph, time_span=(1.5, 3)),
            frame.animate.reorient(70, 86, 0, (-4.94, -2.45, 3.51), 19.43),
            run_time=3
        )

        # Show interal and continuation
        if self.show_integral:
            # For an insertion
            integral = Tex(R"= \int^\infty_0 f({t})e^{\minus{s}{t}}d{t}", t2c=self.label_config["t2c"])
            integral.fix_in_frame()
            integral.next_to(Fs_label, RIGHT)
            integral.set_backstroke(BLACK, 5)
            rect = BackgroundRectangle(VGroup(Fs_label, integral))
            rect.set_fill(BLACK, 0.8)
            rect.scale(2, about_edge=DL)
            rect.shift(0.25 * DOWN)

            graph_copy = lt_graph[0].copy()
            graph_copy.set_clip_plane(RIGHT, -s_plane.get_left()[0])
            graph_copy.fade(0.5)

            self.add(rect, Fs_label, integral)
            self.play(
                FadeIn(rect),
                Write(integral, run_time=1)
            )
            self.wait()
            lt_graph.set_clip_plane(RIGHT, s_plane.get_left()[0])
            self.play(
                frame.animate.reorient(-10, 85, 0, (-2.18, 0.45, 3.12), 11.52),
                lt_graph.animate.set_clip_plane(RIGHT, -s_plane.n2p(0)[0]),
                run_time=3
            )
            self.play(
                frame.animate.reorient(33, 85, 0, (-1.81, 0.13, 2.44), 12.25),
                run_time=6
            )
            self.wait()
            self.add(graph_copy, rect, Fs_label, integral)
            self.play(
                FadeOut(rect),
                ShowCreation(graph_copy),
                frame.animate.reorient(-2, 67, 0, (-0.95, -0.06, 1.91), 9.45),
                run_time=8
            )

            # Show key exponentials below poles
            for piece in key_pieces:
                piece.set_height(1)
            self.add(key_pieces, graph_copy, graph)
            self.play(
                frame.animate.reorient(0, 0, 0, (-1.23, 1.49, 1.9), 9.36),
                FadeIn(key_pieces),
                exp_pieces.animate.fade(0.5),
                run_time=3,
            )

        # Reorient
        self.play(frame.animate.reorient(-39, 90, 0, (-1.37, 1.1, 4.12), 10.93), run_time=15)
        self.play(frame.animate.reorient(0, 0, 0, (-2.13, 0.07, 2.2), 9.79), run_time=10)
        self.play(frame.animate.reorient(84, 87, 0, (-4.22, -3.48, 5.26), 22.43), run_time=10)

        # Poles as lines
        pole_lines = VGroup(
            Line(s_plane.n2p(s), s_plane.n2p(s) + 20 * OUT)
            for s in func_s_samples
        )
        pole_lines.set_stroke(WHITE, 3)

        key_pieces.target = key_pieces.generate_target()
        target_rects = VGroup()
        for piece in key_pieces.target:
            piece.set_height(1.2)
            target_rect = piece[0].copy()
            target_rect.set_fill(opacity=0)
            target_rects.add(target_rect)

        self.add(pole_lines, key_pieces, lt_graph)
        self.play(
            ShowCreation(pole_lines, lag_ratio=0.1),
        )
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.98, 0.82, 0.0), 10.00),
            lt_graph[0].animate.set_opacity(0.2),
            lt_graph[1].animate.set_opacity(0.05),
            pole_lines.animate.stretch(0, 2, about_edge=IN),
            MoveToTarget(key_pieces),
            FadeIn(weight_labels),
            run_time=3,
        )
        self.wait()

        # Shift things down
        top_rect = FullScreenRectangle()
        top_rect.set_fill(BLACK, 1).set_stroke(width=0)
        top_rect.set_height(2.5, about_edge=UP, stretch=True)
        top_rect.fix_in_frame()

        h_line = DashedLine(top_rect.get_corner(DL), top_rect.get_corner(DR))
        h_line.set_stroke(WHITE, 1)
        h_line.fix_in_frame()

        top_rect.save_state()
        top_rect.stretch(0, 1, about_edge=UP)

        self.play(
            Restore(top_rect),
            ShowCreation(h_line, time_span=(1, 2)),
            VGroup(axes, graph).animate.shift(2 * DOWN),
            VGroup(graph_label, arrow, fancy_L, Fs_label).animate.shift(3 * DOWN),
            frame.animate.reorient(-17, 90, 0, (-2.86, 1.57, 3.14), 10.95),
            run_time=2
        )
        self.play(frame.animate.reorient(39, 92, 0, (-4.35, 0.64, 3.03), 14.99), run_time=20)

    def get_graph_group(self, func, func_tex=R"f({t})"):
        # axes = Axes((0, 7), (-4, 4), width=0.5 * FRAME_WIDTH - 1, height=5)
        axes = Axes((0, 8), (-1, 6, 0.5), width=0.3 * FRAME_WIDTH - 1, height=7)
        axes.to_edge(LEFT).shift(0.5 * DOWN)
        graph = axes.get_graph(func)
        graph.set_stroke(BLUE, 5)
        graph.set_scale_stroke_with_zoom(True)
        axes.set_scale_stroke_with_zoom(True)
        graph_label = Tex(func_tex, **self.label_config)
        graph_label.move_to(axes).to_edge(UP, buff=LARGE_BUFF)

        graph_group = VGroup(axes, graph, graph_label)
        graph_group.fix_in_frame()
        return graph_group

    def get_s_samples(self):
        return [complex(a, b) for a in range(-2, 3) for b in range(-2, 3)]

    def get_s_plane_and_exp_pieces(self, s_samples):
        s_plane = ComplexPlane((-3, 3), (-3, 3))
        s_plane.set_height(7.5)
        s_plane.move_to(3.75 * RIGHT)
        s_plane.set_z_index(-1)

        exp_pieces = VGroup(
            self.get_exp_graph(s).move_to(s_plane.n2p(s))
            for s in s_samples
        )
        s_plane_name = Text("S-plane", font_size=72)
        s_plane_name.next_to(exp_pieces, UP, MED_SMALL_BUFF)
        return s_plane, exp_pieces, s_plane_name

    def get_arrow_to_Fs(self, graph_label):
        arrow = Vector(2 * RIGHT, thickness=5, fill_color=WHITE)
        arrow.fix_in_frame()
        arrow.next_to(graph_label, RIGHT, buff=MED_LARGE_BUFF)

        fancy_L = Tex(R"\mathcal{L}", font_size=60)
        fancy_L.next_to(arrow, UP, buff=0)
        fancy_L.fix_in_frame()

        Fs_label = Tex(R"F({s})", **self.label_config)
        Fs_label.next_to(arrow, RIGHT, MED_LARGE_BUFF)
        Fs_label.fix_in_frame()
        Fs_label.set_z_index(1)
        Fs_label.set_backstroke(BLACK, 5)

        return VGroup(arrow, fancy_L, Fs_label)

    def get_exp_graph(self, s, **kwargs):
        return get_exp_graph_icon(s, **kwargs)


class AlternateBreakDown(TranslateToNewLanguage):
    def construct(self):
        # Set up
        axes, graph, graph_label = self.get_graph_group(
            lambda t: 0.35 * t**2,
            func_tex=R"f({t}) = {t}^2"
        )
        graph_label.set_backstroke(BLACK, 8)
        s_samples = self.get_s_samples()
        s_plane, exp_pieces, s_plane_name = self.get_s_plane_and_exp_pieces(s_samples)
        arrow, fancy_L, Fs_label = self.get_arrow_to_Fs(graph_label)

        self.add(axes, graph, graph_label)
        self.add(exp_pieces)

        # Note equal to a sum
        ne = Tex(R"\ne", font_size=96)
        ne.next_to(graph_label, RIGHT, MED_LARGE_BUFF)
        ne.set_color(RED)
        sum_tex = Tex(
            R"\sum_{n=1}^N c_n e^{s_n t}",
            t2c={"s_n": YELLOW, "c_n": GREY_A},
            font_size=72,
        )
        sum_tex.next_to(ne, RIGHT)
        ne_rhs = VGroup(ne, sum_tex)

        self.play(LaggedStart(
            FadeIn(ne, scale=2),
            Write(sum_tex),
            exp_pieces.animate.scale(0.7, about_edge=DR),
            lag_ratio=0.2
        ))
        self.wait()

        # Show transform
        self.play(
            LaggedStart(
                FadeOut(graph_label[4:]),
                graph_label[:4].animate.next_to(arrow, LEFT),
                GrowArrow(arrow),
                Write(fancy_L),
                TransformFromCopy(graph_label, Fs_label, path_arc=20 * DEG),
                lag_ratio=0.05
            ),
            FadeOut(ne_rhs, DOWN, scale=0.5),
        )
        self.wait()

        # Show integral
        inv_lt = Tex(
            R"f({t}) = \frac{1}{2\pi i} \int_\gamma F({s}) e^{{s}{t}} d{s}",
            t2c=self.label_config["t2c"]
        )
        inv_lt.next_to(arrow, DOWN, LARGE_BUFF)

        s_plane.replace(exp_pieces)
        s_plane.add_coordinate_labels(font_size=12)
        line = Line(s_plane.get_bottom(), s_plane.get_top())
        line.shift(RIGHT)
        line.set_stroke(YELLOW, 2)
        line.insert_n_curves(20)

        self.play(
            TransformFromCopy(graph_label[:4], inv_lt[:4]),
            TransformFromCopy(Fs_label, inv_lt["F({s})"][0]),
            Write(inv_lt[4:]),
        )
        self.play(
            FadeIn(s_plane),
            LaggedStartMap(FadeOut, exp_pieces, scale=0.1),
        )
        self.play(
            VShowPassingFlash(line.copy()),
            ShowCreation(line),
            run_time=5
        )
        self.wait()
