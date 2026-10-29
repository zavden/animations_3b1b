# ==============================================================================
# Scene:      BayesRuleWithPdf
# Source:     videos/_2020/beta/beta3.py (lines 1556-1677)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/beta2.py, _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl BayesRuleWithPdf.py BayesRuleWithPdf -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

def close_off_graph(axes, graph):
    x_max = axes.x_axis.p2n(graph.get_end())
    graph.add_line_to(axes.c2p(x_max, 0))
    graph.add_line_to(axes.c2p(0, 0))
    return graph


def get_beta_graph(axes, n_plus, n_minus, **kwargs):
    dist = scipy.stats.beta(n_plus + 1, n_minus + 1)
    graph = axes.get_graph(dist.pdf, **kwargs)
    close_off_graph(axes, graph)
    graph.set_stroke(BLUE, 2)
    graph.set_fill(BLUE_E, 1)
    return graph


def reverse_smooth(t):
    return smooth(1 - t)


def get_region_under_curve(axes, graph, min_x, max_x):
    props = [
        binary_search(
            function=lambda a: axes.x_axis.p2n(graph.pfp(a)),
            target=x,
            lower_bound=axes.x_min,
            upper_bound=axes.x_max,
        )
        for x in [min_x, max_x]
    ]
    region = graph.copy()
    region.pointwise_become_partial(graph, *props)
    region.add_line_to(axes.c2p(max_x, 0))
    region.add_line_to(axes.c2p(min_x, 0))
    region.add_line_to(region.get_start())

    region.set_stroke(GREEN, 2)
    region.set_fill(GREEN, 0.5)

    region.axes = axes
    region.graph = graph
    region.min_x = min_x
    region.max_x = max_x

    return region



# ----- From _2020/beta/beta2.py -----

