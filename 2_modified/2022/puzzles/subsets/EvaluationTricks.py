# ==============================================================================
# Scene:      EvaluationTricks
# Source:     videos/_2022/puzzles/subsets.py (lines 2075-2365)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EvaluationTricks.py EvaluationTricks -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - load_mobject('f_of_neg1.mob') (file from Grant's Dropbox) -> the Tex that the original left commented out
# ==============================================================================

from manim_imports_ext import *

class EvaluationTricks(InteractiveScene):
    def construct(self):
        # Setup function
        def func(x, n=10):
            return np.product([1 + x**n for n in range(1, n + 1)])

        plane = NumberPlane(
            (-1, 1),
            (-10, 10, 5),
            width=10,
            faded_line_ratio=4,
        )
        plane.set_height(FRAME_HEIGHT)
        plane.to_edge(LEFT, buff=0)
        plane.add_coordinate_labels(x_values=[-1, 1], y_values=range(-10, 15, 5))
        for cl in plane.x_axis.numbers:
            cl.shift_onto_screen(buff=SMALL_BUFF)
        graph = plane.get_graph(func, x_range=(-1, 1, 0.05))
        graph.set_stroke(YELLOW, 2)
        self.disable_interaction(plane)

        tex_kw = dict(tex_to_color_map={"x": BLUE})
        factored = Tex("f(x) = (1 + x)(1 + x^2)(1 + x^3) \\cdots (1 + x^{2{,}000})", **tex_kw)
        factored.to_corner(UR)
        expanded = VGroup(
            Tex("f(x) = ", **tex_kw),
            Tex("\\sum_{n = 0}^{N} c_n x^n", **tex_kw),
            # Tex("= 1+x+x^{2}+2 x^{3}+2 x^{4}+ \\cdots", **tex_kw)
            Tex("= c_0 + c_1 x + c_2 x^{2} + c_3 x^{3} + \\cdots", **tex_kw)
        )
        expanded.arrange(RIGHT, buff=0.2)
        expanded.next_to(factored, DOWN, LARGE_BUFF, LEFT)

        factored_label = Text("What we know", color=TEAL_B)
        expanded_label = Text("What we want", color=TEAL_C)
        for label, expr in [(factored_label, factored), (expanded_label, expanded)]:
            label.next_to(expr, LEFT, LARGE_BUFF)
            expr.arrow = Arrow(label, expr)

        self.add(factored)
        self.play(
            Write(factored_label),
            ShowCreation(factored.arrow),
        )
        self.wait()
        self.play(FadeTransform(factored.copy(), expanded))
        self.play(
            Write(expanded_label),
            ShowCreation(expanded.arrow),
        )
        self.wait()

        # Black box
        lhs = expanded[0]
        rhs = expanded[2]
        box = SurroundingRectangle(rhs[1:])
        box.set_stroke(WHITE, 1)
        box.set_fill(GREY_E, 1)
        q_marks = Tex("?").get_grid(1, 7, buff=0.7)
        q_marks.move_to(box)
        box.add(q_marks)

        self.play(FadeIn(box, lag_ratio=0.25, run_time=2))
        self.wait()

        # Show example evaluations
        x_tracker = ValueTracker(0.5)
        get_x = x_tracker.get_value
        dot = GlowDot(color=WHITE)
        dot.add_updater(lambda m: m.move_to(plane.i2gp(get_x(), graph)))
        line = Line(DOWN, UP).set_stroke(WHITE, 1)
        line.add_updater(lambda l: l.put_start_and_end_on(
            plane.c2p(get_x(), 0),
            plane.i2gp(get_x(), graph)
        ))

        self.play(
            Write(plane, lag_ratio=0.01),
            LaggedStartMap(FadeOut, VGroup(factored_label, expanded_label, factored.arrow, expanded.arrow)),
        )
        self.play(ShowCreation(graph))
        self.wait()
        self.play(
            ShowCreation(line),
            FadeInFromPoint(dot, line.get_start()),
        )
        self.play(x_tracker.animate.set_value(-0.5), run_time=2)
        self.play(x_tracker.animate.set_value(0.7), run_time=2)
        self.wait()

        # Plug in 0
        f0 = Tex("f(0) = 1", tex_to_color_map={"0": BLUE})
        f0[-1].set_opacity(0)
        f0.next_to(expanded, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        c0_rhs = Tex("= c_0")
        c0_rhs.next_to(f0, RIGHT)
        c0_rhs.shift(0.05 * DOWN)

        self.play(FadeTransform(lhs.copy(), f0))
        self.play(x_tracker.animate.set_value(0))
        self.wait(note="Move box out of the way")
        f0.set_opacity(1)
        self.play(Write(f0[-1]))
        self.add(f0)
        self.wait()
        self.play(Write(c0_rhs))
        f0.add(c0_rhs)

        # Take derivative at 0
        dkw = dict(tex_to_color_map={"0": BLUE})
        f_prime_0 = Tex("f'(0) = c_1", **dkw)
        f_prime_n = Tex("\\frac{1}{n!} f^{(n)}(0) = c_n", **dkw)
        f_prime_0.next_to(f0, RIGHT, buff=1.5)
        f_prime_n.next_to(f_prime_0, DOWN, MED_LARGE_BUFF, LEFT)

        tan_line = plane.get_graph(lambda x: x + 1)
        tan_line.set_stroke(PINK, 2, 0.8)

        self.play(FadeTransform(f0.copy(), f_prime_0))
        self.add(tan_line, dot)
        self.play(ShowCreation(tan_line))
        self.wait(note="Comment on derivative")

        self.play(FadeTransform(f_prime_0.copy(), f_prime_n))
        self.wait(note="Comment on this being a nightmare")

        crosses = VGroup(*map(Cross, (f_prime_0, f_prime_n)))
        crosses.insert_n_curves(20)
        self.play(ShowCreation(crosses))
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(f_prime_0, f_prime_n, *crosses)))

        # Plug in 1
        f1 = Tex(
            "f({1}) \\,=\\, 2^{2{,}000} \\,=\\, c_0 + c_1 + c_2 + c_3 + \\cdots + c_N",
            tex_to_color_map={
                "2^{2{,}000}": TEAL,
                "{1}": BLUE,
                "=": WHITE,
            }
        )
        f1.move_to(f0, LEFT)
        self.play(
            TransformFromCopy(factored[:5], f1[:5]),
            f0.animate.shift(2 * DOWN),
        )
        self.wait()
        self.play(
            Write(f1[5:11]),
            x_tracker.animate.set_value(1)
        )
        self.wait(note="Comment on factored form")
        self.play(Write(f1[11:]))
        self.add(f1)

        # Plug in -1
        # CHANGE: f_of_neg1.mob (mobject saved in Grant's Dropbox) is replaced by the Tex that the original itself left commented out
        fm1 = Tex(
            "f({-1}) \\,=\\, {0} \\,=\\,"
            "c_0 - c_1 + c_2 - c_3 + \\cdots + c_N",
            tex_to_color_map={
                "{-1}": RED,
                "{0}": TEAL,
                "=": WHITE,
            }
        )
        fm1.next_to(f1, DOWN, LARGE_BUFF, LEFT)

        self.play(
            TransformMatchingShapes(f1[:5].copy(), fm1[:5]),
            FadeOut(f0, DOWN)
        )
        self.wait()
        self.play(
            Write(fm1[5:7]),
            ApplyMethod(x_tracker.set_value, -1, run_time=3)
        )
        self.wait()
        self.play(Write(fm1[7:]))
        self.wait()

        # Show filtration expression
        f1_group = VGroup(f1, fm1)
        self.play(
            FadeOut(expanded),
            FadeOut(box),
            f1_group.animate.move_to(expanded, UL),
        )

        h_line = Line(LEFT, RIGHT).match_width(f1_group)
        h_line.set_stroke(GREY_B, 3)
        h_line.next_to(f1_group, DOWN, MED_LARGE_BUFF)
        h_line.stretch(1.05, 0, about_edge=LEFT)

        filter_expr = Tex(
            "{1 \\over 2} \\Big(f({1}) + f({-1})\\Big)"
            "= c_0 + c_2 + c_4 + \\cdots + c_{N}",
            tex_to_color_map={
                "{1}": BLUE,
                "{-1}": RED,
            }
        )
        filter_expr.next_to(h_line, DOWN, MED_LARGE_BUFF)
        filter_expr.align_to(f1_group, LEFT)

        self.play(
            ShowCreation(h_line),
            TransformFromCopy(f1[:4], filter_expr[4:8]),
            TransformFromCopy(fm1[:4], filter_expr[9:14]),
            Write(filter_expr[:4]),
            Write(filter_expr[8]),
            Write(filter_expr[14:16]),
        )
        self.wait()
        self.play(Write(filter_expr[16:]))
        self.wait()

        # Clarify goal
        parens = Tex("()")
        words = OldTexText("Some clever\\\\evaluation of $f$", font_size=36)
        words.set_color(WHITE)
        parens.match_height(words)
        parens[0].next_to(words, LEFT, buff=SMALL_BUFF)
        parens[1].next_to(words, RIGHT, buff=SMALL_BUFF)
        desire = VGroup(
            VGroup(parens, words),
            Tex("= c_0 + c_5 + c_{10} + \\cdots + c_{N}")
        )
        desire.arrange(RIGHT)
        desire.next_to(expanded, DOWN, 1.0, LEFT)

        self.play(
            FadeIn(expanded),
            FadeOut(f1_group, DOWN),
            Uncreate(h_line),
            filter_expr.animate.to_edge(DOWN),
        )
        self.wait()
        self.play(
            FadeIn(desire, DOWN),
        )
        self.wait()

        # Show random values of f
        self.play(
            x_tracker.animate.set_value(0.5),
            FadeOut(tan_line),
        )
        self.wait(0.5)
        for n in range(8):
            self.play(
                x_tracker.animate.set_value(random.uniform(-1, 1)),
                run_time=0.5,
            )
            self.wait(0.5)
        self.play(FadeOut(dot), FadeOut(line))

        # Indicator on x^n
        new_rhs = expanded[1]
        rect = SurroundingRectangle(new_rhs.get_part_by_tex("x^n"), buff=0.05)
        rect.set_stroke(BLUE_B, 2)
        rect.round_corners()

        outcomes = VGroup(
            OldTexText("$1$ if $\\; 5 \\mid n$", font_size=36, color=GREEN),
            OldTexText("$0$ if $\\; 5 \\nmid n$", font_size=36, color=RED_D),
        )
        outcomes.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        outcomes.next_to(new_rhs, RIGHT, 1.5, UP)
        arrows = VGroup(*(
            Arrow(
                rect.get_right(), outcome.get_left(),
                buff=0.25,
                color=outcome.get_color(),
                stroke_width=2.0
            )
            for outcome in outcomes
        ))

        self.play(
            ShowCreation(rect),
            FadeOut(expanded[2]),
        )
        self.wait(0.25)
        for arrow, outcome in zip(arrows, outcomes):
            self.play(
                ShowCreation(arrow),
                GrowFromPoint(outcome, rect.get_right())
            )
            self.wait()
