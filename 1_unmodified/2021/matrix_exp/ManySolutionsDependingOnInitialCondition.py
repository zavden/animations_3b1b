# ==============================================================================
# Scene:      ManySolutionsDependingOnInitialCondition
# Source:     videos/_2021/matrix_exp.py (lines 3342-3593)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManySolutionsDependingOnInitialCondition.py ManySolutionsDependingOnInitialCondition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_1d_equation(r="r"):
    return OldTex(
        "{d \\over d{t}} x({t}) = {" + r + "} \\cdot x({t})",
        tex_to_color_map={
            "{t}": GREY_B,
            "{" + r + "}": BLUE,
            "=": WHITE,
        }
    )


class VideoWrapper(Scene):
    title = ""

    def construct(self):
        self.add(FullScreenRectangle())
        screen_rect = ScreenRectangle(height=6)
        screen_rect.set_stroke(BLUE_D, 1)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.to_edge(DOWN)
        self.add(screen_rect)

        title = OldTexText(self.title, font_size=90)
        if title.get_width() > screen_rect.get_width():
            title.set_width(screen_rect.get_width())
        title.next_to(screen_rect, UP)

        self.play(Write(title))
        self.wait()


class ManySolutionsDependingOnInitialCondition(VideoWrapper):
    def construct(self):
        # Setup graphs and equations
        axes = Axes(
            x_range=(0, 12),
            y_range=(0, 10),
            width=12,
            height=6,
        )
        axes.add(axes.get_x_axis_label("t"))
        axes.add(axes.get_y_axis_label("x"))
        axes.x_axis.add_numbers()
        equation = get_1d_equation("0.3").to_edge(UP)

        def get_graph(x0, r=0.3):
            return axes.get_graph(lambda t: np.exp(r * t) * x0)

        step = 0.05
        graphs = VGroup(*(
            get_graph(x0)
            for x0 in np.arange(step, axes.y_range[1], step)
        ))
        graphs.set_submobject_colors_by_gradient(BLUE_E, BLUE, TEAL, YELLOW)
        graphs.set_stroke(width=1)
        graph = get_graph(1)
        graph.set_color(BLUE)

        solution = OldTex(
            "x({t}) = e^{0.3 {t} } \\cdot x_0",
            tex_to_color_map={"{t}": GREY_B, "0.3": BLUE, "=": WHITE},
        )
        solution.next_to(equation, DOWN, LARGE_BUFF)
        solution.shift(0.25 * RIGHT)
        solution[-1][1:].set_fill(MAROON_B)

        group = VGroup(solution, equation)
        group.set_stroke(BLACK, 5, background=True)
        group.shift(2 * LEFT)

        labels = VGroup(
            Text("Differential equation", font_size=30),
            Text("Solution", font_size=30),
        )
        labels.set_stroke(BLACK, 5, background=True)
        arrows = VGroup()
        for label, eq in zip(labels, [equation, solution[:-1]]):
            label.next_to(eq, RIGHT, buff=1.5)
            label.align_to(labels[0], LEFT)
            arrows.add(Arrow(label, eq))

        eq_label, sol_label = labels
        eq_arrow, sol_arrow = arrows

        # Show many possible representations
        alt_rhs = OldTex(
            "&= 2^{(0.4328\\dots) t }\\\\",
            "&= 3^{(0.2730\\dots) t }\\\\",
            "&= 4^{(0.2164\\dots) t }\\\\",
            "&= 5^{(0.1864\\dots) t }\\\\",
        )
        alt_rhs.next_to(solution.get_part_by_tex("="), DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        alt_rhs.set_stroke(BLACK, 5, background=True)

        choice_words = Text("This is a choice!", color=YELLOW, font_size=24)
        choice_words.next_to(solution[:-1], RIGHT, MED_LARGE_BUFF)
        choice_words.set_stroke(BLACK, 5, background=True)

        self.add(axes)
        self.add(solution[:-1])

        self.play(ShowCreation(graph, run_time=3))
        self.wait()
        self.play(FlashAround(solution.get_part_by_tex("e"), time_width=2, buff=0.05, run_time=2))
        self.wait()
        self.play(LaggedStartMap(FadeIn, alt_rhs, shift=0.5 * DOWN, lag_ratio=0.6, run_time=5))
        self.wait()
        self.play(
            alt_rhs.animate.set_opacity(0.4),
            FlashAround(solution[4:-1]),
            Write(choice_words, run_time=1)
        )
        self.wait()
        self.play(
            FadeTransform(solution[:3].copy(), equation[2:5]),  # x(t)
            FadeTransform(solution[:3].copy(), equation[7:10]),  # x(t)
            FadeTransform(solution[3].copy(), equation[5]),  # =
            FadeIn(equation[:2]),
            FadeOut(choice_words),
        )
        self.play(FadeTransform(solution[5].copy(), equation[6]))  # r
        self.wait()
        self.play(alt_rhs.animate.set_opacity(1.0))
        self.wait()
        self.play(LaggedStartMap(FadeOut, alt_rhs, shift=DOWN))
        for label, arrow in zip(labels, arrows):
            self.play(
                FadeIn(label, 0.5 * RIGHT),
                GrowArrow(arrow),
            )
            self.wait()

        # Just one solution
        one = Text("One", font_size=30)
        many = Text("out of many", font_size=30)
        one.move_to(sol_label.get_corner(UL), LEFT)
        sol_label.generate_target()
        group = VGroup(
            VGroup(one, sol_label.target).arrange(RIGHT, buff=MED_SMALL_BUFF, aligned_edge=DOWN),
            many
        )
        group.arrange(DOWN, buff=0.15)
        group.move_to(sol_label, LEFT)

        dot = Dot().scale(2 / 3)
        dot.move_to(axes.c2p(0, 0))

        self.add(graphs, graph, equation, solution[:-1], arrows, labels, one, many)
        self.play(
            MoveToTarget(sol_label, rate_func=squish_rate_func(smooth, 0, 0.5)),
            FadeIn(one),
            FadeIn(many),
            ShowIncreasingSubsets(graphs),
            dot.animate.move_to(axes.c2p(0, 10)),
            run_time=4,
        )
        self.wait()

        sol_label = VGroup(one, sol_label, many)

        # Initial conditions
        ic_label = Text("Initial conditions")
        ic_label.rotate(90 * DEGREES)
        ic_label.next_to(axes.y_axis, LEFT)

        x0_tracker = ValueTracker(1)
        get_x0 = x0_tracker.get_value
        x0_label = VGroup(
            OldTex("x_0 = ", font_size=36),
            DecimalNumber(1, font_size=36),
        )
        x0_label.set_color(MAROON_B)
        x0_label[1].match_height(x0_label[0])
        x0_label[1].next_to(x0_label[0][0][2], RIGHT, SMALL_BUFF)
        x0_label.add_updater(lambda m: m[1].set_value(get_x0()).set_color(MAROON_B))
        sv = x0_label.get_width() + MED_SMALL_BUFF
        x0_label.add_updater(lambda m: m.move_to(axes.c2p(0, get_x0()), LEFT).shift(sv * LEFT))

        self.play(
            Write(ic_label),
            run_time=1,
        )
        self.play(
            dot.animate.move_to(axes.c2p(0, 1)),
            graphs.animate.set_stroke(opacity=0.5),
            run_time=2,
        )
        self.wait()

        graph.add_updater(lambda g: g.match_points(get_graph(get_x0())))
        dot.add_updater(lambda d: d.move_to(axes.c2p(0, get_x0())))

        rect = BackgroundRectangle(x0_label)
        rect.set_fill(BLACK, 1)
        self.add(x0_label, rect, ic_label)
        self.play(
            FadeOut(rect),
            FadeOut(ic_label),
            self.camera.frame.animate.shift(0.6 * LEFT)
        )
        self.wait()
        self.play(
            x0_tracker.animate.set_value(0.1),
        )
        self.wait()
        for x in [5, 9]:
            self.play(
                x0_tracker.animate.set_value(x),
                run_time=5
            )
            self.wait()
            self.play(
                x0_tracker.animate.set_value(1),
                run_time=3,
            )
        self.wait()

        # Show general solution
        new_sol_label = Text("General solution", font_size=36)
        new_sol_label.move_to(sol_label, LEFT)

        self.play(
            TransformFromCopy(x0_label[0][0][:2], solution[-1]),
            sol_arrow.animate.become(Arrow(sol_label, solution))
        )
        self.play(
            FadeOut(sol_label),
            FadeIn(new_sol_label),
        )
        self.wait()

        rhs = solution[4:].copy()
        rhs_rect = SurroundingRectangle(rhs, stroke_width=2)
        rhs.generate_target()
        index = equation.index_of_part(equation.get_parts_by_tex("x")[1])
        rhs.target.move_to(equation[index], LEFT)
        rhs.target.shift(0.05 * UP)

        self.play(ShowCreation(rhs_rect))
        self.play(
            MoveToTarget(rhs),
            MaintainPositionRelativeTo(rhs_rect, rhs),
            FadeOut(equation[index:]),
            FadeOut(eq_arrow),
            FadeOut(eq_label),
        )
        self.play(FadeOut(rhs_rect))
        self.wait()
        self.play(x0_tracker.animate.set_value(2.5), run_time=2)
        self.play(x0_tracker.animate.set_value(0.5), run_time=2)
        self.wait()
        self.play(
            FadeOut(rhs),
            FadeIn(equation[index:]),
            FadeIn(eq_arrow),
            FadeIn(eq_label),
        )
        self.wait()

        # Emphasize solution vs action
        exp_rect = SurroundingRectangle(solution[4:7], buff=0.05, stroke_width=2)

        words1 = Text("Don't think of this\n\n as a solution", font_size=30)
        words2 = Text(
            "It's something which\n\nacts on an initial condition\n\nto give a solution",
            t2s={"acts": ITALIC},
            t2c={"acts": YELLOW, "initial condition": MAROON_B},
            font_size=30
        )
        for words in [words1, words2]:
            words.next_to(exp_rect, DOWN, MED_LARGE_BUFF)
            words.set_stroke(BLACK, 5, background=True)

        self.play(
            ShowCreation(exp_rect),
            Write(words1, run_time=1)
        )
        self.wait(2)
        self.play(
            FadeOut(words1),
            FadeIn(words2),
        )
        self.wait(2)