class ShowLimitToPdf(Scene):
    def construct(self):
        # Init
        axes = self.get_axes()
        alpha = 4
        beta = 2
        dist = scipy.stats.beta(alpha, beta)
        bars = self.get_bars(axes, dist, 0.05)

        axis_prob_label = OldTexText("Probability")
        axis_prob_label.next_to(axes.y_axis, UP)
        axis_prob_label.to_edge(LEFT)

        self.add(axes)
        self.add(axis_prob_label)

        # From individual to ranges
        kw = {"tex_to_color_map": {"h": YELLOW}}
        eq_label = OldTex("P(h = 0.8)", **kw)
        ineq_label = OldTex("P(0.8 < h < 0.85)", **kw)

        arrows = VGroup(Vector(DOWN), Vector(DOWN))
        for arrow, x in zip(arrows, [0.8, 0.85]):
            arrow.move_to(axes.c2p(x, 0), DOWN)
        brace = Brace(
            Line(arrows[0].get_start(), arrows[1].get_start()),
            UP, buff=SMALL_BUFF
        )
        eq_label.next_to(arrows[0], UP)
        ineq_label.next_to(brace, UP)

        self.play(
            FadeIn(eq_label, 0.2 * DOWN),
            GrowArrow(arrows[0]),
        )
        self.wait()
        vect = eq_label.get_center() - ineq_label.get_center()
        self.play(
            FadeOut(eq_label, -vect),
            FadeIn(ineq_label, vect),
            TransformFromCopy(*arrows),
            GrowFromPoint(brace, brace.get_left()),
        )
        self.wait()

        # Bars
        arrow = arrows[0]
        arrow.generate_target()
        arrow.target.next_to(bars[16], UP, SMALL_BUFF)
        highlighted_bar_color = RED_E
        bars[16].set_color(highlighted_bar_color)

        for bar in bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)

        kw = {
            "run_time": 2,
            "rate_func": squish_rate_func(smooth, 0.3, 0.9),
        }
        self.play(
            MoveToTarget(arrow, **kw),
            ApplyMethod(ineq_label.next_to, arrows[0].target, UP, **kw),
            FadeOut(arrows[1]),
            FadeOut(brace),
            LaggedStartMap(Restore, bars, run_time=2, lag_ratio=0.025),
        )
        self.wait()

        # Focus on area, not height
        lines = VGroup()
        new_bars = VGroup()
        for bar in bars:
            line = Line(
                bar.get_corner(DL),
                bar.get_corner(DR),
            )
            line.set_stroke(YELLOW, 0)
            line.generate_target()
            line.target.set_stroke(YELLOW, 3)
            line.target.move_to(bar.get_top())
            lines.add(line)

            new_bar = bar.copy()
            new_bar.match_style(line)
            new_bar.set_fill(YELLOW, 0.5)
            new_bar.generate_target()
            new_bar.stretch(0, 1, about_edge=UP)
            new_bars.add(new_bar)

        prob_label = OldTexText(
            "Height",
            "$\\rightarrow$",
            "Probability",
        )
        prob_label.space_out_submobjects(1.1)
        prob_label.next_to(bars[10], UL, LARGE_BUFF)
        height_word = prob_label[0]
        height_cross = Cross(height_word)
        area_word = OldTexText("Area")
        area_word.move_to(height_word, UR)
        area_word.set_color(YELLOW)

        self.play(
            LaggedStartMap(
                MoveToTarget, lines,
                lag_ratio=0.01,
            ),
            FadeInFromDown(prob_label),
        )
        self.add(height_word)
        self.play(
            ShowCreation(height_cross),
            FadeOut(axis_prob_label, LEFT)
        )
        self.wait()
        self.play(
            FadeOut(height_word, UP),
            FadeOut(height_cross, UP),
            FadeInFromDown(area_word),
        )
        self.play(
            FadeOut(lines),
            LaggedStartMap(
                MoveToTarget, new_bars,
                lag_ratio=0.01,
            )
        )
        self.play(
            FadeOut(new_bars),
            area_word.set_color, BLUE,
        )

        prob_label = VGroup(area_word, *prob_label[1:])
        self.add(prob_label)

        # Ask about where values come from
        randy = Randolph(height=1)
        randy.next_to(prob_label, UP, aligned_edge=LEFT)

        bubble = SpeechBubble(
            height=2,
            width=4,
        )
        bubble.move_to(randy.get_corner(UR), DL)
        bubble.write("Where do these\\\\probabilities come from?")

        self.play(
            FadeIn(randy),
            ShowCreation(bubble),
        )
        self.play(
            randy.change, "confused",
            FadeIn(bubble.content, lag_ratio=0.1)
        )
        self.play(Blink(randy))

        bars.generate_target()
        bars.save_state()
        bars.target.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        bars.target.next_to(bars.get_bottom(), UP)

        self.play(MoveToTarget(bars))
        self.play(LaggedStartMap(Indicate, bars, scale_factor=1.05), run_time=1)
        self.play(Restore(bars))
        self.play(Blink(randy))
        self.play(
            FadeOut(randy),
            FadeOut(bubble),
            FadeOut(bubble.content),
        )

        # Refine
        last_ineq_label = ineq_label
        last_bars = bars
        all_ineq_labels = VGroup(ineq_label)
        for step_size in [0.025, 0.01, 0.005, 0.001]:
            new_bars = self.get_bars(axes, dist, step_size)
            new_ineq_label = OldTex(
                "P(0.8 < h < {:.3})".format(0.8 + step_size),
                tex_to_color_map={"h": YELLOW},
            )

            if step_size <= 0.005:
                new_bars.set_stroke(width=0)

            arrow.generate_target()
            bar = new_bars[int(0.8 * len(new_bars))]
            bar.set_color(highlighted_bar_color)
            arrow.target.next_to(bar, UP, SMALL_BUFF)
            new_ineq_label.next_to(arrow.target, UP)

            vect = new_ineq_label.get_center() - last_ineq_label.get_center()

            self.wait()
            self.play(
                ReplacementTransform(
                    last_bars, new_bars,
                    lag_ratio=step_size,
                ),
                MoveToTarget(arrow),
                FadeOut(last_ineq_label, vect),
                FadeIn(new_ineq_label, -vect),
                run_time=2,
            )
            last_ineq_label = new_ineq_label
            last_bars = new_bars
            all_ineq_labels.add(new_ineq_label)

        # Show continuous graph
        graph = get_beta_graph(axes, alpha - 1, beta - 1)
        graph_curve = axes.get_graph(dist.pdf)
        graph_curve.set_stroke([YELLOW, GREEN])

        limit_words = OldTexText("In the limit...")
        limit_words.next_to(
            axes.input_to_graph_point(0.75, graph_curve),
            UP, MED_LARGE_BUFF,
        )

        self.play(
            FadeIn(graph),
            FadeOut(last_ineq_label),
            FadeOut(arrow),
            FadeOut(last_bars),
        )
        self.play(
            ShowCreation(graph_curve),
            Write(limit_words, run_time=1)
        )
        self.play(FadeOut(graph_curve))
        self.wait()

        # Show individual probabilities goes to zero
        all_ineq_labels.arrange(DOWN, aligned_edge=LEFT)
        all_ineq_labels.move_to(prob_label, LEFT)
        all_ineq_labels.to_edge(UP)

        prob_label.generate_target()
        prob_label.target.next_to(
            all_ineq_labels, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )

        rhss = VGroup()
        step_sizes = [0.05, 0.025, 0.01, 0.005, 0.001]
        for label, step in zip(all_ineq_labels, step_sizes):
            eq = OldTex("=")
            decimal = DecimalNumber(
                dist.cdf(0.8 + step) - dist.cdf(0.8),
                num_decimal_places=3,
            )
            eq.next_to(label, RIGHT)
            decimal.next_to(eq, RIGHT)
            decimal.set_stroke(BLACK, 3, background=True)
            rhss.add(VGroup(eq, decimal))

        for rhs in rhss:
            rhs.align_to(rhss[1], LEFT)

        VGroup(all_ineq_labels, rhss).set_height(3, about_edge=UL)

        arrow = Arrow(rhss.get_top(), rhss.get_bottom(), buff=0)
        arrow.next_to(rhss, RIGHT)
        arrow.set_color(YELLOW)
        to_zero_words = OldTexText("Individual probabilites\\\\", "go to zero")
        to_zero_words[1].align_to(to_zero_words[0], LEFT)
        to_zero_words.next_to(arrow, RIGHT, aligned_edge=UP)

        self.play(
            LaggedStartMap(
                FadeInFrom, all_ineq_labels,
                lambda m: (m, UP),
            ),
            LaggedStartMap(
                FadeInFrom, rhss,
                lambda m: (m, UP),
            ),
            MoveToTarget(prob_label)
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(to_zero_words),
        )
        self.play(
            LaggedStartMap(
                Indicate, rhss,
                scale_factor=1.05,
            )
        )
        self.wait(2)

        # What if it was heights
        bars.restore()
        height_word.move_to(area_word, RIGHT)
        height_word.set_color(PINK)
        step = 0.05
        new_y_numbers = VGroup(*[
            DecimalNumber(x) for x in np.arange(step, 5 * step, step)
        ])
        for n1, n2 in zip(axes.y_axis.numbers, new_y_numbers):
            n2.match_height(n1)
            n2.add_background_rectangle(
                opacity=1,
                buff=SMALL_BUFF,
            )
            n2.move_to(n1, RIGHT)

        self.play(
            FadeOut(limit_words),
            FadeOut(graph),
            FadeIn(bars),
            FadeOut(area_word, UP),
            FadeIn(height_word, DOWN),
            FadeIn(new_y_numbers, 0.5 * RIGHT),
        )

        # Height refine
        rect = SurroundingRectangle(rhss[0][1])
        rect.set_stroke(RED, 3)
        self.play(FadeIn(rect))

        last_bars = bars
        for step_size, rhs in zip(step_sizes[1:], rhss[1:]):
            new_bars = self.get_bars(axes, dist, step_size)
            bar = new_bars[int(0.8 * len(new_bars))]
            bar.set_color(highlighted_bar_color)
            new_bars.stretch(
                step_size / 0.05, 1,
                about_edge=DOWN,
            )
            if step_size <= 0.05:
                new_bars.set_stroke(width=0)
            self.remove(last_bars)
            self.play(
                TransformFromCopy(last_bars, new_bars, lag_ratio=step_size),
                rect.move_to, rhs[1],
            )
            last_bars = new_bars
        self.play(
            FadeOut(last_bars),
            FadeOutAndShiftDown(rect),
        )
        self.wait()

        # Back to area
        self.play(
            FadeIn(graph),
            FadeIn(area_word, 0.5 * DOWN),
            FadeOut(height_word, 0.5 * UP),
            FadeOut(new_y_numbers, lag_ratio=0.2),
        )
        self.play(
            arrow.scale, 0, {"about_edge": DOWN},
            FadeOut(to_zero_words, DOWN),
            LaggedStartMap(FadeOutAndShiftDown, all_ineq_labels),
            LaggedStartMap(FadeOutAndShiftDown, rhss),
        )
        self.wait()

        # Ask about y_axis units
        arrow = Arrow(
            axes.y_axis.get_top() + 3 * RIGHT,
            axes.y_axis.get_top(),
            path_arc=90 * DEGREES,
        )
        question = OldTexText("What are the\\\\units here?")
        question.next_to(arrow.get_start(), DOWN)

        self.play(
            FadeIn(question, lag_ratio=0.1),
            ShowCreation(arrow),
        )
        self.wait()

        # Bring back bars
        bars = self.get_bars(axes, dist, 0.05)
        self.play(
            FadeOut(graph),
            FadeIn(bars),
        )
        bars.generate_target()
        bars.save_state()
        bars.target.set_opacity(0.2)
        bar_index = int(0.8 * len(bars))
        bars.target[bar_index].set_opacity(0.8)
        bar = bars[bar_index]

        prob_word = OldTexText("Probability")
        prob_word.rotate(90 * DEGREES)
        prob_word.set_height(0.8 * bar.get_height())
        prob_word.move_to(bar)

        self.play(
            MoveToTarget(bars),
            Write(prob_word, run_time=1),
        )
        self.wait()

        # Show dimensions of bar
        top_brace = Brace(bar, UP)
        side_brace = Brace(bar, LEFT)
        top_label = top_brace.get_tex("\\Delta x")
        side_label = side_brace.get_tex(
            "{\\text{Prob.} \\over \\Delta x}"
        )

        self.play(
            GrowFromCenter(top_brace),
            FadeIn(top_label),
        )
        self.play(GrowFromCenter(side_brace))
        self.wait()
        self.play(Write(side_label))
        self.wait()

        y_label = OldTexText("Probability density")
        y_label.next_to(axes.y_axis, UP, aligned_edge=LEFT)

        self.play(
            Uncreate(arrow),
            FadeOutAndShiftDown(question),
            Write(y_label),
        )
        self.wait(2)
        self.play(
            Restore(bars),
            FadeOut(top_brace),
            FadeOut(side_brace),
            FadeOut(top_label),
            FadeOut(side_label),
            FadeOut(prob_word),
        )

        # Point out total area is 1
        total_label = OldTexText("Total area = 1")
        total_label.set_height(0.5)
        total_label.next_to(bars, UP, LARGE_BUFF)

        self.play(FadeIn(total_label, DOWN))
        bars.save_state()
        self.play(
            bars.arrange, RIGHT, {"aligned_edge": DOWN, "buff": SMALL_BUFF},
            bars.move_to, bars.get_bottom() + 0.5 * UP, DOWN,
        )
        self.play(LaggedStartMap(Indicate, bars, scale_factor=1.05))
        self.play(Restore(bars))

        # Refine again
        for step_size in step_sizes[1:]:
            new_bars = self.get_bars(axes, dist, step_size)
            if step_size <= 0.05:
                new_bars.set_stroke(width=0)
            self.play(
                ReplacementTransform(
                    bars, new_bars, lag_ratio=step_size
                ),
                run_time=3,
            )
            self.wait()
            bars = new_bars
        self.add(graph, total_label)
        self.play(
            FadeIn(graph),
            FadeOut(bars),
            total_label.move_to, axes.c2p(0.7, 0.8)
        )
        self.wait()

        # Name pdf
        func_name = OldTexText("Probability ", "Density ", "Function")
        initials = OldTexText("P", "D", "F")
        for mob in func_name, initials:
            mob.set_color(YELLOW)
            mob.next_to(axes.input_to_graph_point(0.75, graph_curve), UP)

        self.play(
            ShowCreation(graph_curve),
            Write(func_name, run_time=1),
        )
        self.wait()
        func_name_copy = func_name.copy()
        self.play(
            func_name.next_to, initials, UP,
            *[
                ReplacementTransform(np[0], ip[0])
                for np, ip in zip(func_name_copy, initials)
            ],
            *[
                FadeOut(np[1:])
                for np in func_name_copy
            ]
        )
        self.add(initials)
        self.wait()
        self.play(
            FadeOut(func_name),
            FadeOut(total_label),
            FadeOut(graph_curve),
            initials.next_to, axes.input_to_graph_point(0.95, graph_curve), UR,
        )

        # Look at bounded area
        min_x = 0.6
        max_x = 0.8
        region = get_region_under_curve(axes, graph_curve, min_x, max_x)
        area_label = DecimalNumber(
            dist.cdf(max_x) - dist.cdf(min_x),
            num_decimal_places=3,
        )
        area_label.move_to(region)

        v_lines = VGroup()
        for x in [min_x, max_x]:
            v_lines.add(
                DashedLine(
                    axes.c2p(x, 0),
                    axes.c2p(x, 2.5),
                )
            )
        v_lines.set_stroke(YELLOW, 2)

        p_label = VGroup(
            OldTex("P("),
            DecimalNumber(min_x),
            OldTex("\\le"),
            OldTex("h", color=YELLOW),
            OldTex("\\le"),
            DecimalNumber(max_x),
            OldTex(")")
        )
        p_label.arrange(RIGHT, buff=0.25)
        VGroup(p_label[0], p_label[-1]).space_out_submobjects(0.92)
        p_label.next_to(v_lines, UP)

        rhs = VGroup(
            OldTex("="),
            area_label.copy()
        )
        rhs.arrange(RIGHT)
        rhs.next_to(p_label, RIGHT)

        self.play(
            FadeIn(p_label, 2 * DOWN),
            *map(ShowCreation, v_lines),
        )
        self.wait()
        region.func = get_region_under_curve
        self.play(
            UpdateFromAlphaFunc(
                region,
                lambda m, a: m.become(
                    m.func(
                        m.axes, m.graph,
                        m.min_x,
                        interpolate(m.min_x, m.max_x, a)
                    )
                )
            ),
            CountInFrom(area_label),
            UpdateFromAlphaFunc(
                area_label,
                lambda m, a: m.set_opacity(a),
            ),
        )
        self.wait()
        self.play(
            TransformFromCopy(area_label, rhs[1]),
            Write(rhs[0]),
        )
        self.wait()

        # Change range
        new_x = np.mean([min_x, max_x])
        area_label.original_width = area_label.get_width()
        region.new_x = new_x
        # Squish to area 1
        self.play(
            ChangeDecimalToValue(p_label[1], new_x),
            ChangeDecimalToValue(p_label[5], new_x),
            ChangeDecimalToValue(area_label, 0),
            UpdateFromAlphaFunc(
                area_label,
                lambda m, a: m.set_width(
                    interpolate(m.original_width, 1e-6, a)
                )
            ),
            ChangeDecimalToValue(rhs[1], 0),
            v_lines[0].move_to, axes.c2p(new_x, 0), DOWN,
            v_lines[1].move_to, axes.c2p(new_x, 0), DOWN,
            UpdateFromAlphaFunc(
                region,
                lambda m, a: m.become(m.func(
                    m.axes, m.graph,
                    interpolate(m.min_x, m.new_x, a),
                    interpolate(m.max_x, m.new_x, a),
                ))
            ),
            run_time=2,
        )
        self.wait()

        # Stretch to area 1
        self.play(
            ChangeDecimalToValue(p_label[1], 0),
            ChangeDecimalToValue(p_label[5], 1),
            ChangeDecimalToValue(area_label, 1),
            UpdateFromAlphaFunc(
                area_label,
                lambda m, a: m.set_width(
                    interpolate(1e-6, m.original_width, clip(5 * a, 0, 1))
                )
            ),
            ChangeDecimalToValue(rhs[1], 1),
            v_lines[0].move_to, axes.c2p(0, 0), DOWN,
            v_lines[1].move_to, axes.c2p(1, 0), DOWN,
            UpdateFromAlphaFunc(
                region,
                lambda m, a: m.become(m.func(
                    m.axes, m.graph,
                    interpolate(m.new_x, 0, a),
                    interpolate(m.new_x, 1, a),
                ))
            ),
            run_time=5,
        )
        self.wait()

    def get_axes(self):
        axes = Axes(
            x_min=0,
            x_max=1,
            x_axis_config={
                "tick_frequency": 0.05,
                "unit_size": 12,
                "include_tip": False,
            },
            y_min=0,
            y_max=4,
            y_axis_config={
                "tick_frequency": 1,
                "unit_size": 1.25,
                "include_tip": False,
            }
        )
        axes.center()

        h_label = OldTex("h")
        h_label.set_color(YELLOW)
        h_label.next_to(axes.x_axis.n2p(1), UR, buff=0.2)
        axes.x_axis.add(h_label)
        axes.x_axis.label = h_label

        axes.x_axis.add_numbers(
            *np.arange(0.2, 1.2, 0.2),
            num_decimal_places=1
        )
        axes.y_axis.add_numbers(*range(1, 5))
        return axes

    def get_bars(self, axes, dist, step_size):
        bars = VGroup()
        for x in np.arange(0, 1, step_size):
            bar = Rectangle()
            bar.set_stroke(BLUE, 2)
            bar.set_fill(BLUE, 0.5)
            h_line = Line(
                axes.c2p(x, 0),
                axes.c2p(x + step_size, 0),
            )
            v_line = Line(
                axes.c2p(0, 0),
                axes.c2p(0, dist.pdf(x)),
            )
            bar.match_width(h_line, stretch=True)
            bar.match_height(v_line, stretch=True)
            bar.move_to(h_line, DOWN)
            bars.add(bar)
        return bars



