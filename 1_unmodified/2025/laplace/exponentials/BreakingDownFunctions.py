# ==============================================================================
# Scene:      BreakingDownFunctions
# Source:     videos/_2025/laplace/exponentials.py (lines 1337-1578)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BreakingDownFunctions.py BreakingDownFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ForcedOscillatorSolutionForm(InteractiveScene):
    def construct(self):
        # Create linear combination
        exp_texs = [Rf"e^{{s_{n} t}}" for n in range(1, 5)]
        const_texs = [Rf"c_{n}" for n in range(1, 5)]
        terms = [" ".join(pair) for pair in zip(const_texs, exp_texs)]
        solution = Tex("x(t) = " + " + ".join(terms), isolate=[*exp_texs, *const_texs])
        solution.to_edge(RIGHT)

        solution[re.compile(r's_\w+')].set_color(YELLOW)
        solution[re.compile(r'c_\w+')].set_color(BLUE)

        cut_index = solution.submobjects.index(solution["+"][1][0])
        first_two = solution[:cut_index]
        last_two = solution[cut_index:]

        first_two.save_state()
        first_two.to_edge(RIGHT, buff=1.5)

        self.add(first_two)

        # Not this
        ex_mark = Exmark(font_size=72).set_color(RED)
        checkmark = Checkmark(font_size=72).set_color(GREEN)
        ex_mark.next_to(first_two, UP, MED_LARGE_BUFF, aligned_edge=LEFT)
        checkmark.next_to(first_two.saved_state, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        nope = Text("Nope!", font_size=60).set_fill(border_width=4)
        nope.match_color(ex_mark)
        nope.next_to(ex_mark, RIGHT)

        actually = Text("Actually...", font_size=60)
        actually.set_fill(border_width=2)
        actually.match_color(checkmark)
        actually.next_to(checkmark, RIGHT, SMALL_BUFF, aligned_edge=DOWN, index_of_submobject_to_align=0)

        self.play(Write(ex_mark), Write(nope))

        # Freely tune coefficients
        c_trackers = ValueTracker(0).replicate(2)

        def get_c_values():
            return [tracker.get_value() for tracker in c_trackers]

        number_lines = VGroup(
            NumberLine((-3, 3), width=2).rotate(90 * DEG).next_to(solution[c_tex], DOWN)
            for c_tex in const_texs[:2]
        )
        for line in number_lines:
            line.set_width(0.1, stretch=True)
            line.add_numbers(font_size=12, direction=LEFT, buff=0.1)

        tips = ArrowTip().rotate(PI).set_height(0.2).replicate(2)
        tips.set_color(BLUE)

        def update_tips(tips):
            for tip, line, value in zip(tips, number_lines, get_c_values()):
                tip.move_to(line.n2p(value), LEFT)
            return tips

        tips.add_updater(update_tips)

        c_labels = VGroup(DecimalNumber(0, font_size=24) for _ in range(2))

        def update_c_labels(c_labels):
            for label, tip, value in zip(c_labels, tips, get_c_values()):
                label.set_value(value)
                label.next_to(tip, RIGHT, SMALL_BUFF)

        c_labels.add_updater(update_c_labels)

        def random_tuning_animation(run_time=2, lag_ratio=0.25):
            return LaggedStart(
                *(
                    tracker.animate.set_value(random.uniform(-3, 3))
                    for tracker in c_trackers
                ),
                lag_ratio=lag_ratio,
                run_time=run_time,
            )

        self.play(
            FadeIn(number_lines),
            VFadeIn(tips),
            VFadeIn(c_labels),
            random_tuning_animation()
        )
        for _ in range(6):
            self.play(random_tuning_animation())
        self.wait()

        # Show four particulcar exponentials
        plane = ComplexPlane((-3, 3), (-2, 2))
        plane.set_height(3.25)
        plane.to_corner(UL)
        plane.add_coordinate_labels(font_size=16)
        plane.coordinate_labels[-1].set_opacity(0)

        s_values = [1.5j, -1.5j, -0.3 + 1.0j, -0.3 - 1.0j]
        s_dots = Group(
            GlowDot(plane.n2p(s))
            for s in s_values
        )
        s_labels = VGroup(
            Tex(Rf"s_{n}", font_size=24).set_color(YELLOW).next_to(dot, vect, buff=-0.1)
            for n, dot, vect in zip(it.count(1), s_dots, [RIGHT, RIGHT, LEFT, LEFT])
        )

        self.play(LaggedStart(
            FadeOut(number_lines, lag_ratio=0.1),
            FadeOut(tips, lag_ratio=0.1),
            FadeOut(c_labels, lag_ratio=0.1),
            FadeOut(VGroup(ex_mark, nope), LEFT),
            FadeIn(VGroup(checkmark, actually), LEFT),
            Restore(first_two),
            FadeIn(last_two, LEFT),
            run_time=2
        ))
        self.play(
            FadeIn(plane),
            LaggedStartMap(FadeIn, s_dots),
            LaggedStart(
                *(
                    FadeTransform(solution[f"s_{n + 1}"].copy(), s_labels[n])
                    for n in range(4)
                )
            ),
        )
        self.wait()

        # Comment on constants
        const_rects = VGroup(
            SurroundingRectangle(solution[c_tex], buff=0.075)
            for c_tex in const_texs
        )
        const_rects.set_stroke(BLUE, 2)

        underlines = VGroup(
            Line(c1.get_bottom(), c2.get_bottom(), path_arc=40 * DEG)
            for c1, c2 in it.combinations(const_rects, 2)
        )
        underlines.set_stroke(TEAL, 2)
        underlines.insert_n_curves(10)

        underlines = VGroup(
            Vector(0.75 * UP, thickness=4).next_to(rect, DOWN, buff=0)
            for rect in const_rects
        )
        underlines.set_fill(BLUE)

        constraint_words = TexText("Only specific $c_n$ work")
        constraint_words.set_fill(BLUE, border_width=1)
        constraint_words.match_width(underlines)
        constraint_words.next_to(underlines, DOWN, buff=SMALL_BUFF)

        self.play(
            FadeIn(constraint_words, lag_ratio=0.1),
            FadeOut(checkmark),
            FadeOut(actually),
            LaggedStartMap(ShowCreation, const_rects, lag_ratio=0.25),
            LaggedStartMap(GrowArrow, underlines),
        )
        self.play(FadeOut(const_rects, lag_ratio=0.1))

        # Add exponential parts
        if False:
            # For an insertion
            for term, s in zip(exp_texs, s_values):
                exp_diagram = self.get_exponential_diagram(solution[term], s)
                self.add(exp_diagram)
            self.wait(24)

        # Ask about each part
        term_rects = VGroup(
            SurroundingRectangle(solution[term], buff=0.1).set_stroke(TEAL, 2)
            for term in terms
        )
        s_rects = VGroup(
            SurroundingRectangle(solution[exp_tex][0][1:3], buff=0.05).set_stroke(YELLOW, 2)
            for exp_tex in exp_texs
        )

        moving_rects = const_rects.copy()
        self.remove(const_rects)

        anim_kw = dict(lag_ratio=0.25, run_time=1.5)
        self.play(
            FadeOut(constraint_words),
            FadeOut(underlines),
            Transform(moving_rects, term_rects, **anim_kw)
        )
        self.wait()
        self.play(Transform(moving_rects, s_rects, **anim_kw))
        self.wait()
        self.play(Transform(moving_rects, const_rects, **anim_kw))
        self.wait()
        self.play(FadeOut(moving_rects, **anim_kw))

    def get_exponential_diagram(self, term, s, c=1.0, color=PINK):
        plane = ComplexPlane((-1, 1), (-1, 1))
        plane.set_width(1.25)
        plane.next_to(term, UP)

        t_tracker = ValueTracker()
        get_t = t_tracker.get_value
        t_tracker.add_updater(lambda m, dt: m.increment_value(dt))

        vector = Vector(thickness=2, fill_color=color)
        vector.add_updater(lambda m: m.put_start_and_end_on(
            plane.n2p(0),
            plane.n2p(c * np.exp(s * get_t())),
        ))

        tail = TracingTail(vector.get_end, stroke_color=color, time_traced=2, stroke_width=(0, 4))
        path = TracedPath(vector.get_end, stroke_color=color, stroke_width=1, stroke_opacity=0.75)

        return Group(plane, t_tracker, vector, tail, path)


class BreakingDownFunctions(ForcedOscillatorSolutionForm):
    def construct(self):
        # A s plane on the left, output plane on the right
        s_plane, out_plane = planes = VGroup(
            ComplexPlane((-2, 2), (-2, 2)),
            ComplexPlane((-2, 2), (-2, 2)),
        )
        for plane in planes:
            plane.set_height(5)
            plane.add_coordinate_labels(font_size=16)

        out_plane.center().to_edge(DOWN)
        s_plane.move_to(out_plane).to_edge(LEFT)

        self.add(out_plane)

        # Write a function as a sum, above the output plane
        n_range = list(range(1, 6))
        exp_texs = [Rf"e^{{s_{n} t}}" for n in n_range]
        const_texs = [Rf"c_{n}" for n in n_range]
        terms = [" ".join(pair) for pair in zip(const_texs, exp_texs)]
        solution = Tex("x(t) = " + " + ".join(terms), isolate=[*exp_texs, *const_texs])

        solution[re.compile(r's_\w+')].set_color(YELLOW)
        solution[re.compile(r'c_\w+')].set_color(BLUE)

        solution.next_to(out_plane, UP)

        self.add(solution)

        # Exp animations
        s_values = [-0.2 + 2j, -0.2 - 2j, -0.1 + 1j, -0.1 - 1j, -0.2]
        c_values = [1j, -1j, 0.8, 0.8, -0.75]
        colors = color_gradient([PINK, MAROON_B], len(n_range), interp_by_hsl=False)
        exp_diagrams = Group()
        for term, s, c, color in zip(terms, s_values, c_values, colors):
            part = solution[term]
            if len(part) == 0:
                continue
            exp_diagram = self.get_exponential_diagram(part, s, c, color)
            self.add(*exp_diagram)
            exp_diagrams.add(exp_diagram)

        # Set up the output
        center_point = VectorizedPoint(out_plane.n2p(0))
        all_vects = Vector().replicate(len(n_range))
        scale_factor = out_plane.x_axis.get_unit_size() / exp_diagrams[0][0].x_axis.get_unit_size()

        for diagram, vect, previous in zip(exp_diagrams, all_vects, [center_point, *all_vects]):
            vect.clone = diagram[2]
            vect.previous = previous
            vect.add_updater(lambda m: m.become(m.clone).scale(scale_factor))
            vect.add_updater(lambda m: m.shift(m.previous.get_end() - m.get_start()))

        self.add(all_vects)

        # Add output graph
        graph = VMobject()
        graph.set_stroke(RED, 3)
        graph.start_new_path(all_vects[-1].get_end())

        def update_graph(graph, dt):
            graph.shift(0.25 * dt * DOWN)
            graph.add_line_to(all_vects[-1].get_end())

        graph.add_updater(update_graph)

        self.add(graph)

        self.wait(30)
        self.play(VFadeOut(graph), VFadeOut(all_vects))
        exp_diagrams.suspend_updating()

        # Collapse to the s plane
        out_plane.generate_target()
        plane_group = VGroup(s_plane, out_plane.target)
        plane_group.arrange(RIGHT, buff=2)
        plane_group.to_edge(DOWN)
        compact_equation = Tex(
            R"x(t) = \sum_{n=1}^{N} c_n e^{{s_n} t}",
            t2c={"c_n": BLUE, "s_n": YELLOW},
            isolate=["n=1", "N"]
        )
        compact_equation.next_to(out_plane.target, UP)
        compact_equation_start = compact_equation[:-4]

        s_dot = GlowDot()
        s_dot.move_to(s_plane.n2p(s_values[2]))
        s_label = Tex(R"s").set_color(YELLOW)
        s_label.always.next_to(s_dot, UL, buff=-0.1)
        s_plane_title = Text(R"S-plane", font_size=60)
        s_plane_title.next_to(s_plane, UP)
        s_plane_title.set_color(YELLOW)

        exp_graph = VMobject()
        exp_graph.set_stroke(PINK, 2)

        def update_exp_graph(exp_graph):
            s = s_plane.p2n(s_dot.get_center())
            anchors = np.array([
                out_plane.n2p(np.exp(s * t))
                for t in np.arange(0, 100, 0.1)
            ])
            exp_graph.set_points_as_corners(anchors)

        exp_graph.add_updater(update_exp_graph)

        self.play(LaggedStart(
            MoveToTarget(out_plane),
            LaggedStart(*(
                exp_diagram.animate.scale(scale_factor).move_to(out_plane.target)
                for exp_diagram in exp_diagrams
            ), lag_ratio=0.01),
            AnimationGroup(*(
                ReplacementTransform(solution[t1], compact_equation[t2])
                for t1, t2 in [
                    ("x(t) = ", "x(t) = "),
                    (re.compile(r'c_\w+'), "c_n"),
                    (re.compile(r's_\w+'), "s_n"),
                    ("e", "e"),
                    ("t", "t"),
                    ("+", R"\sum_{n=1}^{N}"),
                ]
            )),
            lag_ratio=0.2,
            run_time=2
        ))
        exp_graph.update()
        self.play(
            FadeIn(s_plane),
            TransformFromCopy(compact_equation["s_n"][0], s_label),
            FadeTransform(compact_equation["s_n"][0].copy(), s_dot),
            Write(s_plane_title),
            FadeOut(exp_diagrams[2]),
            FadeIn(exp_graph, suspend_mobject_updating=True),
            compact_equation_start.animate.set_opacity(0.4)
        )
        self.remove(exp_diagrams)
        self.wait()

        # Growth, decay and oscillation
        arrows = VGroup(
            Arrow(s_plane.n2p(0), s_plane.n2p(z), thickness=4, fill_color=GREY_A)
            for z in [2, -2, 2j, -2j]
        )
        arrows.set_fill(GREY_A, 1)
        arrow_labels = VGroup(
            Text("Growth", font_size=36).next_to(arrows[0], UP, buff=0),
            Text("Decay", font_size=36).next_to(arrows[1], UP, buff=0),
            Text("Oscillation", font_size=36).rotate(-90 * DEG).next_to(arrows[3], RIGHT, buff=SMALL_BUFF),
        )
        rot_vect = Vector(2 * RIGHT, fill_color=RED, thickness=5)
        rot_vect.shift(out_plane.n2p(0) - rot_vect.get_start())
        rot_vect.rotate(-45 * DEG, about_point=out_plane.n2p(0))
        rot_vect.add_updater(lambda m, dt: m.rotate(2 * dt, about_point=out_plane.n2p(0)))

        self.play(
            s_dot.animate.shift(0.2 * RIGHT).set_anim_args(run_time=1),
            GrowArrow(arrows[0]),
            FadeIn(arrow_labels[0]),
        )
        self.play(
            s_dot.animate.shift(0.2 * LEFT).set_anim_args(run_time=1),
            GrowArrow(arrows[1]),
            FadeIn(arrow_labels[1]),
        )
        self.play(
            # s_dot.animate.shift(3 * DOWN).set_anim_args(run_time=4, rate_func=there_and_back),
            GrowArrow(arrows[2]),
            GrowArrow(arrows[3]),
            FadeIn(arrow_labels[2]),
            VFadeIn(rot_vect)
        )
        self.wait()
        self.play(VFadeOut(rot_vect))

        # Show multiple s
        frame = self.frame
        s_values[:2] = [-1.5 + 0.5j, -1.5 - 0.5j]
        s_values.extend([-0.8 + 1.5j, -0.8 - 1.5j])
        s_dots = Group(GlowDot(s_plane.n2p(s)) for s in s_values)

        self.play(
            FadeOut(arrows),
            FadeOut(arrow_labels),
            FadeOut(out_plane),
            FadeOut(exp_graph),
            FadeIn(s_dots, lag_ratio=0.5),
            FadeOut(s_dot),
            FadeOut(s_label),
            compact_equation.animate.set_height(2.0).set_opacity(1).next_to(s_plane, RIGHT, LARGE_BUFF),
            frame.animate.match_y(s_plane),
        )
        self.wait()

        # Infinite
        inf = Tex(R"\infty", font_size=60)
        N = compact_equation["N"][0]
        inf.move_to(N)

        dot_line = Group(
            GlowDot(s_plane.n2p(complex(-0.5, b)))
            for b in np.linspace(-2, 2, 25)
        )

        self.play(
            FlashAround(N, time_width=1),
            # Transform(N, inf, path_arc=20 * DEG),
            FadeTransform(N, inf, path_arc=20 * DEG),
            ShowIncreasingSubsets(dot_line, run_time=5, rate_func=linear),
            ReplacementTransform(s_dots, dot_line[:len(s_dots)].copy().set_opacity(0))
        )

        # Continuous range
        integral_eq = Tex(
            R"x(t) = \int_{\gamma} c(s) e^{st} ds",
            t2c={"s": YELLOW, R"\gamma": YELLOW}
        )
        integral_eq.replace(compact_equation, dim_to_match=1)
        integral_eq.shift(0.5 * RIGHT)
        line = Line(dot_line.get_bottom(), dot_line.get_top())
        line.set_stroke(YELLOW, 2)
        thick_line = line.copy().set_stroke(width=6)
        thick_line.insert_n_curves(100)

        self.play(
            LaggedStart(*(
                FadeTransform(compact_equation[t1], integral_eq[t2])
                for t1, t2 in [
                    ("x(t) = ", "x(t) ="),
                    (R"\sum_{n=1}^{N}", R"\int_{\gamma}"),
                    (R"n=1", R"\gamma"),
                    ("c_n", "c(s)"),
                    (R"e^{{s_n} t}", R"e^{st}"),
                ]
            )),
            FadeIn(integral_eq[R"ds"]),
            LaggedStartMap(FadeOut, dot_line, lag_ratio=0.5, scale=0.25, time_span=(0.3, 2)),
            VShowPassingFlash(thick_line, run_time=2),
            ShowCreation(line, run_time=2),
        )
        self.wait()
