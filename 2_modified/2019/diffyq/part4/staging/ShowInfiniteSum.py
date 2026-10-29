# ==============================================================================
# Scene:      ShowInfiniteSum
# Source:     videos/_2019/diffyq/part4/staging.py (lines 394-1045)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part3/staging.py
#
# Run from this folder:
#     manimgl ShowInfiniteSum.py ShowInfiniteSum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The final loop asked for 53 partial-sum transformations and n_range gives only 49 (StopIteration in Cairo too): it is trimmed from 40 to 36 steps.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part3/staging.py -----

class FourierSeriesIllustraiton(Scene):
    CONFIG = {
        "n_range": range(1, 31, 2),
        "axes_config": {
            "axis_config": {
                "include_tip": False,
            },
            "x_axis_config": {
                "tick_frequency": 1 / 4,
                "unit_size": 4,
            },
            "x_min": 0,
            "x_max": 1,
            "y_min": -1,
            "y_max": 1,
        },
        "colors": [BLUE, GREEN, RED, YELLOW, PINK],
    }

    def construct(self):
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.shift(2 * UP)
        aaa_group.shift_onto_screen()
        axes1, arrow, axes2 = aaa_group

        axes2.add(self.get_target_func_graph(axes2))

        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)

        sum_tex = self.get_sum_tex()
        sum_tex.next_to(axes1, DOWN, LARGE_BUFF)
        sum_tex.shift(RIGHT)
        eq = OldTex("=")
        target_func_tex = self.get_target_func_tex()
        target_func_tex.next_to(axes2, DOWN)
        target_func_tex.match_y(sum_tex)
        eq.move_to(midpoint(
            target_func_tex.get_left(),
            sum_tex.get_right()
        ))

        range_words = OldTexText(
            "For $0 \\le x \\le 1$"
        )
        range_words.next_to(
            VGroup(sum_tex, target_func_tex),
            DOWN,
        )

        rects = it.chain(
            [
                SurroundingRectangle(piece)
                for piece in self.get_sum_tex_pieces(sum_tex)
            ],
            it.cycle([None])
        )

        self.add(axes1, arrow, axes2)
        self.add(sum_tex, eq, target_func_tex)
        self.add(range_words)

        curr_partial_sum = axes1.get_graph(lambda x: 0)
        curr_partial_sum.set_stroke(width=1)
        for sine_graph, partial_sum, rect in zip(sine_graphs, partial_sums, rects):
            anims1 = [
                ShowCreation(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.set_stroke,
                {"width": 1, "opacity": 0.5},
                curr_partial_sum.set_stroke,
                {"width": 0, "background": True},
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            if rect:
                rect.match_style(sine_graph)
                anims1.append(ShowCreation(rect))
                anims2.append(FadeOut(rect))
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    def get_axes_arrow_axes(self):
        axes1 = Axes(**self.axes_config)
        axes1.x_axis.add_numbers(
            0.5, 1,
            num_decimal_places=1
        )
        axes1.y_axis.add_numbers(
            -1, 1,
            direction=LEFT,
            num_decimal_places=1,
        )
        axes2 = axes1.deepcopy()

        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        group = VGroup(axes1, arrow, axes2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        return group

    def get_sine_graphs(self, axes):
        sine_graphs = VGroup(*[
            axes.get_graph(self.generate_nth_func(n))
            for n in self.n_range
        ])
        sine_graphs.set_stroke(width=3)
        for graph, color in zip(sine_graphs, it.cycle(self.colors)):
            graph.set_color(color)
        return sine_graphs

    def get_partial_sums(self, axes, sine_graphs):
        partial_sums = VGroup(*[
            axes.get_graph(self.generate_kth_partial_sum_func(k + 1))
            for k in range(len(self.n_range))
        ])
        partial_sums.match_style(sine_graphs)
        return partial_sums

    def get_sum_tex(self):
        return OldTex(
            "\\frac{4}{\\pi} \\left(",
            "\\frac{\\cos(\\pi x)}{1}",
            "-\\frac{\\cos(3\\pi x)}{3}",
            "+\\frac{\\cos(5\\pi x)}{5}",
            "- \\cdots \\right)"
        ).scale(0.75)

    def get_sum_tex_pieces(self, sum_tex):
        return sum_tex[1:4]

    def get_target_func_tex(self):
        step_tex = OldTex(
            """
            1 \\quad \\text{if $x < 0.5$} \\\\
            0 \\quad \\text{if $x = 0.5$} \\\\
            -1 \\quad \\text{if $x > 0.5$} \\\\
            """
        )
        lb = Brace(step_tex, LEFT, buff=SMALL_BUFF)
        step_tex.add(lb)
        return step_tex

    def get_target_func_graph(self, axes):
        step_func = axes.get_graph(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
            color=YELLOW,
            stroke_width=3,
        )
        dot = Dot(axes.c2p(0.5, 0), color=step_func.get_color())
        dot.scale(0.5)
        step_func.add(dot)
        return step_func

    # def generate_nth_func(self, n):
    #     return lambda x: (4 / n / PI) * np.sin(TAU * n * x)

    def generate_nth_func(self, n):
        return lambda x: np.prod([
            (4 / PI),
            (1 / n) * (-1)**((n - 1) / 2),
            np.cos(PI * n * x)
        ])

    def generate_kth_partial_sum_func(self, k):
        return lambda x: np.sum([
            self.generate_nth_func(n)(x)
            for n in self.n_range[:k]
        ])



# ----- From _2019/diffyq/part4/staging.py -----

class ShowInfiniteSum(FourierSeriesIllustraiton):
    CONFIG = {
        "n_range": range(1, 101, 2),
        "colors": [BLUE, GREEN, RED, YELLOW, PINK],
        "axes_config": {
            "y_max": 1.5,
            "y_min": -1.5,
            "y_axis_config": {
                "tick_frequency": 0.5,
                "unit_size": 1.0,
                "stroke_width": 2,
            },
            "x_axis_config": {
                "tick_frequency": 0.1,
                "stroke_width": 2,
            },
        },
    }

    def construct(self):
        self.add_equation()
        self.add_graphs()
        self.show_to_infinity()
        self.walk_through_constants()

        self.ask_about_infinite_sum()
        self.show_inf_sum_of_numbers()
        self.show_many_inputs_in_parallel()
        self.follow_single_inputs()

    def add_equation(self):
        inf_sum = self.get_infinite_sum()
        step_func_def = self.get_step_func_definition()
        step_func_def.next_to(inf_sum, RIGHT)
        equation = VGroup(inf_sum, step_func_def)
        equation.set_width(FRAME_WIDTH - 1)
        equation.center().to_edge(UP)

        self.add(equation)

        self.equation = equation
        self.inf_sum = inf_sum
        self.inf_sum = inf_sum
        self.step_func_def = step_func_def

    def add_graphs(self):
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.next_to(self.equation, DOWN, buff=1.5)
        axes1, arrow, axes2 = aaa_group

        tfg = self.get_target_func_graph(axes2)
        tfg.set_color(WHITE)
        axes2.add(tfg)

        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)
        partial_sums.set_stroke(width=0.5)
        partial_sums[-1].set_stroke(width=2)
        colors = self.colors
        partial_sums[len(colors):].set_color_by_gradient(*colors)

        self.add(aaa_group)
        self.add(partial_sums)

        self.partial_sums = partial_sums
        self.sine_graphs = sine_graphs
        self.aaa_group = aaa_group

    def show_to_infinity(self):
        dots = self.inf_sum.dots
        arrow = Vector(1.5 * RIGHT)
        arrow.next_to(
            dots, DOWN, MED_LARGE_BUFF,
            aligned_edge=RIGHT
        )
        words = OldTexText("Sum to $\\infty$")
        words.next_to(arrow, DOWN)

        self.play(
            FadeIn(words, LEFT),
            GrowArrow(arrow)
        )
        self.wait()

        self.inf_words = VGroup(arrow, words)

    def walk_through_constants(self):
        inf_sum = self.inf_sum
        terms = self.inf_sum.terms
        sine_graphs = self.sine_graphs
        partial_sums = self.partial_sums

        rects = VGroup(*[
            SurroundingRectangle(
                term,
                color=term[-1].get_color(),
                stroke_width=2
            )
            for term in terms
        ])
        dots_rect = SurroundingRectangle(inf_sum.dots)
        dots_rect.set_stroke(width=2)

        curr_rect = rects[0].copy()
        curr_partial_sum = partial_sums[0]
        curr_partial_sum.set_stroke(width=3)

        self.play(
            FadeOut(partial_sums[1:]),
            FadeIn(curr_rect),
            FadeIn(curr_partial_sum),
        )

        for sg, ps, rect in zip(sine_graphs[1:], partial_sums[1:], rects[1:]):
            self.play(
                FadeOut(curr_rect),
                FadeIn(rect),
                FadeIn(sg),
            )
            curr_rect.become(rect)
            self.remove(rect)
            self.add(curr_rect)
            ps.set_stroke(width=3)
            self.play(
                curr_partial_sum.set_stroke, {"width": 0.5},
                ReplacementTransform(sg, ps),
            )
            curr_partial_sum = ps
        self.play(
            Transform(curr_rect, dots_rect),
            curr_partial_sum.set_stroke, {"width": 0.5},
            LaggedStart(
                *[
                    UpdateFromAlphaFunc(
                        ps,
                        lambda m, a: m.set_stroke(
                            width=(3 * there_and_back(a) + 0.5 * a)
                        ),
                    )
                    for ps in partial_sums[4:]
                ],
                run_time=3,
                lag_ratio=0.2,
            ),
        )
        self.play(partial_sums[-1].set_stroke, {"width": 2})
        self.play(
            FadeOut(curr_rect),
            ShowCreationThenFadeAround(inf_sum.four_over_pi),
        )
        self.wait()

    def ask_about_infinite_sum(self):
        inf_words = self.inf_words
        randy = Randolph(mode="confused")
        randy.set_height(1.5)

        outline = inf_words[1].copy()
        outline.set_stroke(YELLOW, 1)
        outline.set_fill(opacity=0)

        question = OldTexText(
            "What$\\dots$\\\\ does this mean?"
        )
        question.scale(0.7)
        question.next_to(inf_words, LEFT)
        randy.next_to(question, DOWN, aligned_edge=RIGHT)

        self.play(FadeIn(question))
        self.play(FadeIn(randy))
        self.play(
            Blink(randy),
            ShowCreationThenFadeOut(outline)
        )
        self.wait()
        self.play(FadeOut(randy), FadeOut(question))

    def show_inf_sum_of_numbers(self):
        inf_sum = self.inf_sum
        graph_group = VGroup(
            self.aaa_group, self.partial_sums
        )

        number_line = NumberLine(
            x_min=0,
            x_max=1,
            tick_frequency=0.1,
            big_tick_numbers=[0, 0.5, 1],
            unit_size=8,
            # line_to_number_buff=0.4,
        )
        number_line.set_stroke(GREY_B, 2)
        number_line.move_to(2 * DOWN)
        number_line.add_numbers(
            *np.arange(0, 1.5, 0.5),
            num_decimal_places=1
        )

        num_inf_sum = OldTex(
            "{1 \\over 1}",
            "-{1 \\over 3}",
            "+{1 \\over 5}",
            "-{1 \\over 7}",
            "+{1 \\over 9}",
            "-{1 \\over 11}",
            "+\\cdots",
            "= {\\pi \\over 4}"
        )
        num_inf_sum.move_to(UP)

        self.play(
            FadeOut(graph_group, DOWN),
            FadeIn(number_line, UP),
            FadeOut(self.inf_words),
            *[
                TransformFromCopy(t1[-1:], t2)
                for t1, t2 in zip(
                    inf_sum.terms,
                    num_inf_sum,
                )
            ],
            TransformFromCopy(
                inf_sum.dots,
                num_inf_sum[-2],
            ),
            TransformFromCopy(
                inf_sum.dots,
                num_inf_sum[-4:-2]
            ),
            self.equation.set_opacity, 0.5,
        )
        self.play(Write(num_inf_sum[-1]))

        # Show sums
        terms = [
            u / n
            for u, n in zip(
                it.cycle([1, -1]),
                range(1, 1001, 2)
            )
        ]
        partial_sums = np.cumsum(terms)
        tip = ArrowTip(start_angle=-TAU / 4)
        value_tracker = ValueTracker(1)
        get_value = value_tracker.get_value
        tip.add_updater(
            lambda t: t.move_to(
                number_line.n2p(get_value()),
                DOWN,
            )
        )
        n_braces = 7
        braces = VGroup(*[
            Brace(num_inf_sum[:n], DOWN)
            for n in range(1, n_braces + 1)
        ])
        brace = braces[0].copy()
        decimal = DecimalNumber(
            0, num_decimal_places=6,
        )
        decimal.add_updater(lambda d: d.set_value(get_value()))
        decimal.add_updater(lambda d: d.next_to(tip, UP, SMALL_BUFF))

        term_count = VGroup(
            Integer(1), OldTexText("terms")
        )
        term_count_tracker = ValueTracker(1)
        term_count[0].set_color(YELLOW)
        term_count.add_updater(
            lambda m: m[0].set_value(term_count_tracker.get_value())
        )
        term_count.add_updater(lambda m: m.arrange(
            RIGHT, aligned_edge=DOWN
        ))
        term_count.add_updater(lambda m: m.next_to(brace, DOWN))

        pi_fourths_tip = ArrowTip(start_angle=90 * DEGREES)
        pi_fourths_tip.set_color(WHITE)
        pi_fourths_tip.move_to(
            number_line.n2p(PI / 4), UP,
        )
        pi_fourths_label = OldTex(
            "{\\pi \\over 4} ="
        )
        pi_fourths_value = DecimalNumber(
            PI / 4, num_decimal_places=4
        )
        pi_fourths_value.scale(0.8)
        pi_fourths_value.next_to(pi_fourths_label, RIGHT, buff=0.2)
        pi_fourths_label.add(pi_fourths_value)
        # pi_fourths_label.scale(0.7)
        pi_fourths_label.next_to(
            pi_fourths_tip, DOWN, MED_SMALL_BUFF,
            aligned_edge=LEFT,
        )

        self.play(
            LaggedStartMap(
                FadeIn, VGroup(
                    brace, tip, decimal,
                    term_count,
                )
            ),
            FadeIn(pi_fourths_tip),
            FadeIn(pi_fourths_label),
        )
        for ps, new_brace in zip(partial_sums[1:], braces[1:]):
            term_count_tracker.increment_value(1)
            self.play(
                Transform(brace, new_brace),
                value_tracker.set_value, ps,
            )
            self.leave_mark(number_line, ps)
            self.wait()

        count = 0
        num_moving_values = n_braces + 8
        for ps in partial_sums[n_braces:num_moving_values]:
            value_tracker.set_value(ps)
            self.leave_mark(number_line, ps)
            count += 1
            term_count_tracker.increment_value(1)
            self.wait(0.5)
        decimal.remove_updater(decimal.updaters[-1])
        decimal.match_x(pi_fourths_tip)

        new_marks = VGroup(*[
            self.leave_mark(number_line, ps)
            for ps in partial_sums[num_moving_values:]
        ])
        number_line.remove(*new_marks)
        term_count_tracker.increment_value(1)
        self.play(
            UpdateFromAlphaFunc(
                value_tracker,
                lambda m, a: m.set_value(
                    partial_sums[integer_interpolate(
                        num_moving_values,
                        len(partial_sums) - 1,
                        a,
                    )[0]]
                ),
            ),
            ShowIncreasingSubsets(new_marks),
            term_count_tracker.set_value, len(partial_sums),
            run_time=10,
            rate_func=smooth,
        )
        self.play(LaggedStartMap(
            FadeOut, VGroup(
                num_inf_sum,
                brace,
                decimal,
                term_count,
                tip,
                number_line,
                new_marks,
                pi_fourths_tip,
                pi_fourths_label,
            ),
            lag_ratio=0.3,
        ))
        self.play(
            FadeInFromDown(graph_group),
            self.equation.set_opacity, 1,
        )

    def show_many_inputs_in_parallel(self):
        aaa_group = self.aaa_group
        axes1, arrow, axes2 = aaa_group
        partial_sums = self.partial_sums

        inputs = np.linspace(0, 1, 21)
        n_iterations = 100

        values = np.array([
            [
                (4 / PI) * (u / n) * np.cos(n * PI * x)
                for x in inputs
            ]
            for u, n in zip(
                it.cycle([1, -1]),
                range(1, 2 * n_iterations + 1, 2),
            )
        ])
        p_sums = np.apply_along_axis(np.cumsum, 0, values)

        dots = VGroup(*[Dot() for x in inputs])
        dots.scale(0.5)
        dots.set_color_by_gradient(BLUE, YELLOW)
        n_tracker = ValueTracker(0)

        def update_dots(dots):
            n = int(n_tracker.get_value())
            outputs = p_sums[n]
            for dot, x, y in zip(dots, inputs, outputs):
                dot.move_to(axes1.c2p(x, y))
        dots.add_updater(update_dots)

        lines = VGroup(*[
            self.get_dot_line(dot, axes1.x_axis)
            for dot in dots
        ])

        self.remove(*self.inf_words)
        self.play(
            FadeOut(partial_sums),
            FadeIn(dots),
            FadeIn(lines),
        )
        self.play(
            n_tracker.set_value, len(p_sums) - 1,
            run_time=5,
        )
        dots.clear_updaters()

        index = 4
        self.input_dot = dots[index]
        self.input_line = lines[index]
        self.partial_sum_values = p_sums[:, index]
        self.cosine_values = values[:, index]

        dots.remove(self.input_dot)
        lines.remove(self.input_line)
        self.add(self.input_line)
        self.add(self.input_dot)

        self.play(
            FadeOut(dots),
            FadeOut(lines),
        )

    def follow_single_inputs(self):
        aaa_group = self.aaa_group
        inf_sum = self.inf_sum
        axes1, arrow, axes2 = aaa_group
        x_axis = axes1.x_axis
        dot = self.input_dot
        partial_sums = self.partial_sums
        partial_sums.set_stroke(width=2)

        input_tracker = ValueTracker(
            x_axis.p2n(dot.get_center())
        )
        get_input = input_tracker.get_value

        input_label = OldTex("x =", "0.2")
        input_decimal = DecimalNumber(get_input())
        input_decimal.replace(input_label[1])
        input_decimal.set_color(BLUE)
        input_label.remove(input_label[1])
        input_label.add(input_decimal)
        input_label.next_to(dot, UR, SMALL_BUFF)

        def get_brace_value_label(brace, u, n):
            result = DecimalNumber()
            result.scale(0.7)
            result.next_to(brace, DOWN, SMALL_BUFF)
            result.add_updater(lambda d: d.set_value(
                (u / n) * np.cos(PI * n * get_input())
            ))
            return result

        braces = VGroup(*[
            Brace(term, DOWN)
            for term in inf_sum.terms
        ])
        brace_value_labels = VGroup(*[
            get_brace_value_label(brace, u, n)
            for brace, u, n in zip(
                braces,
                it.cycle([1, -1]),
                it.count(1, 2),
            )
        ])
        bv_rects = VGroup(*[
            SurroundingRectangle(
                brace_value_labels[:n],
                color=BLUE,
                stroke_width=1,
            )
            for n in range(1, len(braces) + 1)
        ])

        bv_rect = bv_rects[0].copy()
        partial_sum = partial_sums[0].copy()

        dot.add_updater(
            lambda d: d.move_to(partial_sum.point_from_proportion(
                inverse_interpolate(
                    x_axis.x_min,
                    x_axis.x_max,
                    get_input(),
                )
            ))
        )

        n_waves_label = OldTexText(
            "Sum of", "10", "waves"
        )
        n_waves_label.next_to(axes1.c2p(0.5, 1), UR)
        n_tracker = ValueTracker(1)
        n_dec = Integer(1)
        n_dec.set_color(YELLOW)
        n_dec.move_to(n_waves_label[1])
        n_waves_label[1].set_opacity(0)
        n_waves_label.add(n_dec)
        n_dec.add_updater(lambda n: n.set_value(
            n_tracker.get_value()
        ))
        n_dec.add_updater(lambda m: m.move_to(
            n_waves_label[1]
        ))

        self.play(
            FadeIn(input_label, LEFT),
            dot.scale, 1.5,
        )
        self.wait()
        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            LaggedStartMap(GrowFromCenter, brace_value_labels),
            *[
                TransformFromCopy(
                    input_label[0][0],
                    term[n][1],
                )
                for i, term in enumerate(inf_sum.terms)
                for n in [2 if i == 0 else 4]
            ]
        )
        self.wait()

        self.add(partial_sum, dot)
        dot.set_stroke(BLACK, 1, background=True)
        self.play(
            FadeOut(input_label),
            FadeIn(n_waves_label),
            FadeIn(bv_rect),
            FadeIn(partial_sum),
        )
        self.wait()

        ps_iter = iter(partial_sums[1:])

        def get_ps_anim():
            return AnimationGroup(
                Transform(partial_sum, next(ps_iter)),
                ApplyMethod(n_tracker.increment_value, 1),
            )

        for i in range(1, 4):
            self.play(
                Transform(bv_rect, bv_rects[i]),
                get_ps_anim(),
            )
            self.wait()

        self.play(
            FadeOut(bv_rect),
            get_ps_anim()
        )
        for x in range(3):
            self.play(get_ps_anim())
        self.play(
            input_tracker.set_value, 0.7,
        )
        for x in range(6):
            self.play(get_ps_anim())
        self.play(input_tracker.set_value, 0.5)
        # CHANGE: n_range gives 50 partial sums (49 after the first) and the original asked for 53 transformations (StopIteration); the last loop is trimmed
        for x in range(36):
            self.play(
                get_ps_anim(),
                run_time=0.5,
            )

    #
    def get_dot_line(self, dot, axis, line_class=Line):
        def get_line():
            p = dot.get_center()
            lp = axis.n2p(axis.p2n(p))
            return line_class(lp, p, stroke_width=1)
        return always_redraw(get_line)

    def leave_mark(self, number_line, value):
        tick = number_line.get_tick(value)
        tick.set_color(BLUE)
        number_line.add(tick)
        return tick

    def get_infinite_sum(self):
        colors = self.colors
        inf_sum = OldTex(
            "{4 \\over \\pi}", "\\left(",
            "{\\cos\\left({1}\\pi x\\right) \\over {1}}",
            "-",
            "{\\cos\\left({3}\\pi x\\right) \\over {3}}",
            "+",
            "{\\cos\\left({5}\\pi x\\right) \\over {5}}",
            "-",
            "{\\cos\\left({7}\\pi x\\right) \\over {7}}",
            "+",
            "\\cdots",
            "\\right)",
            tex_to_color_map={
                "{1}": colors[0],
                "{-1 \\over 3}": colors[1],
                "{3}": colors[1],
                "{1 \\over 5}": colors[2],
                "{5}": colors[2],
                "{-1 \\over 7}": colors[3],
                "{7}": colors[3],
                "{1 \\over 9}": colors[4],
                "{9}": colors[4],
            }
        )
        inf_sum.get_parts_by_tex("-")[0].set_color(colors[1])
        inf_sum.get_parts_by_tex("-")[1].set_color(colors[3])
        inf_sum.get_parts_by_tex("+")[0].set_color(colors[2])

        inf_sum.terms = VGroup(
            inf_sum[2:6],
            inf_sum[6:12],
            inf_sum[12:18],
            inf_sum[18:24],
        )
        inf_sum.dots = inf_sum.get_part_by_tex("\\cdots")
        inf_sum.four_over_pi = inf_sum.get_part_by_tex(
            "{4 \\over \\pi}"
        )

        return inf_sum

    def get_step_func_definition(self):
        values = VGroup(*map(Integer, [1, 0, -1]))
        conditions = VGroup(*map(TexText, [
            "if $x < 0.5$",
            "if $x = 0.5$",
            "if $x > 0.5$",
        ]))
        values.arrange(DOWN, buff=MED_LARGE_BUFF)
        for condition, value in zip(conditions, values):
            condition.move_to(value)
            condition.align_to(conditions[0], LEFT)
        conditions.next_to(values, RIGHT, LARGE_BUFF)
        brace = Brace(values, LEFT)

        eq = OldTex("=")
        eq.scale(1.5)
        eq.next_to(brace, LEFT)

        return VGroup(eq, brace, values, conditions)
