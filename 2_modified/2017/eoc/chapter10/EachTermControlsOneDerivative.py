# ==============================================================================
# Scene:      EachTermControlsOneDerivative
# Source:     videos/_2017/eoc/chapter10.py (lines 1844-1889)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EachTermControlsOneDerivative.py EachTermControlsOneDerivative -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow.CONFIG does not exist in GL (Cairo Arrow tip_length default was 0.25)
# ==============================================================================

from manim_imports_ext import *

def derivative(func, x, n = 1, dx = 0.01):
    samples = [func(x + (k - n/2)*dx) for k in range(n+1)]
    while len(samples) > 1:
        samples = [
            (s_plus_dx - s)/dx
            for s, s_plus_dx in zip(samples, samples[1:])
        ]
    return samples[0]


def taylor_approximation(func, highest_term, center_point = 0):
    derivatives = [
        derivative(func, center_point, n = n)
        for n in range(highest_term + 1)
    ]
    coefficients = [
        d/math.factorial(n) 
        for n, d in enumerate(derivatives)
    ]
    return lambda x : sum([
        c*((x-center_point)**n) 
        for n, c in enumerate(coefficients)
    ])


class ExampleApproximation(GraphScene):
    CONFIG = {
        "function" : lambda x : np.exp(-x**2),
        "function_tex" : "e^{-x^2}", 
        "function_color" : BLUE,
        "order_sequence" : [0, 2, 4],
        "center_point" : 0,
        "approximation_terms" : ["1 ", "-x^2", "+\\frac{1}{2}x^4"],
        "approximation_color" : GREEN,
        "x_min" : -3,
        "x_max" : 3,
        "y_min" : -1,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }
    def construct(self):
        self.setup_axes()
        func_graph = self.get_graph(
            self.function,
            self.function_color,
        )
        approx_graphs = [
            self.get_graph(
                taylor_approximation(self.function, n),
                self.approximation_color
            )
            for n in self.order_sequence
        ]

        near_text = OldTexText(
            "Near %s $= %d$"%(
                self.x_axis_label, self.center_point
            )
        )
        near_text.to_corner(UP + RIGHT)
        near_text.add_background_rectangle()
        equation = OldTex(
            self.function_tex, 
            "\\approx",
            *self.approximation_terms
        )
        equation.next_to(near_text, DOWN, MED_LARGE_BUFF)
        equation.to_edge(RIGHT)
        near_text.next_to(equation, UP, MED_LARGE_BUFF)
        equation.set_color_by_tex(
            self.function_tex, self.function_color,
            substring = False
        )
        approx_terms = VGroup(*[
            equation.get_part_by_tex(tex, substring = False)
            for tex in self.approximation_terms
        ])
        approx_terms.set_fill(
            self.approximation_color,
            opacity = 0,
        )
        equation.add_background_rectangle()

        approx_graph = VectorizedPoint(
            self.input_to_graph_point(self.center_point, func_graph)
        )

        self.play(
            ShowCreation(func_graph, run_time = 2),
            Animation(equation),
            Animation(near_text),
        )
        for graph, term in zip(approx_graphs, approx_terms):
            self.play(
                Transform(approx_graph, graph, run_time = 2),
                Animation(equation),
                Animation(near_text),
                term.set_fill, None, 1,
            )
            self.wait()
        self.wait(2)


class ExampleApproximationWithSine(ExampleApproximation):
    CONFIG = {
        "function" : np.sin,
        "function_tex" : "\\sin(x)", 
        "order_sequence" : [1, 3, 5],
        "center_point" : 0,
        "approximation_terms" : [
            "x", 
            "-\\frac{1}{6}x^3", 
            "+\\frac{1}{120}x^5",
        ],
        "approximation_color" : GREEN,
        "x_min" : -2*np.pi,
        "x_max" : 2*np.pi,
        "x_tick_frequency" : np.pi/2,
        "y_min" : -2,
        "y_max" : 2,
        "graph_origin" : DOWN + 2*LEFT,
    }


