# ==============================================================================
# Scene:      ShowTipToTailSum
# Source:     videos/_2017/waves.py (lines 1618-1884)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowTipToTailSum.py ShowTipToTailSum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo replaced mob.update with the updater function; GL update(dt, frame_rate) is a real method, so the function is kept as line_updater
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


class ShowTipToTailSum(ShowVectorEquation):
    def construct(self):
        self.force_skipping()
        self.add_vector()
        self.add_plane()
        self.add_vertial_vector()
        self.revert_to_original_skipping_status()

        self.add_kets()
        self.show_vector_sum()
        self.write_superposition()
        self.add_amplitudes()
        self.add_phase_shift()

    def add_vertial_vector(self):
        self.h_vector = self.vector
        self.h_oscillating_vector = self.oscillating_vector
        self.h_oscillating_vector.start_up_time = 0

        self.v_oscillating_vector = self.h_oscillating_vector.copy()
        self.v_vector = self.v_oscillating_vector.vector
        self.v_oscillating_vector.A_vect = [0, 2, 0]
        self.v_oscillating_vector.update(0)

        self.d_oscillating_vector = Mobject.add_updater(
            Vector(UP+RIGHT, color = E_COLOR),
            lambda v : v.put_start_and_end_on(
                ORIGIN,
                self.v_vector.get_end()+ self.h_vector.get_end(),
            )
        )
        self.d_vector = self.d_oscillating_vector.mobject
        self.d_oscillating_vector.update(0)

        self.add(self.v_oscillating_vector)
        self.add_foreground_mobject(self.v_vector)

    def add_kets(self):
        h_ket, v_ket = kets = VGroup(*[
            OldTex(
                "\\cos(", "2\\pi", "f", "t", ")",
                "|\\!\\%sarrow\\rangle"%s
            )
            for s in ("right", "up")
        ])
        for ket in kets:
            ket.set_color_by_tex_to_color_map({
                "f" : self.f_color,    
                "rangle" : YELLOW,
            })
            ket.add_background_rectangle(opacity = 1)
            ket.scale(0.8)

        h_ket.next_to(2*RIGHT, UP, SMALL_BUFF)
        v_ket.next_to(2*UP, UP, SMALL_BUFF)
        self.add_foreground_mobject(kets)

        self.kets = kets

    def show_vector_sum(self):
        h_line = DashedLine(ORIGIN, 2*RIGHT)
        v_line = DashedLine(ORIGIN, 2*UP)

        # CHANGE: Cairo replaced mob.update with the updater function; GL update(dt, frame_rate) is a real method, so the function is kept as line_updater
        h_line.line_updater = self.generate_dashed_line_update(
            self.h_vector, self.v_vector
        )
        # CHANGE: Cairo replaced mob.update with the updater function; GL update(dt, frame_rate) is a real method, so the function is kept as line_updater
        v_line.line_updater = self.generate_dashed_line_update(
            self.v_vector, self.h_vector
        )

        h_ket, v_ket = self.kets
        for ket in self.kets:
            ket.generate_target()
        plus = OldTex("+")
        ket_sum = VGroup(h_ket.target, plus, v_ket.target)
        ket_sum.arrange(RIGHT)
        ket_sum.next_to(3*RIGHT + 2*UP, UP, SMALL_BUFF)

        self.wait(4)
        self.remove(self.h_oscillating_vector, self.v_oscillating_vector)
        self.add(self.h_vector, self.v_vector)
        h_line.update(h_line)
        v_line.update(v_line)
        self.play(*it.chain(
            list(map(MoveToTarget, self.kets)),
            [Write(plus)],
            list(map(ShowCreation, [h_line, v_line])),
        ))
        blue_black = average_color(BLUE, BLACK)
        self.play(
            GrowFromPoint(self.d_vector, ORIGIN),
            self.h_vector.set_fill, blue_black,
            self.v_vector.set_fill, blue_black,
        )
        self.wait()
        self.add(
            self.h_oscillating_vector,
            self.v_oscillating_vector,
            self.d_oscillating_vector,
            Mobject.add_updater(h_line, h_line.line_updater),
            Mobject.add_updater(v_line, v_line.line_updater),
        )
        self.wait(4)

        self.ket_sum = VGroup(h_ket, plus, v_ket)

    def write_superposition(self):
        superposition_words = OldTexText(
            "``Superposition''", "of",
            "$|\\!\\rightarrow\\rangle$", "and", 
            "$|\\!\\uparrow\\rangle$",
        )
        superposition_words.scale(0.8)
        superposition_words.set_color_by_tex("rangle", YELLOW)
        superposition_words.add_background_rectangle()
        superposition_words.to_corner(UP+LEFT)
        ket_sum = self.ket_sum
        ket_sum.generate_target()
        ket_sum.target.move_to(superposition_words)
        ket_sum.target.align_to(ket_sum, UP)

        sum_word = OldTexText("", "Sum")
        weighted_sum_word = OldTexText("Weighted", "sum")
        for word in sum_word, weighted_sum_word:
            word.scale(0.8)
            word.set_color(GREEN)
            word.add_background_rectangle()
            word.move_to(superposition_words.get_part_by_tex("Super"))

        self.play(
            Write(superposition_words, run_time = 2),
            MoveToTarget(ket_sum)
        )
        self.wait(2)
        self.play(
            FadeIn(sum_word),
            superposition_words.shift, MED_LARGE_BUFF*DOWN,
            ket_sum.shift, MED_LARGE_BUFF*DOWN,
        )
        self.wait()
        self.play(ReplacementTransform(
            sum_word, weighted_sum_word
        ))
        self.wait(2)

    def add_amplitudes(self):
        h_ket, plus, r_ket = self.ket_sum
        for mob in self.ket_sum:
            mob.generate_target()
        h_A, v_A = 2, 0.5
        h_A_mob, v_A_mob = A_mobs = VGroup(*[
            OldTex(str(A)).add_background_rectangle()
            for A in [h_A, v_A]
        ])
        A_mobs.scale(0.8)
        A_mobs.set_color(GREEN)
        h_A_mob.move_to(h_ket, LEFT)
        VGroup(h_ket.target, plus.target).next_to(
            h_A_mob, RIGHT, SMALL_BUFF
        )
        v_A_mob.next_to(plus.target, RIGHT, SMALL_BUFF)
        r_ket.target.next_to(v_A_mob, RIGHT, SMALL_BUFF)
        A_mobs.shift(0.4*SMALL_BUFF*UP)

        h_ov = self.h_oscillating_vector
        v_ov = self.v_oscillating_vector


        self.play(*it.chain(
            list(map(MoveToTarget, self.ket_sum)),
            list(map(Write, A_mobs)),
            [
                UpdateFromAlphaFunc(
                    ov.vector,
                    self.generate_A_update(
                        ov, 
                        A*np.array(ov.A_vect), 
                        np.array(ov.A_vect)
                    )
                )
                for ov, A in [(h_ov, h_A), (v_ov, v_A)]
            ]
        ))
        self.wait(4)

        self.A_mobs = A_mobs

    def add_phase_shift(self):
        h_ket, plus, v_ket = self.ket_sum

        plus_phi = OldTex("+", "\\pi/2")
        plus_phi.set_color_by_tex("pi", self.phi_color)
        plus_phi.scale(0.8)
        plus_phi.next_to(v_ket.get_part_by_tex("t"), RIGHT, SMALL_BUFF)
        v_ket.generate_target()
        VGroup(*v_ket.target[1][-2:]).next_to(plus_phi, RIGHT, SMALL_BUFF)
        v_ket.target[0].replace(v_ket.target[1])


        h_ov = self.h_oscillating_vector
        v_ov = self.v_oscillating_vector

        ellipse = Circle()
        ellipse.stretch_to_fit_height(2)
        ellipse.stretch_to_fit_width(8)
        ellipse.set_color(self.phi_color)

        h_A_mob, v_A_mob = self.A_mobs
        new_h_A_mob = v_A_mob.copy()
        new_h_A_mob.move_to(h_A_mob, RIGHT)

        self.add_foreground_mobject(plus_phi)
        self.play(
            MoveToTarget(v_ket),
            Write(plus_phi),
            UpdateFromAlphaFunc(
                v_ov.vector,
                self.generate_phi_update(
                    v_ov, 
                    np.array([0, np.pi/2, 0]), 
                    np.array(v_ov.phi_vect)
                )
            )
        )
        self.play(FadeIn(ellipse))
        self.wait(5)
        self.play(
            UpdateFromAlphaFunc(
                h_ov.vector,
                self.generate_A_update(
                    h_ov, 
                    0.25*np.array(h_ov.A_vect), 
                    np.array(h_ov.A_vect),
                )
            ),
            ellipse.stretch, 0.25, 0,
            Transform(h_A_mob, new_h_A_mob)
        )
        self.wait(8)

    #####

    def generate_A_update(self, ov, A_vect, prev_A_vect):
        def update(vect, alpha):
            ov.A_vect = interpolate(
                np.array(prev_A_vect),
                A_vect,
                alpha
            )
            return vect
        return update

    def generate_phi_update(self, ov, phi_vect, prev_phi_vect):
        def update(vect, alpha):
            ov.phi_vect = interpolate(
                prev_phi_vect, phi_vect, alpha
            )
            return vect
        return update

    def generate_dashed_line_update(self, v1, v2):
        def update_line(line):
            line.put_start_and_end_on_with_projection(
                *v1.get_start_and_end()
            )
            line.shift(v2.get_end() - line.get_start())
        return update_line
