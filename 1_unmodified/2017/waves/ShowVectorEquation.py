# ==============================================================================
# Scene:      ShowVectorEquation
# Source:     videos/_2017/waves.py (lines 1124-1548)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowVectorEquation.py ShowVectorEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


E_COLOR = BLUE


class OscillatingVector(ContinualAnimation):
    CONFIG = {
        "tail" : ORIGIN,
        "frequency" : 1,
        "A_vect" : [1, 0, 0],
        "phi_vect" : [0, 0, 0],
        "vector_to_be_added_to" : None,
    }
    def setup(self):
        self.vector = self.mobject

    def update_mobject(self, dt):
        f = self.frequency
        t = self.internal_time
        angle = 2*np.pi*f*t
        vect = np.array([
            A*np.exp(complex(0, angle + phi))
            for A, phi in zip(self.A_vect, self.phi_vect)
        ]).real
        self.update_tail()
        self.vector.put_start_and_end_on(self.tail, self.tail+vect)

    def update_tail(self):
        if self.vector_to_be_added_to is not None:
            self.tail = self.vector_to_be_added_to.get_end()


class ShowVectorEquation(Scene):
    CONFIG = {
        "f_color" : RED,
        "phi_color" : MAROON_B,
        "A_color" : GREEN,
    }
    def construct(self):
        self.add_vector()
        self.add_plane()
        self.write_horizontally_polarized()
        self.write_components()
        self.show_graph()
        self.add_phi()
        self.add_amplitude()
        self.add_kets()
        self.switch_to_vertically_polarized_light()

    def add_vector(self):
        self.vector = Vector(2*RIGHT, color = E_COLOR)
        self.oscillating_vector = OscillatingVector(
            self.vector,
            A_vect = [2, 0, 0],
            frequency = 0.25,
        )
        self.add(self.oscillating_vector)
        self.wait(3)

    def add_plane(self):
        xy_plane = NumberPlane(
            axes_color = GREY_B,
            color = GREY_D,
            secondary_color = GREY_D,
            x_unit_size = 2,
            y_unit_size = 2,
        )
        xy_plane.add_coordinates()
        xy_plane.add(xy_plane.get_axis_labels())

        self.play(
            Write(xy_plane),
            Animation(self.vector)
        )
        self.wait(2)
        self.xy_plane = xy_plane

    def write_horizontally_polarized(self):
        words = OldTexText(
            "``", "Horizontally", " polarized", "''",
            arg_separator = ""
        )
        words.next_to(ORIGIN, LEFT)
        words.to_edge(UP)
        words.add_background_rectangle()

        self.play(Write(words, run_time = 3))
        self.wait()

        self.horizontally_polarized_words = words

    def write_components(self):
        x, y = components = VGroup(
            OldTex("\\cos(", "2\\pi", "f_x", "t", "+ ", "\\phi_x", ")"),
            OldTex("0", "")
        )
        components.arrange(DOWN)
        lb, rb = brackets = OldTex("[]")
        brackets.set_height(components.get_height() + SMALL_BUFF)
        lb.next_to(components, LEFT, buff = 0.3)
        rb.next_to(components, RIGHT, buff = 0.3)
        E, equals = E_equals = OldTex(
            "\\vec{\\textbf{E}}", "="
        )
        E.set_color(E_COLOR)
        E_equals.next_to(brackets, LEFT)
        E_equals.add_background_rectangle()
        brackets.add_background_rectangle()
        group = VGroup(E_equals, brackets, components)
        group.next_to(
            self.horizontally_polarized_words, 
            DOWN, MED_LARGE_BUFF, RIGHT
        )

        x_without_phi = OldTex("\\cos(", "2\\pi", "f_x", "t", ")")
        x_without_phi.move_to(x)
        for mob in x, x_without_phi:
            mob.set_color_by_tex_to_color_map({
                "f_x" : self.f_color,
                "phi_x" : self.phi_color,
            })

        def update_brace(brace):
            brace.stretch_to_fit_width(
                max(self.vector.get_width(), 0.001)
            )
            brace.next_to(self.vector.get_center(), DOWN, SMALL_BUFF)
            return brace
        moving_brace = Mobject.add_updater(
            Brace(Line(LEFT, RIGHT), DOWN), update_brace
        )
        moving_x_without_phi = Mobject.add_updater(
            x_without_phi.copy().add_background_rectangle(),
            lambda m : m.next_to(moving_brace.mobject, DOWN, SMALL_BUFF)
        )

        self.play(Write(E_equals), Write(brackets))
        y.save_state()
        y.move_to(self.horizontally_polarized_words)
        y.set_fill(opacity = 0)
        self.play(y.restore)
        self.wait()
        self.add(moving_brace, moving_x_without_phi)
        self.play(
            FadeIn(moving_brace.mobject),
            FadeIn(x_without_phi),
            FadeIn(moving_x_without_phi.mobject),
            lag_ratio = 0.5,
            run_time = 2,
        )
        self.wait(3)
        self.play(
            FadeOut(moving_brace.mobject),
            FadeOut(moving_x_without_phi.mobject),
        )
        self.remove(moving_brace, moving_x_without_phi)

        self.E_equals = E_equals
        self.brackets = brackets
        self.x_without_phi = x_without_phi
        self.components = components

    def show_graph(self):
        axes = Axes(
            x_min = -0.5,
            x_max = 5.2,
            y_min = -1.5,
            y_max = 1.5,
        )
        axes.x_axis.add_numbers(*list(range(1, 6)))
        t = OldTex("t")
        t.next_to(axes.x_axis, UP, SMALL_BUFF, RIGHT)
        cos = self.x_without_phi.copy()
        cos.next_to(axes.y_axis, RIGHT, SMALL_BUFF, UP)
        cos_arg = VGroup(*cos[1:-1])
        fx_equals_1 = OldTex("f_x", "= 1")
        fx_equals_fourth = OldTex("f_x", "= 0.25")
        fx_group = VGroup(fx_equals_1, fx_equals_fourth)
        for fx in fx_group:
            fx[0].set_color(self.f_color)
            fx.move_to(axes, UP+RIGHT)
        high_f_graph, low_f_graph = graphs = VGroup(*[
            FunctionGraph(
                lambda x : np.cos(2*np.pi*f*x),
                color = E_COLOR,
                x_min = 0,
                x_max = 4/f,
                num_steps = 20/f,
            )
            for f in (1, 0.25,)
        ])

        group = VGroup(axes, t, cos, high_f_graph, *fx_group)
        rect = SurroundingRectangle(
            group,
            buff = MED_LARGE_BUFF,
            stroke_color = WHITE,
            stroke_width = 3,
            fill_color = BLACK,
            fill_opacity = 0.9
        )
        group.add_to_back(rect)
        group.scale(0.8)
        group.to_corner(UP+RIGHT, buff = -SMALL_BUFF)
        group.remove(*it.chain(fx_group, graphs))
        low_f_graph.scale(0.8)
        low_f_graph.move_to(high_f_graph, LEFT)

        cos_arg_rect = SurroundingRectangle(cos_arg)

        new_ov = OscillatingVector(
            Vector(RIGHT, color = E_COLOR),
            A_vect = [2, 0, 0],
            frequency = 1,
            start_up_time = 0,
        )

        self.play(FadeIn(group))
        self.play(
            ReplacementTransform(
                self.components[0].get_part_by_tex("f_x").copy(),
                fx_equals_1
            ),
        )
        self.wait(4 - (self.oscillating_vector.internal_time%4))
        self.remove(self.oscillating_vector)
        self.add(new_ov)
        self.play(ShowCreation(
            high_f_graph, run_time = 4,
            rate_func=linear,
        ))
        self.wait()
        self.play(FadeOut(new_ov.vector))
        self.remove(new_ov)
        self.add(self.oscillating_vector)
        self.play(
            ReplacementTransform(*fx_group),
            ReplacementTransform(*graphs),
            FadeOut(new_ov.vector),
            FadeIn(self.vector)
        )
        self.wait(4)
        self.play(ShowCreation(cos_arg_rect))
        self.play(FadeOut(cos_arg_rect))
        self.wait(5)

        self.corner_group = group
        self.fx_equals_fourth = fx_equals_fourth
        self.corner_cos = cos
        self.low_f_graph = low_f_graph
        self.graph_axes = axes

    def add_phi(self):
        corner_cos = self.corner_cos
        corner_phi = OldTex("+", "\\phi_x")
        corner_phi.set_color_by_tex("phi", self.phi_color)
        corner_phi.scale(0.8)
        corner_phi.next_to(corner_cos[-2], RIGHT, SMALL_BUFF)

        x, y = self.components
        x_without_phi = self.x_without_phi

        words = OldTexText("``Phase shift''")
        words.next_to(ORIGIN, UP+LEFT)
        words.set_color(self.phi_color)
        words.add_background_rectangle()
        arrow = Arrow(words.get_top(), x[-2])
        arrow.set_color(WHITE)

        self.play(
            ReplacementTransform(
                VGroup(*x_without_phi[:-1]),
                VGroup(*x[:-3]),
            ),
            ReplacementTransform(x_without_phi[-1], x[-1]),
            Write(VGroup(*x[-3:-1])),
            corner_cos[-1].next_to, corner_phi.copy(), RIGHT, SMALL_BUFF,
            Write(corner_phi),
            FadeOut(self.fx_equals_fourth),
        )
        self.play(self.low_f_graph.shift, MED_LARGE_BUFF*LEFT)
        self.play(
            Write(words, run_time = 1),
            ShowCreation(arrow)
        )
        self.wait(3)
        self.play(*list(map(FadeOut, [words, arrow])))

        self.corner_cos.add(corner_phi)

    def add_amplitude(self):
        x, y = self.components
        corner_cos = self.corner_cos
        graph = self.low_f_graph
        graph_y_axis = self.graph_axes.y_axis

        A = OldTex("A_x")
        A.set_color(self.A_color)
        A.move_to(x.get_left())
        corner_A = A.copy()
        corner_A.scale(0.8)
        corner_A.move_to(corner_cos, LEFT)

        h_brace = Brace(Line(ORIGIN, 2*RIGHT), UP)
        v_brace = Brace(Line(
            graph_y_axis.number_to_point(0),
            graph_y_axis.number_to_point(1),
        ), LEFT, buff = SMALL_BUFF)
        for brace in h_brace, v_brace:
            brace.A = brace.get_tex("A_x")
            brace.A.set_color(self.A_color)
        v_brace.A.scale(0.5, about_point = v_brace.get_center())
        all_As = VGroup(A, corner_A, h_brace.A, v_brace.A)

        def update_vect(vect):
            self.oscillating_vector.A_vect[0] = h_brace.get_width()
            return vect

        self.play(
            GrowFromCenter(h_brace),
            GrowFromCenter(v_brace),
        )
        self.wait(2)
        self.play(
            x.next_to, A, RIGHT, SMALL_BUFF,
            corner_cos.next_to, corner_A, RIGHT, SMALL_BUFF,
            FadeIn(all_As)
        )
        x.add(A)
        corner_cos.add(corner_A)
        self.wait()
        factor = 0.5
        self.play(
            v_brace.stretch_in_place, factor, 1,
            v_brace.move_to, v_brace.copy(), DOWN,
            MaintainPositionRelativeTo(v_brace.A, v_brace),
            h_brace.stretch_in_place, factor, 0,
            h_brace.move_to, h_brace.copy(), LEFT,
            MaintainPositionRelativeTo(h_brace.A, h_brace),
            UpdateFromFunc(self.vector, update_vect),
            graph.stretch_in_place, factor, 1,
        )
        self.wait(4)

        self.h_brace = h_brace 
        self.v_brace = v_brace

    def add_kets(self):
        x, y = self.components
        E_equals = self.E_equals
        for mob in x, y, E_equals:
            mob.add_background_rectangle()
            mob.generate_target()

        right_ket = OldTex("|\\rightarrow\\rangle")
        up_ket = OldTex("|\\uparrow\\rangle")
        kets = VGroup(right_ket, up_ket)
        kets.set_color(YELLOW)
        for ket in kets:
            ket.add_background_rectangle()
        plus = OldTexText("+")
        group = VGroup(
            E_equals.target, 
            x.target, right_ket, plus,
            y.target, up_ket,
        )
        group.arrange(RIGHT)
        E_equals.target.shift(SMALL_BUFF*UP)
        group.scale(0.8)
        group.move_to(self.brackets, DOWN)
        group.to_edge(LEFT, buff = MED_SMALL_BUFF)

        kets_word = OldTexText("``kets''")
        kets_word.next_to(kets, DOWN, buff = 0.8)
        arrows = VGroup(*[
            Arrow(kets_word.get_top(), ket, color = ket.get_color())
            for ket in kets
        ])
        ket_rects = VGroup(*list(map(SurroundingRectangle, kets)))
        ket_rects.set_color(WHITE)
        unit_vectors = VGroup(*[Vector(2*vect) for vect in (RIGHT, UP)])
        unit_vectors.set_fill(YELLOW)

        self.play(
            FadeOut(self.brackets),
            *list(map(MoveToTarget, [E_equals, x, y]))
        )
        self.play(*list(map(Write, [right_ket, plus, up_ket])), run_time = 1)
        self.play(
            Write(kets_word),
            LaggedStartMap(ShowCreation, arrows, lag_ratio = 0.7),
            run_time = 2,
        )
        self.wait()
        for ket, ket_rect, unit_vect in zip(kets, ket_rects, unit_vectors):
            self.play(ShowCreation(ket_rect))
            self.play(FadeOut(ket_rect))
            self.play(ReplacementTransform(ket[1][1].copy(), unit_vect))
            self.wait()
        self.play(FadeOut(unit_vectors))
        self.play(*list(map(FadeOut, [kets_word, arrows])))

        self.kets = kets
        self.plus = plus

    def switch_to_vertically_polarized_light(self):
        x, y = self.components
        x_ket, y_ket = self.kets
        plus = self.plus

        x.target = OldTex("0", "").add_background_rectangle()
        y.target = OldTex(
            "A_y", "\\cos(", "2\\pi", "f_y", "t", "+", "\\phi_y", ")"
        )
        y.target.set_color_by_tex_to_color_map({
            "A" : self.A_color,            
            "f" : self.f_color,
            "phi" : self.phi_color,
        })
        y.target.add_background_rectangle()
        VGroup(x.target, y.target).scale(0.8)
        for mob in [plus] + list(self.kets):
            mob.generate_target()

        movers = x, x_ket, plus, y, y_ket
        group = VGroup(*[m.target for m in movers])
        group.arrange(RIGHT)
        group.move_to(x, LEFT)

        vector_A_vect = np.array(self.oscillating_vector.A_vect)
        def update_vect(vect, alpha):
            self.oscillating_vector.A_vect = rotate_vector(
                vector_A_vect, alpha*np.pi/2
            )
            return vect

        new_h_brace = Brace(Line(ORIGIN, UP), RIGHT)

        words = OldTexText(
            "``", "Vertically", " polarized", "''",
            arg_separator = "",
        )
        words.add_background_rectangle()
        words.move_to(self.horizontally_polarized_words)

        self.play(
            UpdateFromAlphaFunc(self.vector, update_vect),
            Transform(self.h_brace, new_h_brace),
            self.h_brace.A.next_to, new_h_brace, RIGHT, SMALL_BUFF,
            Transform(self.horizontally_polarized_words, words),
            *list(map(FadeOut, [
                self.corner_group, self.v_brace, 
                self.v_brace.A, self.low_f_graph,
            ]))
        )
        self.play(*list(map(MoveToTarget, movers)))
        self.wait(5)
