# ==============================================================================
# Scene:      Antiderivative
# Source:     videos/_2017/eoc/chapter9.py (lines 991-1418)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Antiderivative.py Antiderivative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AverageOfContinuousVariable(GraphScene):
    CONFIG = {
        "bounds" : [1, 7],
        "bound_colors" : [RED, GREEN],
    }
    def construct(self):
        self.setup_axes()
        graph = self.get_graph(
            lambda x : 0.1*x*(x-3)*(x-6) + 4
        )
        graph_label = self.get_graph_label(graph, "f(x)")
        boundary_lines = self.get_vertical_lines_to_graph(
            graph, *self.bounds, num_lines = 2,
            line_class = DashedLine
        )
        for line, color in zip(boundary_lines, self.bound_colors):
            line.set_color(color)
        v_line = self.get_vertical_line_to_graph(
            self.bounds[0], graph, color = YELLOW,
        )

        question = OldTexText(
            "What is the average \\\\ value of $f(x)$?"
        )
        question.next_to(boundary_lines, UP)

        self.play(ShowCreation(graph), Write(graph_label))
        self.play(ShowCreation(boundary_lines))
        self.play(FadeIn(
            question,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.play(ShowCreation(v_line))
        for bound in reversed(self.bounds):
            self.play(self.get_v_line_change_anim(
                v_line, graph, bound, 
                run_time = 3,
            ))
            self.wait()
        self.wait()

    def get_v_line_change_anim(self, v_line, graph, target_x, **kwargs):
        start_x = self.x_axis.point_to_number(v_line.get_bottom())
        def update(v_line, alpha):
            new_x = interpolate(start_x, target_x, alpha)
            v_line.put_start_and_end_on(
                self.coords_to_point(new_x, 0),
                self.input_to_graph_point(new_x, graph)
            )
            return v_line
        return UpdateFromAlphaFunc(v_line, update, **kwargs)


class AverageOfSineStart(AverageOfContinuousVariable):
    CONFIG = {
        "y_min" : -2, 
        "y_max" : 2,
        "x_min" : -1,
        "x_max" : 2.5*np.pi,
        "x_leftmost_tick" : 0,
        "x_tick_frequency" : np.pi/4,
        "x_axis_width" : 12,
        "graph_origin" : 5*LEFT,
        "x_label_scale_val" : 0.75,
        "func" : np.sin,
        "graph_color" : BLUE,
        "bounds" : [0, np.pi],
    }
    def construct(self):
        self.setup_axes()
        self.add_graph()
        self.ask_about_average()

    def add_graph(self, run_time = 1):
        graph = self.get_graph(self.func, color = self.graph_color)
        graph_label = self.get_graph_label(
            graph, "\\sin(x)",
            direction = UP
        )
        self.play(
            ShowCreation(graph),
            Write(graph_label),
            run_time = run_time
        )

        self.graph = graph
        self.graph_label = graph_label

    def ask_about_average(self):
        half_period_graph = self.get_graph_portion_between_bounds()
        question = OldTexText("Average height?")
        question.to_edge(UP)
        arrow = Arrow(question.get_bottom(), half_period_graph.get_top())
        midpoint = np.mean(self.bounds)
        v_line = self.get_vertical_line_to_graph(
            midpoint, self.graph,
            line_class = DashedLine,
            color = WHITE
        )

        self.play(FadeIn(half_period_graph))
        self.play(
            Write(question, run_time = 2),
            ShowCreation(arrow)
        )
        self.play(ShowCreation(v_line))
        for bound in self.bounds + [midpoint]:
            self.play(self.get_v_line_change_anim(
                v_line, self.graph, bound,
                run_time = 3
            ))

    #########

    def get_graph_portion_between_bounds(self):
        self.graph_portion_between_bounds = self.get_graph(
            self.func,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
            color = YELLOW
        )
        return self.graph_portion_between_bounds

    def setup_axes(self):
        GraphScene.setup_axes(self)
        self.add_x_axis_labels()

    def add_x_axis_labels(self):
        labels_and_x_values = [
            ("\\pi/2", np.pi/2),
            ("\\pi", np.pi),
            ("3\\pi/2", 3*np.pi/2),
            ("2\\pi", 2*np.pi),
        ]
        self.x_axis_labels = VGroup()
        for label, x in labels_and_x_values:
            tex_mob = OldTex(label)
            tex_mob.scale(self.x_label_scale_val)
            tex_mob.move_to(
                self.coords_to_point(x, -3*self.x_axis.tick_size), 
            )
            self.add(tex_mob)
            self.x_axis_labels.add(tex_mob)


class Antiderivative(AverageOfSineStart):
    CONFIG = {
        "antideriv_color" : GREEN,
        "deriv_color" : BLUE,
        "riemann_rect_dx" : 0.01,
        "y_axis_label" : "",
        "graph_origin" : 4*LEFT + DOWN,
    }
    def construct(self):
        self.setup_axes()
        self.add_x_axis_labels()
        self.negate_derivative_of_cosine()
        self.walk_through_slopes()
        self.apply_ftoc()
        self.show_difference_in_antiderivative()
        self.comment_on_area()
        self.divide_by_pi()
        self.set_color_antiderivative_fraction()
        self.show_slope()
        self.bring_back_derivative()
        self.show_tangent_slope()

    def add_x_axis_labels(self):
        AverageOfSineStart.add_x_axis_labels(self)
        self.remove(*self.x_axis_labels[::2])

    def negate_derivative_of_cosine(self):
        cos, neg_cos, sin, neg_sin = graphs = [
            self.get_graph(func)
            for func in [
                np.cos, 
                lambda x : -np.cos(x), 
                np.sin,
                lambda x : -np.sin(x),
            ]
        ]
        VGroup(cos, neg_cos).set_color(self.antideriv_color)
        VGroup(sin, neg_sin).set_color(self.deriv_color)
        labels = ["\\cos(x)", "-\\cos(x)", "\\sin(x)", "-\\sin(x)"]
        x_vals = [2*np.pi, 2*np.pi, 5*np.pi/2, 5*np.pi/2]
        vects = [UP, DOWN, UP, DOWN]
        for graph, label, x_val, vect in zip(graphs, labels, x_vals, vects):
            graph.label = self.get_graph_label(
                graph, label,
                x_val = x_val,
                direction = vect,
                buff = SMALL_BUFF
            ) 

        derivs = []
        for F, f in ("\\cos", "-\\sin"), ("-\\cos", "\\sin"):
            deriv = OldTex(
                "{d(", F, ")", "\\over\\,", "dx}", "(x)", 
                "=", f, "(x)"
            )
            deriv.set_color_by_tex(F, self.antideriv_color)
            deriv.set_color_by_tex(f, self.deriv_color)
            deriv.to_edge(UP)
            derivs.append(deriv)
        cos_deriv, neg_cos_deriv = derivs

        self.add(cos_deriv)
        for graph in cos, neg_sin:
            self.play(
                ShowCreation(graph, rate_func = smooth),
                Write(
                    graph.label, 
                    rate_func = squish_rate_func(smooth, 0.3, 1)
                ),
                run_time = 2
            )
            self.wait()
        self.wait()
        self.play(*[
            ReplacementTransform(*pair)
            for pair in [
                (derivs),
                (cos, neg_cos),
                (cos.label, neg_cos.label),
                (neg_sin, sin),
                (neg_sin.label, sin.label),
            ]
        ])
        self.wait(2)

        self.neg_cos = neg_cos
        self.sin = sin
        self.deriv = neg_cos_deriv

    def walk_through_slopes(self):
        neg_cos = self.neg_cos
        sin = self.sin

        faders = sin, sin.label
        for mob in faders:
            mob.save_state()
        sin_copy = self.get_graph(
            np.sin,
            x_min = 0,
            x_max = 2*np.pi,
            color = BLUE,
        )
        v_line = self.get_vertical_line_to_graph(
            0, neg_cos,
            line_class = DashedLine,
            color = WHITE
        )

        ss_group = self.get_secant_slope_group(
            0, neg_cos,
            dx = 0.001,
            secant_line_color = YELLOW
        )
        def quad_smooth(t):
            return 0.25*(np.floor(4*t) + smooth((4*t) % 1))

        self.play(*[
            ApplyMethod(m.fade, 0.6)
            for m in faders
        ])
        self.wait()
        self.play(*list(map(ShowCreation, ss_group)), run_time = 2)
        kwargs = {
            "run_time" : 20,
            "rate_func" : quad_smooth,
        }
        v_line_anim = self.get_v_line_change_anim(
            v_line, sin_copy, 2*np.pi,
            **kwargs
        )
        self.animate_secant_slope_group_change(
            ss_group,
            target_x = 2*np.pi,
            added_anims = [
                ShowCreation(sin_copy, **kwargs),
                v_line_anim
            ],
            **kwargs
        )
        self.play(
            *list(map(FadeOut, [ss_group, v_line, sin_copy]))
        )
        self.wait()

        self.ss_group = ss_group

    def apply_ftoc(self):
        deriv = self.deriv
        integral = OldTex(
            "\\int", "^\\pi", "_0", "\\sin(x)", "\\,dx"
        )
        rhs = OldTex(
            "=", "\\big(", "-\\cos", "(", "\\pi", ")", "\\big)",
            "-", "\\big(", "-\\cos", "(", "0", ")", "\\big)",
        )
        rhs.next_to(integral, RIGHT)
        equation = VGroup(integral, rhs)
        equation.to_corner(UP+RIGHT, buff = MED_SMALL_BUFF)
        (start_pi, end_pi), (start_zero, end_zero) = start_end_pairs = [
            [
                m.get_part_by_tex(tex) 
                for m in (integral, rhs)
            ]
            for tex in ("\\pi", "0")
        ]

        for tex_mob in integral, rhs:
            tex_mob.set_color_by_tex("sin", self.deriv_color)
            tex_mob.set_color_by_tex("cos", self.antideriv_color)
            tex_mob.set_color_by_tex("0", YELLOW)
            tex_mob.set_color_by_tex("\\pi", YELLOW)

        self.play(
            Write(integral),
            self.deriv.scale, 0.5,
            self.deriv.center,
            self.deriv.to_edge, LEFT, MED_SMALL_BUFF,
            self.deriv.shift, UP,
        )
        self.wait()

        self.play(FadeIn(
            VGroup(*[part for part in rhs if part not in [end_pi, end_zero]]),
            lag_ratio = 0.5,
            run_time = 2,
        ))
        self.wait()
        for start, end in start_end_pairs:
            self.play(ReplacementTransform(
                start.copy(), end,
                path_arc = np.pi/6,
                run_time = 2
            ))
            self.wait()

        self.integral = integral
        self.rhs = rhs

    def show_difference_in_antiderivative(self):
        pi_point, zero_point = points = [
            self.input_to_graph_point(x, self.neg_cos)
            for x in reversed(self.bounds)
        ]
        interim_point = pi_point[0]*RIGHT + zero_point[1]*UP
        pi_dot, zero_dot = dots = [
            Dot(point, color = YELLOW)
            for point in points
        ]
        v_line = DashedLine(pi_point, interim_point)
        h_line = DashedLine(interim_point, zero_point)
        v_line_brace = Brace(v_line, RIGHT)
        two_height_label = v_line_brace.get_text(
            "$2$", buff = SMALL_BUFF
        )
        two_height_label.add_background_rectangle()

        pi = self.x_axis_labels[1]
        #Horrible hack
        black_pi = pi.copy().set_color(BLACK)
        self.add(black_pi, pi)

        cos_tex = self.rhs.get_part_by_tex("cos")

        self.play(ReplacementTransform(
            cos_tex.copy(), pi_dot
        ))
        self.wait()
        moving_dot = pi_dot.copy()
        self.play(
            ShowCreation(v_line),
            # Animation(pi),
            pi.shift, 0.8*pi.get_width()*(LEFT+UP),
            moving_dot.move_to, interim_point,
        )
        self.play(
            ShowCreation(h_line),
            ReplacementTransform(moving_dot, zero_dot)
        )
        self.play(GrowFromCenter(v_line_brace))
        self.wait(2)
        self.play(Write(two_height_label))
        self.wait(2)

        self.v_line = v_line
        self.h_line = h_line
        self.pi_dot = pi_dot
        self.zero_dot = zero_dot
        self.v_line_brace = v_line_brace
        self.two_height_label = two_height_label

    def comment_on_area(self):
        rects = self.get_riemann_rectangles(
            self.sin, 
            dx = self.riemann_rect_dx,
            stroke_width = 0,
            fill_opacity = 0.7,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
        )
        area_two = OldTex("2").replace(
            self.two_height_label
        )

        self.play(Write(rects))
        self.wait()
        self.play(area_two.move_to, rects)
        self.wait(2)

        self.rects = rects
        self.area_two = area_two

    def divide_by_pi(self):
        integral = self.integral
        rhs = self.rhs
        equals = rhs[0]
        rhs_without_eq = VGroup(*rhs[1:])
        frac_lines = VGroup(*[
            OldTex("\\over\\,").stretch_to_fit_width(
                mob.get_width()
            ).move_to(mob)
            for mob in (integral, rhs_without_eq)
        ])
        frac_lines.shift(
            (integral.get_height()/2 + SMALL_BUFF)*DOWN
        )
        pi_minus_zeros = VGroup(*[
            OldTex("\\pi", "-", "0").next_to(line, DOWN)
            for line in frac_lines
        ])
        for tex_mob in pi_minus_zeros:
            for tex in "pi", "0":
                tex_mob.set_color_by_tex(tex, YELLOW)

        answer = OldTex(" = \\frac{2}{\\pi}")
        answer.next_to(
            frac_lines, RIGHT,
            align_using_submobjects = True
        )
        answer.shift_onto_screen()

        self.play(
            equals.next_to, frac_lines[0].copy(), RIGHT,
            rhs_without_eq.next_to, frac_lines[1].copy(), UP,
            *list(map(Write, frac_lines))
        )
        self.play(*[
            ReplacementTransform(
                integral.get_part_by_tex(tex).copy(),
                pi_minus_zeros[0].get_part_by_tex(tex)
            )
            for tex in ("\\pi","0")
        ] + [
            Write(pi_minus_zeros[0].get_part_by_tex("-"))
        ])
        self.play(*[
            ReplacementTransform(
                rhs.get_part_by_tex(
                    tex, substring = False
                ).copy(),
                pi_minus_zeros[1].get_part_by_tex(tex)
            )
            for tex in ("\\pi", "-", "0")
        ])
        self.wait(2)

        full_equation = VGroup(
            integral, frac_lines, rhs, pi_minus_zeros
        )
        background_rect = BackgroundRectangle(full_equation, fill_opacity = 1)
        background_rect.stretch_in_place(1.2, dim = 1)
        full_equation.add_to_back(background_rect)
        self.play(
            full_equation.shift, 
            (answer.get_width()+MED_LARGE_BUFF)*LEFT
        )
        self.play(Write(answer))
        self.wait()

        self.antiderivative_fraction = VGroup(
            rhs_without_eq,
            frac_lines[1],
            pi_minus_zeros[1]
        )
        self.integral_fraction = VGroup(
            integral,
            frac_lines[0],
            pi_minus_zeros[0],
            equals
        )

    def set_color_antiderivative_fraction(self):
        fraction = self.antiderivative_fraction
        big_rect = Rectangle(
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.75,
        )
        big_rect.set_width(FRAME_WIDTH)
        big_rect.set_height(FRAME_HEIGHT)
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)

        self.play(
            FadeIn(big_rect),
            FadeIn(morty),
            Animation(fraction)
        )
        self.play(morty.change, "raise_right_hand", fraction)
        self.play(Blink(morty))
        self.wait(2)
        self.play(
            FadeOut(big_rect),
            FadeOut(morty),
            Animation(fraction)
        )

    def show_slope(self):
        line = Line(
            self.zero_dot.get_center(),
            self.pi_dot.get_center(),
        )
        line.set_color(RED)
        line.scale(1.2)

        new_v_line = self.v_line.copy().set_color(RED)
        new_h_line = self.h_line.copy().set_color(RED)

        pi = OldTex("\\pi")
        pi.next_to(self.h_line, DOWN)

        self.play(
            FadeOut(self.rects),
            FadeOut(self.area_two)
        )
        self.play(ShowCreation(new_v_line))
        self.play(
            ShowCreation(new_h_line),
            Write(pi)
        )
        self.wait()
        self.play(ShowCreation(line, run_time = 2))
        self.wait()

    def bring_back_derivative(self):
        self.play(
            FadeOut(self.integral_fraction),
            self.deriv.scale, 1.7,
            self.deriv.to_corner, UP+LEFT, MED_LARGE_BUFF,
            self.deriv.shift, MED_SMALL_BUFF*DOWN,
        )
        self.wait()

    def show_tangent_slope(self):
        ss_group = self.get_secant_slope_group(
            0, self.neg_cos,
            dx = 0.001,
            secant_line_color = YELLOW,
            secant_line_length = 4,
        )

        self.play(*list(map(ShowCreation, ss_group)), run_time = 2)
        for count in range(2):
            for x in reversed(self.bounds):
                self.animate_secant_slope_group_change(
                    ss_group,
                    target_x = x,
                    run_time = 6,
                )