class ExampleApproximationWithCos(ExampleApproximationWithSine):
    CONFIG = {
        "function" : np.cos,
        "function_tex" : "\\cos(\\theta)", 
        "order_sequence" : [0, 2],
        "approximation_terms" : [
            "1", 
            "-\\frac{1}{2} \\theta ^2", 
        ],
        "x_axis_label" : "$\\theta$",
        "y_axis_label" : "",
        "x_axis_width" : 13,
        "graph_origin" : DOWN,
    }

    def construct(self):
        ExampleApproximationWithSine.construct(self)
        randy = Randolph(color = BLUE_C)
        randy.to_corner(DOWN+LEFT)
        high_graph = self.get_graph(lambda x : 4)
        v_lines, alt_v_lines = [
            VGroup(*[
                self.get_vertical_line_to_graph(
                    u*dx, high_graph,
                    line_class = DashedLine,
                    color = YELLOW
                )
                for u in (-1, 1)
            ])
            for dx in (0.01, 0.7)
        ]

        self.play(*list(map(ShowCreation, v_lines)), run_time = 2)
        self.play(Transform(
            v_lines, alt_v_lines,
            run_time = 2,
        ))
        self.play(FadeIn(randy))
        self.play(PiCreatureBubbleIntroduction(
            randy, "How...?",
            bubble_type = ThoughtBubble,
            look_at = self.graph_origin,
            target_mode = "confused"
        ))
        self.wait(2)
        self.play(Blink(randy))
        self.wait()

    def setup_axes(self):
        GraphScene.setup_axes(self)
        x_val_label_pairs = [
            (-np.pi, "-\\pi"),
            (np.pi, "\\pi"),
            (2*np.pi, "2\\pi"),
        ]
        self.x_axis_labels = VGroup()
        for x_val, label in x_val_label_pairs:
            tex = OldTex(label)
            tex.next_to(self.coords_to_point(x_val, 0), DOWN)
            self.add(tex)
            self.x_axis_labels.add(tex)


