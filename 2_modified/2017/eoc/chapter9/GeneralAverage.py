# ==============================================================================
# Scene:      GeneralAverage
# Source:     videos/_2017/eoc/chapter9.py (lines 1420-1722)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GeneralAverage.py GeneralAverage -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
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


class GeneralAverage(AverageOfContinuousVariable):
    CONFIG = {
        "bounds" : [1, 6],
        "bound_colors" : [GREEN, RED],
        "graph_origin" : 5*LEFT + 2*DOWN,
        "num_rect_iterations" : 4,
        "max_dx" : 0.25,
    }
    def construct(self):
        self.setup_axes()
        self.add_graph()
        self.ask_about_average()
        self.show_signed_area()
        self.put_area_away()
        self.show_finite_sample()
        self.show_improving_samples()

    def add_graph(self):
        graph = self.get_graph(self.func)
        graph_label = self.get_graph_label(graph, "f(x)")
        v_lines = VGroup(*[
            self.get_vertical_line_to_graph(
                x, graph, line_class = DashedLine
            )
            for x in self.bounds
        ])
        for line, color in zip(v_lines, self.bound_colors):
            line.set_color(color)
        # CHANGE: Grant's repo renamed TexMobject->Tex here (new GL class); the 2017 code needs the Cairo-style OldTex
        labels = list(map(OldTex, "ab"))
        for line, label in zip(v_lines, labels):
            vect = line.get_start()-line.get_end()
            label.next_to(line, vect/get_norm(vect))
            label.set_color(line.get_color())

        self.y_axis_label_mob.shift(0.7*LEFT)

        self.play(
            ShowCreation(graph),
            Write(
                graph_label, 
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
            run_time = 2
        )
        for line, label in zip(v_lines, labels):
            self.play(
                Write(label),
                ShowCreation(line)
            )
        self.wait()

        self.graph = graph
        self.graph_label = graph_label
        self.bounds_labels = labels
        self.bound_lines = v_lines

    def ask_about_average(self):
        v_line = self.get_vertical_line_to_graph(
            self.bounds[0], self.graph, 
            line_class = DashedLine,
            color = WHITE
        )
        average = OldTexText("Average = ")
        fraction = OldTex(
            "{\\displaystyle \\int", "^b", "_a", "f(x)", "\\,dx",
            "\\over", "b", "-", "a}"
        )
        for color, tex in zip(self.bound_colors, "ab"):
            fraction.set_color_by_tex(tex, color)
        fraction.set_color_by_tex("displaystyle", WHITE)
        integral = VGroup(*fraction[:5])
        denominator = VGroup(*fraction[5:])
        average.next_to(fraction.get_part_by_tex("over"), LEFT)
        group = VGroup(average, fraction)
        group.center().to_edge(UP).shift(LEFT)

        self.count = 0
        def next_v_line_anim():
            target = self.bounds[0] if self.count%2 == 1 else self.bounds[1]
            self.count += 1
            return self.get_v_line_change_anim(
                v_line, self.graph, target,
                run_time = 4,
            )

        self.play(
            next_v_line_anim(),
            Write(average, run_time = 2),
        )
        self.play(
            next_v_line_anim(),
            Write(
                VGroup(*[
                    fraction.get_part_by_tex(tex)
                    for tex in ("int", "f(x)", "dx", "over")
                ]),
                rate_func = squish_rate_func(smooth, 0.25, 0.75),
                run_time = 4
            ),
            *[
                ReplacementTransform(
                    label.copy(),
                    fraction.get_part_by_tex(tex, substring = False),
                    run_time = 2
                )
                for label, tex in zip(
                    self.bounds_labels, 
                    ["_a", "^b"]
                )
            ]
        )
        self.play(
            next_v_line_anim(),
            Write(
                fraction.get_part_by_tex("-"),
                run_time = 4,
                rate_func = squish_rate_func(smooth, 0.5, 0.75),
            ),
            *[
                ReplacementTransform(
                    label.copy(),
                    fraction.get_part_by_tex(tex, substring = False),
                    run_time = 4,
                    rate_func = squish_rate_func(smooth, 0.25, 0.75)
                )
                for label, tex in zip(
                    self.bounds_labels, 
                    ["a}", "b"]
                )
            ]

        )
        self.play(next_v_line_anim())
        self.play(FadeOut(v_line))

        self.average_expression = VGroup(average, fraction)

    def show_signed_area(self):
        rect_list = self.get_riemann_rectangles_list(
            self.graph,
            self.num_rect_iterations,
            max_dx = self.max_dx,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
            end_color = BLUE,
            fill_opacity = 0.75,
            stroke_width = 0.25,
        )
        rects = rect_list[0]
        plus = OldTex("+")
        plus.move_to(self.coords_to_point(2, 2))
        minus = OldTex("-")
        minus.move_to(self.coords_to_point(5.24, -1))

        self.play(FadeIn(
            rects, 
            run_time = 2,
            lag_ratio = 0.5
        ))
        for new_rects in rect_list[1:]:
            self.transform_between_riemann_rects(rects, new_rects)
        self.play(Write(plus))
        self.play(Write(minus))
        self.wait(2)

        self.area = VGroup(rects, plus, minus)

    def put_area_away(self):
        self.play(
            FadeOut(self.area),
            self.average_expression.scale, 0.75,
            self.average_expression.to_corner, DOWN+RIGHT,
        )
        self.wait()

    def show_finite_sample(self):
        v_lines = self.get_vertical_lines_to_graph(
            self.graph,
            x_min = self.bounds[0],
            x_max = self.bounds[1],
            color = GREEN
        )
        for line in v_lines:
            if self.y_axis.point_to_number(line.get_end()) < 0:
                line.set_color(RED)
            line.save_state()

        line_pair = VGroup(*v_lines[6:8])
        brace = Brace(line_pair, DOWN)
        dx = brace.get_text("$dx$")

        num_samples = OldTexText("Num. samples")
        approx = OldTex("\\approx")
        rhs = OldTex("{b", "-", "a", "\\over", "dx}")
        for tex, color in zip("ab", self.bound_colors):
            rhs.set_color_by_tex(tex, color)
        expression = VGroup(num_samples, approx, rhs)
        expression.arrange(RIGHT)
        expression.next_to(self.y_axis, RIGHT)
        rhs_copy = rhs.copy()

        f_brace = Brace(line_pair, LEFT, buff = 0)
        f_x = f_brace.get_text("$f(x)$")
        add_up_f_over = OldTex("\\text{Add up $f(x)$}", "\\over")
        add_up_f_over.next_to(num_samples, UP)
        add_up_f_over.to_edge(UP)


        self.play(ShowCreation(v_lines, run_time = 2))
        self.play(*list(map(Write, [brace, dx])))
        self.wait()
        self.play(Write(VGroup(num_samples, approx, *rhs[:-1])))
        self.play(ReplacementTransform(
            dx.copy(), rhs.get_part_by_tex("dx")
        ))
        self.wait(2)

        self.play(
            FadeIn(add_up_f_over),
            *[
                ApplyFunction(
                    lambda m : m.fade().set_stroke(width = 2),
                    v_line
                )
                for v_line in v_lines
            ]
        )
        self.play(*[
            ApplyFunction(
                lambda m : m.restore().set_stroke(width = 5),
                v_line,
                run_time = 3,
                rate_func = squish_rate_func(
                    there_and_back, a, a+0.2
                )
            )
            for v_line, a in zip(v_lines, np.linspace(0, 0.8, len(v_lines)))
        ])
        self.play(*[vl.restore for vl in v_lines])
        self.play(rhs_copy.next_to, add_up_f_over, DOWN)
        self.wait(2)
        frac_line = add_up_f_over[1]
        self.play(
            FadeOut(rhs_copy.get_part_by_tex("over")),
            rhs_copy.get_part_by_tex("dx").next_to,
                add_up_f_over[0], RIGHT, SMALL_BUFF,
            frac_line.scale_about_point, 1.2, frac_line.get_left(),
            frac_line.stretch_to_fit_height, frac_line.get_height(),
        )
        rhs_copy.remove(rhs_copy.get_part_by_tex("over"))
        self.wait(2)

        int_fraction = self.average_expression[1].copy()
        int_fraction.generate_target()
        int_fraction.target.next_to(add_up_f_over, RIGHT, LARGE_BUFF)
        int_fraction.target.shift_onto_screen()
        double_arrow = OldTex("\\Leftrightarrow")
        double_arrow.next_to(
            int_fraction.target.get_part_by_tex("over"), LEFT
        )

        self.play(
            MoveToTarget(int_fraction),
            VGroup(add_up_f_over, rhs_copy).shift, 0.4*DOWN
        )
        self.play(Write(double_arrow))
        self.play(*list(map(FadeOut, [
            dx, brace, num_samples, approx, rhs
        ])))
        self.wait()

        self.v_lines = v_lines

    def show_improving_samples(self):
        stroke_width = self.v_lines[0].get_stroke_width()
        new_v_lines_list = [
            self.get_vertical_lines_to_graph(
                self.graph,
                x_min = self.bounds[0],
                x_max = self.bounds[1],
                num_lines = len(self.v_lines)*(2**n),
                color = GREEN,
                stroke_width = float(stroke_width)/n
            )
            for n in range(1, 4)
        ]
        for new_v_lines in new_v_lines_list:
            for line in new_v_lines:
                if self.y_axis.point_to_number(line.get_end()) < 0:
                    line.set_color(RED)

        for new_v_lines in new_v_lines_list:
            self.play(Transform(
                self.v_lines, new_v_lines,
                run_time = 2,
                lag_ratio = 0.5
            ))
        self.wait()

    ####

    def func(self, x):
        return 0.09*(x+1)*(x-4)*(x-8)