# ----- From _2020/beta/beta3.py -----

class BayesRuleWithPdf(ShowLimitToPdf):
    def construct(self):
        # Axes
        axes = self.get_axes()
        sf = 1.5
        axes.y_axis.stretch(sf, 1, about_point=axes.c2p(0, 0))
        for number in axes.y_axis.numbers:
            number.stretch(1 / sf, 1)
        self.add(axes)

        # Formula
        bayes = self.get_formula()

        post = bayes[:5]
        eq = bayes[5]
        prior = bayes[6:9]
        likelihood = bayes[9:14]
        over = bayes[14]
        p_data = bayes[15:]

        self.play(FadeInFromDown(bayes))
        self.wait()

        # Prior
        prior_graph = get_beta_graph(axes, 0, 0)
        prior_graph_top = Line(
            prior_graph.get_corner(UL),
            prior_graph.get_corner(UR),
        )
        prior_graph_top.set_stroke(YELLOW, 3)

        bayes.save_state()
        bayes.set_opacity(0.2)
        prior.set_opacity(1)

        self.play(
            Restore(bayes, rate_func=reverse_smooth),
            FadeIn(prior_graph),
            ShowCreation(prior_graph_top),
        )
        self.play(FadeOut(prior_graph_top))
        self.wait()

        # Scale Down
        nh = 1
        nt = 2

        scaled_graph = axes.get_graph(
            lambda x: scipy.stats.binom(3, x).pmf(1) + 1e-6
        )
        scaled_graph.set_stroke(GREEN)
        scaled_region = get_region_under_curve(axes, scaled_graph, 0, 1)

        def to_uniform(p, axes=axes):
            return axes.c2p(
                axes.x_axis.p2n(p),
                int(axes.y_axis.p2n(p) != 0),
            )

        scaled_region.set_fill(opacity=0.75)
        scaled_region.save_state()
        scaled_region.apply_function(to_uniform)

        self.play(
            Restore(scaled_region),
            UpdateFromAlphaFunc(
                scaled_region,
                lambda m, a: m.set_opacity(a * 0.75),
            ),
            likelihood.set_opacity, 1,
        )
        self.wait()

        # Rescale
        new_graph = get_beta_graph(axes, nh, nt)
        self.play(
            ApplyMethod(
                scaled_region.set_height, new_graph.get_height(),
                {"about_edge": DOWN, "stretch": True},
                run_time=2,
            ),
            over.set_opacity, 1,
            p_data.set_opacity, 1,
        )
        self.wait()
        self.play(
            post.set_opacity, 1,
            eq.set_opacity, 1,
        )
        self.wait()

        # Use lower case
        new_bayes = self.get_formula(lowercase=True)
        new_bayes.replace(bayes, dim_to_match=0)
        rects = VGroup(
            SurroundingRectangle(new_bayes[0][0]),
            SurroundingRectangle(new_bayes[6][0]),
        )
        rects.set_stroke(YELLOW, 3)

        self.remove(bayes)
        bayes = self.get_formula()
        self.add(bayes)
        self.play(Transform(bayes, new_bayes))
        self.play(ShowCreationThenFadeOut(rects))

    def get_formula(self, lowercase=False):
        p_sym = "p" if lowercase else "P"
        bayes = OldTex(
            p_sym + "({s} \\,|\\, \\text{data})", "=",
            "{" + p_sym + "({s})",
            "P(\\text{data} \\,|\\, {s})",
            "\\over",
            "P(\\text{data})",
            tex_to_color_map={
                "{s}": YELLOW,
                "\\text{data}": GREEN,
            }
        )
        bayes.set_height(1.5)
        bayes.to_edge(UP)
        return bayes