class ConstructQuadraticApproximation(ExampleApproximationWithCos):
    CONFIG = {
        "x_axis_label" : "$x$",
        "colors" : [BLUE, YELLOW, GREEN],
    }
    def construct(self):
        self.setup_axes()
        self.add_cosine_graph()
        self.add_quadratic_graph()
        self.introduce_quadratic_constants()
        self.show_value_at_zero()
        self.set_c0_to_one()
        self.let_c1_and_c2_vary()
        self.show_tangent_slope()
        self.compute_cosine_derivative()
        self.compute_polynomial_derivative()
        self.let_c2_vary()
        self.point_out_negative_concavity()
        self.compute_cosine_second_derivative()
        self.show_matching_curvature()
        self.show_matching_tangent_lines()
        self.compute_polynomial_second_derivative()
        self.box_final_answer()

    def add_cosine_graph(self):
        cosine_label = OldTex("\\cos(x)")
        cosine_label.to_corner(UP+LEFT)
        cosine_graph = self.get_graph(np.cos)
        dot = Dot(color = WHITE)
        dot.move_to(cosine_label)
        for mob in cosine_label, cosine_graph:
            mob.set_color(self.colors[0])

        def update_dot(dot):
            dot.move_to(cosine_graph.get_points()[-1])
            return dot

        self.play(Write(cosine_label, run_time = 1))
        self.play(dot.move_to, cosine_graph.get_points()[0])
        self.play(
            ShowCreation(cosine_graph),
            UpdateFromFunc(dot, update_dot),
            run_time = 4
        )
        self.play(FadeOut(dot))

        self.cosine_label = cosine_label
        self.cosine_graph = cosine_graph

    def add_quadratic_graph(self):
        quadratic_graph = self.get_quadratic_graph()

        self.play(ReplacementTransform(
            self.cosine_graph.copy(),
            quadratic_graph,
            run_time = 3
        ))

        self.quadratic_graph = quadratic_graph

    def introduce_quadratic_constants(self):
        quadratic_tex = self.get_quadratic_tex("c_0", "c_1", "c_2")
        const_terms = quadratic_tex.get_parts_by_tex("c")
        free_to_change = OldTexText("Free to change")
        free_to_change.next_to(const_terms, DOWN, LARGE_BUFF)
        arrows = VGroup(*[
            Arrow(
                free_to_change.get_top(),
                const.get_bottom(),
                # CHANGE: Arrow.CONFIG does not exist in GL (Cairo Arrow tip_length default was 0.25)
                tip_length = 0.75*0.25,
                color = const.get_color()
            )
            for const in const_terms
        ])
        alt_consts_list = [
            (0, -1, -0.25),
            (1, -1, -0.25),
            (1, 0, -0.25),
            (),
        ]

        self.play(FadeIn(
            quadratic_tex, 
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.play(
            FadeIn(free_to_change),
            *list(map(ShowCreation, arrows))
        )
        self.play(*[
            ApplyMethod(
                const.scale, 0.8,
                run_time = 2,
                rate_func = squish_rate_func(there_and_back, a, a + 0.75)
            )
            for const, a in zip(const_terms, np.linspace(0, 0.25, len(const_terms)))
        ])
        for alt_consts in alt_consts_list:
            self.change_quadratic_graph(
                self.quadratic_graph, *alt_consts
            )
            self.wait()

        self.quadratic_tex = quadratic_tex
        self.free_to_change_group = VGroup(free_to_change, *arrows)
        self.free_to_change_group.arrows = arrows

    def show_value_at_zero(self):
        arrow, x_equals_0 = ax0_group = self.get_arrow_x_equals_0_group()
        ax0_group.next_to(
            self.cosine_label, RIGHT,
            align_using_submobjects = True
        )
        one = OldTex("1")
        one.next_to(arrow, RIGHT)
        one.save_state()
        one.move_to(self.cosine_label)
        one.set_fill(opacity = 0)

        v_line = self.get_vertical_line_to_graph(
            0, self.cosine_graph,
            line_class = DashedLine, 
            color = YELLOW
        )

        self.play(ShowCreation(v_line))
        self.play(
            ShowCreation(arrow),
            Write(x_equals_0, run_time = 2)
        )
        self.play(one.restore)
        self.wait()

        self.v_line = v_line
        self.equals_one_group = VGroup(arrow, x_equals_0, one)

    def set_c0_to_one(self):
        poly_at_zero = self.get_quadratic_tex(
            "c_0", "c_1", "c_2", arg = "0"
        )
        poly_at_zero.next_to(self.quadratic_tex, DOWN)
        equals_c0 = OldTex("=", "c_0", "+0")
        equals_c0.set_color_by_tex("c_0", self.colors[0])
        equals_c0.next_to(
            poly_at_zero.get_part_by_tex("="), DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        poly_group = VGroup(
            equals_c0,
            poly_at_zero,
            self.quadratic_tex,
        )
        poly_group_target = VGroup(
            OldTex("=", "1", "+0").set_color_by_tex("1", self.colors[0]),
            self.get_quadratic_tex("1", "c_1", "c_2", arg = "0"),
            self.get_quadratic_tex("1", "c_1", "c_2"),
        )
        for start, target in zip(poly_group, poly_group_target):
            target.move_to(start)

        self.play(FadeOut(self.free_to_change_group))
        self.play(ReplacementTransform(
            self.quadratic_tex.copy(),
            poly_at_zero
        ))
        self.wait(2)
        self.play(FadeIn(equals_c0))
        self.wait(2)
        self.play(Transform(
            poly_group, poly_group_target,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(2)
        self.play(*list(map(FadeOut, [poly_at_zero, equals_c0])))

        self.free_to_change_group.remove(
            self.free_to_change_group.arrows[0]
        )
        self.play(FadeIn(self.free_to_change_group))

    def let_c1_and_c2_vary(self):
        alt_consts_list = [
            (1, 1, -0.25),
            (1, -1, -0.25),
            (1, -1, 0.25),
            (1, 1, -0.1),
        ]

        for alt_consts in alt_consts_list:
            self.change_quadratic_graph(
                self.quadratic_graph,
                *alt_consts
            )
            self.wait()

    def show_tangent_slope(self):
        graph_point_at_zero = self.input_to_graph_point(
            0, self.cosine_graph
        ) 
        tangent_line = self.get_tangent_line(0, self.cosine_graph)

        self.play(ShowCreation(tangent_line))
        self.change_quadratic_graph(
            self.quadratic_graph, 1, 0, -0.1
        )
        self.wait()
        self.change_quadratic_graph(
            self.quadratic_graph, 1, 1, -0.1
        )
        self.wait(2)
        self.change_quadratic_graph(
            self.quadratic_graph, 1, 0, -0.1
        )
        self.wait(2)

        self.tangent_line = tangent_line

    def compute_cosine_derivative(self):
        derivative, rhs = self.get_cosine_derivative()


        self.play(FadeIn(
            VGroup(derivative, *rhs[:2]),
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(2)
        self.play(Write(VGroup(*rhs[2:])), run_time = 2)
        self.wait()
        self.play(Rotate(
            self.tangent_line, np.pi/12,
            in_place = True,
            run_time = 3,
            rate_func = wiggle
        ))
        self.wait()

    def compute_polynomial_derivative(self):
        derivative = self.get_quadratic_derivative("c_1", "c_2")
        derivative_at_zero = self.get_quadratic_derivative(
            "c_1", "c_2", arg = "0"
        )
        equals_c1 = OldTex("=", "c_1", "+0")
        equals_c1.next_to(
            derivative_at_zero.get_part_by_tex("="), DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        equals_c1.set_color_by_tex("c_1", self.colors[1])
        poly_group = VGroup(
            equals_c1,
            derivative,
            self.quadratic_tex
        )
        poly_group_target = VGroup(
            OldTex("=", "0", "+0").set_color_by_tex(
                "0", self.colors[1], substring = False
            ),
            self.get_quadratic_derivative("0", "c_2", arg = "0"),
            self.get_quadratic_tex("1", "0", "c_2")
        )
        for start, target in zip(poly_group, poly_group_target):
            target.move_to(start)

        self.play(FadeOut(self.free_to_change_group))
        self.play(FadeIn(
            derivative, 
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait()
        self.play(Transform(
            derivative, derivative_at_zero,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(2)
        self.play(Write(equals_c1))
        self.wait(2)
        self.play(Transform(
            poly_group, poly_group_target,
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait(2)

        self.play(*list(map(FadeOut, poly_group[:-1])))
        self.free_to_change_group.remove(
            self.free_to_change_group.arrows[1]
        )
        self.play(FadeIn(self.free_to_change_group))

    def let_c2_vary(self):
        alt_c2_values = [-1, -0.05, 1, -0.2]
        for alt_c2 in alt_c2_values:
            self.change_quadratic_graph(
                self.quadratic_graph,
                1, 0, alt_c2
            )
            self.wait()

    def point_out_negative_concavity(self):
        partial_cosine_graph = self.get_graph(
            np.cos,
            x_min = -1, 
            x_max = 1,
            color = PINK
        )

        self.play(ShowCreation(partial_cosine_graph, run_time = 2))
        self.wait()
        for x, run_time in (-1, 2), (1, 4):
            self.play(self.get_tangent_line_change_anim(
                self.tangent_line, x, self.cosine_graph,
                run_time = run_time
            ))
            self.wait()
        self.play(*list(map(FadeOut, [
            partial_cosine_graph, self.tangent_line
        ])))

    def compute_cosine_second_derivative(self):
        second_deriv, rhs = self.get_cosine_second_derivative()

        self.play(FadeIn(
            VGroup(second_deriv, *rhs[1][:2]),
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(3)
        self.play(Write(VGroup(*rhs[1][2:]), run_time = 2))
        self.wait()

    def show_matching_curvature(self):
        alt_consts_list = [
            (1, 1, -0.2),
            (1, 0, -0.2),
            (1, 0, -0.5),
        ]
        for alt_consts in alt_consts_list:
            self.change_quadratic_graph(
                self.quadratic_graph,
                *alt_consts
            )
            self.wait()

    def show_matching_tangent_lines(self):
        graphs = [self.quadratic_graph, self.cosine_graph]
        tangent_lines = [
            self.get_tangent_line(0, graph, color = color)
            for graph, color in zip(graphs, [WHITE, YELLOW])
        ]
        tangent_change_anims = [
            self.get_tangent_line_change_anim(
                line, np.pi/2, graph, 
                run_time = 6,
                rate_func = there_and_back,
            )
            for line, graph in zip(tangent_lines, graphs)
        ]

        self.play(*list(map(ShowCreation, tangent_lines)))
        self.play(*tangent_change_anims)
        self.play(*list(map(FadeOut, tangent_lines)))

    def compute_polynomial_second_derivative(self):
        c2s = ["c_2", "\\text{\\tiny $\\left(-\\frac{1}{2}\\right)$}"]
        derivs = [
            self.get_quadratic_derivative("0", c2)
            for c2 in c2s
        ]
        second_derivs = [
            OldTex(
                "{d^2 P \\over dx^2}", "(x)", "=", "2", c2
            )
            for c2 in c2s
        ]
        for deriv, second_deriv in zip(derivs, second_derivs):
            second_deriv[0].scale(
                0.7, about_point = second_deriv[0].get_right()
            )
            second_deriv[-1].set_color(self.colors[-1])
            second_deriv.next_to(
                deriv, DOWN, 
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )

        poly_group = VGroup(
            second_derivs[0], 
            derivs[0],
            self.quadratic_tex
        )
        poly_group_target = VGroup(
            second_derivs[1],
            derivs[1],
            self.get_quadratic_tex("1", "0", c2s[1])
        )
        for tex_mob in poly_group_target:
            tex_mob.get_part_by_tex(c2s[1]).shift(SMALL_BUFF*UP)

        self.play(FadeOut(self.free_to_change_group))
        self.play(FadeIn(derivs[0]))
        self.wait(2)
        self.play(Write(second_derivs[0]))
        self.wait(2)
        self.play(Transform(
            poly_group, poly_group_target,
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait(3)

    def box_final_answer(self):
        box = Rectangle(stroke_color = PINK)
        box.stretch_to_fit_width(
            self.quadratic_tex.get_width() + MED_LARGE_BUFF
        )
        box.stretch_to_fit_height(
            self.quadratic_tex.get_height() + MED_LARGE_BUFF
        )
        box.move_to(self.quadratic_tex)

        self.play(ShowCreation(box, run_time = 2))
        self.wait(2)

    ######

    def change_quadratic_graph(self, graph, *args, **kwargs):
        transformation_kwargs = {}
        transformation_kwargs["run_time"] = kwargs.pop("run_time", 2)
        transformation_kwargs["rate_func"] = kwargs.pop("rate_func", smooth)
        new_graph = self.get_quadratic_graph(*args, **kwargs)
        self.play(Transform(graph, new_graph, **transformation_kwargs))
        graph.underlying_function = new_graph.underlying_function

    def get_quadratic_graph(self, c0 = 1, c1 = 0, c2 = -0.5):
        return self.get_graph(
            lambda x : c0 + c1*x + c2*x**2,
            color = self.colors[2]
        )

    def get_quadratic_tex(self, c0, c1, c2, arg = "x"):
        tex_mob = OldTex(
            "P(", arg, ")", "=", 
            c0, "+", c1, arg, "+", c2, arg, "^2"
        )
        for tex, color in zip([c0, c1, c2], self.colors):
            tex_mob.set_color_by_tex(tex, color)
        tex_mob.to_corner(UP+RIGHT)
        return tex_mob

    def get_quadratic_derivative(self, c1, c2, arg = "x"):
        result = OldTex(
            "{dP \\over dx}", "(", arg, ")", "=",
            c1, "+", "2", c2, arg
        )
        result[0].scale(0.7, about_point = result[0].get_right())
        for index, color in zip([5, 8], self.colors[1:]):
            result[index].set_color(color)
        if hasattr(self, "quadratic_tex"):
            result.next_to(
                self.quadratic_tex, DOWN,
                buff = MED_LARGE_BUFF,
                aligned_edge = LEFT
            )
        return result

    def get_arrow_x_equals_0_group(self):
        arrow = Arrow(LEFT, RIGHT)
        x_equals_0 = OldTex("x = 0")
        x_equals_0.scale(0.75)
        x_equals_0.next_to(arrow.get_center(), UP, 2*SMALL_BUFF)
        x_equals_0.shift(SMALL_BUFF*LEFT)
        return VGroup(arrow, x_equals_0)

    def get_tangent_line(self, x, graph, color = YELLOW):
        tangent_line = Line(LEFT, RIGHT, color = color)
        tangent_line.rotate(self.angle_of_tangent(x, graph))
        tangent_line.scale(2)
        tangent_line.move_to(self.input_to_graph_point(x, graph))
        return tangent_line

    def get_tangent_line_change_anim(self, tangent_line, new_x, graph, **kwargs):
        start_x = self.x_axis.point_to_number(
            tangent_line.get_center()
        )
        def update(tangent_line, alpha):
            x = interpolate(start_x, new_x, alpha)
            new_line = self.get_tangent_line(
                x, graph, color = tangent_line.get_color()
            )
            Transform(tangent_line, new_line).update(1)
            return tangent_line
        return UpdateFromAlphaFunc(tangent_line, update, **kwargs)

    def get_cosine_derivative(self):
        if not hasattr(self, "cosine_label"):
            self.cosine_label = OldTex("\\cos(x)")
            self.cosine_label.to_corner(UP+LEFT)
        derivative = OldTex(
            "{d(", "\\cos", ")", "\\over", "dx}", "(0)",
        )
        derivative.set_color_by_tex("\\cos", self.colors[0])
        derivative.scale(0.7)
        derivative.next_to(
            self.cosine_label, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rhs = OldTex("=", "-\\sin(0)", "=", "0")
        rhs.set_color_by_tex("\\sin", self.colors[1])
        rhs.scale(0.75)
        rhs.next_to(
            derivative, RIGHT,
            align_using_submobjects = True
        )

        self.cosine_derivative = VGroup(derivative, rhs)
        return self.cosine_derivative

    def get_cosine_second_derivative(self):
        if not hasattr(self, "cosine_derivative"):
            self.get_cosine_derivative()
        second_deriv = OldTex(
            "{d^2(", "\\cos", ")", "\\over", "dx^2}", 
            "(", "0", ")",
        )
        second_deriv.set_color_by_tex("cos", self.colors[0])
        second_deriv.set_color_by_tex("-\\cos", self.colors[2])
        second_deriv.scale(0.75)
        second_deriv.add_background_rectangle()
        second_deriv.next_to(
            self.cosine_derivative, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rhs = OldTex("=", "-\\cos(0)", "=", "-1")
        rhs.set_color_by_tex("cos", self.colors[2])
        rhs.scale(0.8)
        rhs.next_to(
            second_deriv, RIGHT, 
            align_using_submobjects = True
        )
        rhs.add_background_rectangle()

        self.cosine_second_derivative = VGroup(second_deriv, rhs)
        return self.cosine_second_derivative


class CubicAndQuarticApproximations(ConstructQuadraticApproximation):
    CONFIG = {
        "colors": [BLUE, YELLOW, GREEN, RED, MAROON_B],
    }
    def construct(self):
        self.add_background()
        self.take_third_derivative_of_cubic()
        self.show_third_derivative_of_cosine()
        self.set_c3_to_zero()
        self.show_cubic_curves()
        self.add_quartic_term()
        self.show_fourth_derivative_of_cosine()
        self.take_fourth_derivative_of_quartic()
        self.solve_for_c4()
        self.show_quartic_approximation()


    def add_background(self):
        self.setup_axes()
        self.cosine_graph = self.get_graph(
            np.cos, color = self.colors[0]
        )
        self.quadratic_graph = self.get_quadratic_graph()
        self.big_rect = Rectangle(
            height = FRAME_HEIGHT,
            width = FRAME_WIDTH,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.5,
        )
        self.add(
            self.cosine_graph, self.quadratic_graph,
            self.big_rect
        )

        self.cosine_label = OldTex("\\cos", "(0)", "=1")
        self.cosine_label.set_color_by_tex("cos", self.colors[0])
        self.cosine_label.scale(0.75)
        self.cosine_label.to_corner(UP+LEFT)
        self.add(self.cosine_label)
        self.add(self.get_cosine_derivative())
        self.add(self.get_cosine_second_derivative())

        self.polynomial = OldTex(
            "P(x)=", "1", "-\\frac{1}{2}", "x^2"
        )
        self.polynomial.set_color_by_tex("1", self.colors[0])
        self.polynomial.set_color_by_tex("-\\frac{1}{2}", self.colors[2])
        self.polynomial.to_corner(UP+RIGHT)
        self.polynomial.quadratic_part = VGroup(
            *self.polynomial[1:]
        )
        self.add(self.polynomial)

    def take_third_derivative_of_cubic(self):
        polynomial = self.polynomial
        plus_cubic_term = OldTex("+\\,", "c_3", "x^3")
        plus_cubic_term.next_to(polynomial, RIGHT)
        plus_cubic_term.to_edge(RIGHT, buff = LARGE_BUFF)
        plus_cubic_term.set_color_by_tex("c_3", self.colors[3])
        plus_cubic_copy = plus_cubic_term.copy()

        polynomial.generate_target()
        polynomial.target.next_to(plus_cubic_term, LEFT)

        self.play(FocusOn(polynomial))
        self.play(
            MoveToTarget(polynomial),
            GrowFromCenter(plus_cubic_term)
        )
        self.wait()

        brace = Brace(polynomial.quadratic_part, DOWN)
        third_derivative = OldTex(
            "\\frac{d^3 P}{dx^3}(x) = ", "0"
        )
        third_derivative.shift(
            brace.get_bottom() + MED_SMALL_BUFF*DOWN -\
            third_derivative.get_part_by_tex("0").get_top()
        )        

        self.play(Write(third_derivative[0]))
        self.play(GrowFromCenter(brace))
        self.play(ReplacementTransform(
            polynomial.quadratic_part.copy(),
            VGroup(third_derivative[1])
        ))
        self.wait(2)
        self.play(plus_cubic_copy.next_to, third_derivative, RIGHT)
        derivative_term = self.take_derivatives_of_monomial(
            VGroup(*plus_cubic_copy[1:])
        )
        third_derivative.add(plus_cubic_copy[0], derivative_term)

        self.plus_cubic_term = plus_cubic_term
        self.polynomial_third_derivative = third_derivative
        self.polynomial_third_derivative_brace = brace

    def show_third_derivative_of_cosine(self):
        cosine_third_derivative = self.get_cosine_third_derivative()
        dot = Dot(fill_opacity = 0.5)
        dot.move_to(self.polynomial_third_derivative)

        self.play(
            dot.move_to, cosine_third_derivative,
            dot.set_fill, None, 0
        )
        self.play(ReplacementTransform(
            self.cosine_second_derivative.copy(),
            cosine_third_derivative
        ))
        self.wait(2)
        dot.set_fill(opacity = 0.5)
        self.play(
            dot.move_to, self.polynomial_third_derivative.get_right(),
            dot.set_fill, None, 0,
        )
        self.wait()

    def set_c3_to_zero(self):
        c3s = VGroup(
            self.polynomial_third_derivative[-1][-1],
            self.plus_cubic_term.get_part_by_tex("c_3")
        )
        zeros = VGroup(*[
            OldTex("0").move_to(c3)
            for c3 in c3s
        ])
        zeros.set_color(self.colors[3])
        zeros.shift(SMALL_BUFF*UP)
        zeros[0].shift(0.25*SMALL_BUFF*(UP+LEFT))

        self.play(Transform(
            c3s, zeros, 
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(2)

    def show_cubic_curves(self):
        real_graph = self.quadratic_graph
        real_graph.save_state()
        graph = real_graph.copy()
        graph.save_state()
        alt_graphs = [
            self.get_graph(func, color = real_graph.get_color())
            for func in [
                lambda x : x*(x-1)*(x+1),
                lambda x : 1 - 0.5*(x**2) + 0.2*(x**3)
            ]
        ]

        self.play(FadeIn(graph))
        real_graph.set_stroke(width = 0)
        for alt_graph in alt_graphs:
            self.play(Transform(graph, alt_graph, run_time = 2))
            self.wait()
        self.play(graph.restore, run_time = 2)
        real_graph.restore()
        self.play(FadeOut(graph))

    def add_quartic_term(self):
        polynomial = self.polynomial
        plus_quartic_term = OldTex("+\\,", "c_4", "x^4")
        plus_quartic_term.next_to(polynomial, RIGHT)
        plus_quartic_term.set_color_by_tex("c_4", self.colors[4])

        self.play(*list(map(FadeOut, [
            self.plus_cubic_term,
            self.polynomial_third_derivative,
            self.polynomial_third_derivative_brace,
        ])))
        self.play(Write(plus_quartic_term))
        self.wait()

        self.plus_quartic_term = plus_quartic_term

    def show_fourth_derivative_of_cosine(self):
        cosine_fourth_derivative = self.get_cosine_fourth_derivative()

        self.play(FocusOn(self.cosine_third_derivative))
        self.play(ReplacementTransform(
            self.cosine_third_derivative.copy(),
            cosine_fourth_derivative
        ))
        self.wait(3)

    def take_fourth_derivative_of_quartic(self):
        quartic_term = VGroup(*self.plus_quartic_term.copy()[1:])
        fourth_deriv_lhs = OldTex("{d^4 P \\over dx^4}(x)", "=")
        fourth_deriv_lhs.next_to(
            self.polynomial, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        alt_rhs = OldTex("=", "24 \\cdot", "c_4")
        alt_rhs.next_to(
            fourth_deriv_lhs.get_part_by_tex("="), DOWN,
            buff = LARGE_BUFF,
            aligned_edge = LEFT
        )
        alt_rhs.set_color_by_tex("c_4", self.colors[4])

        self.play(Write(fourth_deriv_lhs))
        self.play(
            quartic_term.next_to, fourth_deriv_lhs, RIGHT
        )
        self.wait()
        fourth_deriv_rhs = self.take_derivatives_of_monomial(quartic_term)
        self.wait()
        self.play(Write(alt_rhs))
        self.wait()

        self.fourth_deriv_lhs = fourth_deriv_lhs
        self.fourth_deriv_rhs = fourth_deriv_rhs
        self.fourth_deriv_alt_rhs = alt_rhs

    def solve_for_c4(self):
        c4s = VGroup(
            self.fourth_deriv_alt_rhs.get_part_by_tex("c_4"),
            self.fourth_deriv_rhs[-1],
            self.plus_quartic_term.get_part_by_tex("c_4")
        )
        fraction = OldTex("\\text{\\small $\\frac{1}{24}$}")
        fraction.set_color(self.colors[4])
        fractions = VGroup(*[
            fraction.copy().move_to(c4, LEFT)
            for c4 in c4s
        ])
        fractions.shift(SMALL_BUFF*UP)
        x_to_4 = self.plus_quartic_term.get_part_by_tex("x^4")
        x_to_4.generate_target()
        x_to_4.target.shift(MED_SMALL_BUFF*RIGHT)

        self.play(
            Transform(
                c4s, fractions,
                run_time = 3,
                lag_ratio = 0.5,
            ),
            MoveToTarget(x_to_4, run_time = 2)
        )
        self.wait(3)

    def show_quartic_approximation(self):
        real_graph = self.quadratic_graph
        graph = real_graph.copy()
        quartic_graph = self.get_graph(
            lambda x : 1 - (x**2)/2.0 + (x**4)/24.0,
            color = graph.get_color(),
        )
        tex_mobs = VGroup(*[
            self.polynomial,
            self.fourth_deriv_rhs,
            self.fourth_deriv_alt_rhs,
            self.cosine_label,
            self.cosine_derivative,
            self.cosine_second_derivative,
            self.cosine_third_derivative[1],
        ])
        for tex_mob in tex_mobs:
            tex_mob.add_to_back(BackgroundRectangle(tex_mob))


        self.play(FadeIn(graph))
        real_graph.set_stroke(width = 0)
        self.play(
            Transform(
                graph, quartic_graph,
                run_time = 3,
            ),
            Animation(tex_mobs)
        )
        self.wait(3)


    ####

    def take_derivatives_of_monomial(self, term, *added_anims):
        """
        Must be a group of pure Texs,
        last part must be of the form x^n
        """
        n = int(term[-1].get_tex()[-1])
        curr_term = term
        added_anims_iter = iter(added_anims)
        for k in range(n, 0, -1):
            exponent = curr_term[-1][-1]
            exponent_copy = exponent.copy()
            front_num = OldTex("%d \\cdot"%k)
            front_num.move_to(curr_term[0][0], LEFT)

            new_monomial = OldTex("x^%d"%(k-1))
            new_monomial.replace(curr_term[-1])
            Transform(curr_term[-1], new_monomial).update(1)
            curr_term.generate_target()
            curr_term.target.shift(
                (front_num.get_width()+SMALL_BUFF)*RIGHT
            )
            curr_term[-1][-1].set_fill(opacity = 0)

            possibly_added_anims = []
            try:
                possibly_added_anims.append(next(added_anims_iter))
            except:
                pass

            self.play(
                ApplyMethod(
                    exponent_copy.replace, front_num[0],
                    path_arc = np.pi,
                ),
                Write(
                    front_num[1], 
                    rate_func = squish_rate_func(smooth, 0.5, 1)
                ),
                MoveToTarget(curr_term),
                *possibly_added_anims,
                run_time = 2
            )
            self.remove(exponent_copy)
            self.add(front_num)
            curr_term = VGroup(front_num, *curr_term)
        self.wait()
        self.play(FadeOut(curr_term[-1]))

        return VGroup(*curr_term[:-1])

    def get_cosine_third_derivative(self):
        if not hasattr(self, "cosine_second_derivative"):
            self.get_cosine_second_derivative()
        third_deriv = OldTex(
            "{d^3(", "\\cos", ")", "\\over", "dx^3}", 
            "(", "0", ")",
        )
        third_deriv.set_color_by_tex("cos", self.colors[0])
        third_deriv.set_color_by_tex("-\\cos", self.colors[3])
        third_deriv.scale(0.75)
        third_deriv.add_background_rectangle()
        third_deriv.next_to(
            self.cosine_second_derivative, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rhs = OldTex("=", "\\sin(0)", "=", "0")
        rhs.set_color_by_tex("sin", self.colors[3])
        rhs.scale(0.8)
        rhs.next_to(
            third_deriv, RIGHT, 
            align_using_submobjects = True
        )
        rhs.add_background_rectangle()
        rhs.background_rectangle.scale(1.2)

        self.cosine_third_derivative = VGroup(third_deriv, rhs)
        return self.cosine_third_derivative

    def get_cosine_fourth_derivative(self):
        if not hasattr(self, "cosine_third_derivative"):
            self.get_cosine_third_derivative()
        fourth_deriv = OldTex(
            "{d^4(", "\\cos", ")", "\\over", "dx^4}", 
            "(", "0", ")",
        )
        fourth_deriv.set_color_by_tex("cos", self.colors[0])
        fourth_deriv.scale(0.75)
        fourth_deriv.add_background_rectangle()
        fourth_deriv.next_to(
            self.cosine_third_derivative, DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        rhs = OldTex("=", "\\cos(0)", "=", "1")
        rhs.set_color_by_tex("cos", self.colors[4])
        rhs.scale(0.8)
        rhs.next_to(
            fourth_deriv, RIGHT, 
            align_using_submobjects = True
        )
        rhs.add_background_rectangle()
        rhs.background_rectangle.scale(1.2)

        self.cosine_fourth_derivative = VGroup(fourth_deriv, rhs)
        return self.cosine_fourth_derivative


class EachTermControlsOneDerivative(Scene):
    def construct(self):
        colors = CubicAndQuarticApproximations.CONFIG["colors"]
        polynomial = OldTex(
            "P(x) = ", "c_0", "+", "c_1", "x", *it.chain(*[
                ["+", "c_%d"%n, "x^%d"%n]
                for n in range(2, 5)
            ])
        )
        consts = polynomial.get_parts_by_tex("c")
        deriv_words = VGroup(*[
            OldTexText("Controls \\\\ $%s(0)$"%tex)
            for tex in [
                "P",
                "\\frac{dP}{dx}",
            ] + [
                "\\frac{d^%d P}{dx^%d}"%(n, n)
                for n in range(2, 5)
            ]
        ])
        deriv_words.arrange(
            RIGHT, 
            buff = LARGE_BUFF,
            aligned_edge = UP
        )
        deriv_words.set_width(FRAME_WIDTH - MED_LARGE_BUFF)
        deriv_words.to_edge(UP)

        for const, deriv, color in zip(consts, deriv_words, colors):
            for mob in const, deriv:
                mob.set_color(color)
            arrow = Arrow(
                const.get_top(),
                deriv.get_bottom(),
                # buff = SMALL_BUFF,
                color = color
            )
            deriv.arrow = arrow

        self.add(polynomial)
        for deriv in deriv_words:
            self.play(
                ShowCreation(deriv.arrow),
                FadeIn(deriv)
            )
            self.wait()
