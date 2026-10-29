# ==============================================================================
# Scene:      GeneralLinearEquation
# Source:     videos/_2025/laplace/supplements.py (lines 1170-1458)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralLinearEquation.py GeneralLinearEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralLinearEquation(InteractiveScene):
    def construct(self):
        # Set up equations
        a_texs = ["a_n", "a_2", "a_1", "a_0"]
        x_texs = ["x^{n}(t)", "x''(t)", "x'(t)", "x(t)"]
        x_colors = color_gradient([BLUE, TEAL], len(x_texs), interp_by_hsl=True)
        t2c = {"{s}": YELLOW}
        t2c.update({a: WHITE for a in a_texs})
        t2c.update({x: color for x, color in zip(x_texs, x_colors)})
        ode = Tex(R"a_n x^{n}(t) + \cdots + a_2 x''(t) + a_1 x'(t) + a_0 x(t) = 0", t2c=t2c)
        exp_version = Tex(
            R"a_n \left({s}^n e^{{s}t}\right) "
            R"+ \cdots "
            R"+ a_2 \left({s}^2 e^{{s}t}\right) "
            R"+ a_1 \left({s}e^{{s}t}\right) "
            R"+ a_0 e^{{s}t} = 0",
            t2c=t2c
        )
        factored = Tex(R"e^{{s}t} \left(a_n {s}^n + \cdots + a_2 {s}^2 + a_1 {s} + a_0 \right) = 0", t2c=t2c)

        ode.to_edge(UP)
        exp_version.next_to(ode, DOWN, MED_LARGE_BUFF)
        factored.move_to(exp_version)

        # Introduce ode
        index = ode.submobjects.index(ode["a_2"][0][0])

        right_part = ode[index:]
        left_part = ode[:index]
        right_part.save_state()
        right_part.set_x(0)

        self.play(FadeIn(right_part, UP))
        self.wait()
        self.play(LaggedStart(
            Restore(right_part),
            Write(left_part)
        ))
        self.add(ode)

        # Highlight equation parts
        x_arrows = VGroup(
            Arrow(UP, ode[x_tex].get_bottom(), fill_color=color)
            for x_tex, color in zip(x_texs, x_colors)
        )
        x_arrows.reverse_submobjects()

        x_rects = VGroup(SurroundingRectangle(ode[x_tex], buff=SMALL_BUFF) for x_tex in x_texs)
        a_rects = VGroup(SurroundingRectangle(ode[a_tex]) for a_tex in a_texs)
        full_rect = SurroundingRectangle(ode[:-2])
        zero_rect = SurroundingRectangle(ode[-2:])
        VGroup(x_rects, a_rects, full_rect, zero_rect).set_stroke(YELLOW, 2)

        self.play(LaggedStartMap(ShowCreation, x_rects))
        self.wait()
        self.play(ReplacementTransform(x_rects, a_rects, lag_ratio=0.2))
        self.wait()
        self.play(ReplacementTransform(a_rects, VGroup(full_rect)))
        self.wait()
        self.play(ReplacementTransform(full_rect, zero_rect))
        self.wait()
        self.play(FadeOut(zero_rect))

        # Plug in e^{st}
        key_map = {
            R"+ a_0 x(t) = 0": R"+ a_0 e^{{s}t} = 0",
            R"+ a_1 x'(t)": R"+ a_1 \left({s}e^{{s}t}\right)",
            R"+ a_2 x''(t)": R"+ a_2 \left({s}^2 e^{{s}t}\right)",
            R"+ \cdots": R"+ \cdots",
            R"a_n x^{n}(t)": R"a_n \left({s}^n e^{{s}t}\right)",
        }

        self.play(LaggedStart(*(
            FadeTransform(ode[k1].copy(), exp_version[k2])
            for k1, k2 in key_map.items()
        ), lag_ratio=0.6, run_time=4))
        self.wait()
        self.play(
            TransformMatchingTex(
                exp_version,
                factored,
                matched_keys=[R"e^{{s}t}", "{s}^n", "{s}^2", "{s}", "a_n", "a_2", "a_1", "a_0"],
                path_arc=45 * DEG
            )
        )
        self.wait()

        # Highlight the polynomail
        poly_rect = SurroundingRectangle(factored[R"a_n {s}^n + \cdots + a_2 {s}^2 + a_1 {s} + a_0"])
        poly_rect.set_stroke(YELLOW, 1)

        self.play(
            ShowCreation(poly_rect),
            FadeOut(factored["e^{{s}t}"]),
            FadeOut(factored[R"\left("]),
            FadeOut(factored[R"\right)"]),
        )

        # Show factored expression
        linear_term_texs = [
            R"({s} - s_1)",
            R"({s} - s_2)",
            R"({s} - s_3)",
            R"\cdots",
            R"({s} - s_n)",
        ]
        fully_factored = Tex(
            R"a_n" + " ".join(linear_term_texs),
            t2c=t2c,
            font_size=42,
            isolate=linear_term_texs
        )
        fully_factored.next_to(poly_rect, DOWN)
        linear_terms = VGroup(
            fully_factored[tex][0]
            for tex in linear_term_texs
        )

        self.play(
            Transform(factored["{s}"][1].copy().replicate(4), fully_factored["{s}"].copy(), remover=True),
            FadeIn(fully_factored, time_span=(0.25, 1)),
        )
        self.wait()

        # Plane
        plane = ComplexPlane((-3, 3), (-3, 3), width=6, height=6)
        plane.set_height(4.5)
        plane.next_to(poly_rect, DOWN, LARGE_BUFF)
        plane.set_x(0)
        plane.add_coordinate_labels(font_size=16)
        c_label = Tex(R"\mathds{C}", font_size=90, fill_color=BLUE)
        c_label.next_to(plane, LEFT, aligned_edge=UP).shift(0.5 * DOWN)

        self.play(
            Write(plane, run_time=1, lag_ratio=2e-2),
            Write(c_label),
        )

        # Show some random root collections
        for n in range(4):
            roots = []
            n_roots = random.randint(3, 7)
            for _ in range(n_roots):
                root = complex(random.uniform(-3, 3), random.uniform(-3, 3))
                if random.random() < 0.25:
                    roots.append(root.real)
                else:
                    roots.extend([root, root.conjugate()])
            dots = Group(GlowDot(plane.n2p(z)) for z in roots)

            self.play(ShowIncreasingSubsets(dots))
            self.play(FadeOut(dots))

        # Turn linear terms into
        roots = [0.2 + 1j, 0.2 - 1j, -0.5 + 3j, -0.5 - 3j, -2]
        root_dots = Group(GlowDot(plane.n2p(root)) for root in roots)

        root_labels = VGroup(
            Tex(Rf"s_{{{n + 1}}}", font_size=36).next_to(dot.get_center(), UR, SMALL_BUFF)
            for n, dot in enumerate(root_dots)
        )
        root_labels.set_color(YELLOW)

        root_intro_kw = dict(lag_ratio=0.3, run_time=4)
        self.play(
            LaggedStart(*(
                FadeTransform(term, dot)
                for term, dot in zip(linear_terms, root_dots)
            ), **root_intro_kw),
            LaggedStart(*(
                TransformFromCopy(term[3:5], label)
                for term, label in zip(linear_terms, root_labels)
            ), **root_intro_kw),
            FadeOut(fully_factored["a_n"][0]),
        )
        self.wait()

        # Show the solutions
        frame = self.frame
        axes = VGroup(
            Axes((0, 10), (-y_max, y_max), width=5, height=1.25)
            for root in roots
            for y_max in [3 if root.real > 0 else 1]
        )
        axes.arrange(DOWN, buff=0.75)
        axes.next_to(plane, RIGHT, buff=6)

        c_trackers = Group(ComplexValueTracker(1) for root in roots)
        graphs = VGroup(
            self.get_graph(axes, root, c_tracker.get_value)
            for axes, root, c_tracker in zip(axes, roots, c_trackers)
        )

        axes_labels = VGroup(
            Tex(Rf"e^{{s_{{{n + 1}}} t}}", font_size=60)
            for n in range(len(axes))
        )
        for label, ax in zip(axes_labels, axes):
            label.next_to(ax, LEFT, aligned_edge=UP)
            label[1:3].set_color(YELLOW)

        self.play(
            FadeIn(axes, lag_ratio=0.2),
            frame.animate.reorient(0, 0, 0, (4.67, -0.94, 0.0), 10.96),
            LaggedStart(
                (FadeTransform(m1.copy(), m2) for m1, m2 in zip(root_labels, axes_labels)),
                lag_ratio=0.05,
                group_type=Group
            ),
            run_time=2
        )

        rect = Square(side_length=1e-3).move_to(plane.n2p(0))
        rect.set_stroke(TEAL, 3)
        for root_label, graph in zip(root_labels, graphs):
            self.play(
                ShowCreation(graph, time_span=(0.5, 2.0), suspend_mobject_updating=True),
                rect.animate.surround(root_label, buff=0.1),
            )
        self.play(FadeOut(rect))
        self.wait()

        # Add on constants
        constant_labels = VGroup(
            Tex(Rf"c_{{{n + 1}}}", font_size=60).next_to(label[0], LEFT, SMALL_BUFF, aligned_edge=UP)
            for n, label in enumerate(axes_labels)
        )
        constant_labels.set_color(BLUE_B)
        target_values = [0.5, 0.25, 1.5, -1.5, -1]

        solution_rect = SurroundingRectangle(VGroup(axes_labels, axes, constant_labels), buff=MED_SMALL_BUFF)
        solution_rect.set_stroke(WHITE, 1)
        solution_words = Text("All Solutions", font_size=60)
        solution_words.next_to(solution_rect, UP)
        solution_word = solution_words["Solutions"][0]
        solution_word.save_state(0)
        solution_word.match_x(solution_rect)

        const_rects = VGroup(SurroundingRectangle(c_label) for c_label in constant_labels)
        const_rects.set_stroke(BLUE, 3)

        plusses = Tex("+").replicate(4)
        for l1, l2, plus in zip(axes_labels, axes_labels[1:], plusses):
            plus.move_to(VGroup(l1, l2)).shift(SMALL_BUFF * LEFT)

        self.play(
            ShowCreation(solution_rect),
            Write(solution_word),
        )
        self.play(
            LaggedStartMap(Write, constant_labels, lag_ratio=0.5),
            LaggedStart(*(
                c_tracker.animate.set_value(value)
                for c_tracker, value in zip(c_trackers, target_values)
            ), lag_ratio=0.5),
            run_time=4
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, plusses),
            Write(solution_words["All"]),
            Restore(solution_word),
        )
        self.wait()

        # Play with constants
        self.play(LaggedStartMap(ShowCreation, const_rects, lag_ratio=0.15))
        value_sets = [
            [1, 1, 1, 1, 1],
            [1j, -1j, 1 + 1j, -1 + 1j, -0.5],
            [-0.5, 1j, 1j, 1 + 1j, -1],
        ]
        for values in value_sets:
            self.play(
                LaggedStart(*(
                    c_tracker.animate.set_value(value)
                    for c_tracker, value in zip(c_trackers, values)
                ), lag_ratio=0.25, run_time=3)
            )
            self.wait()
        self.play(LaggedStartMap(FadeOut, const_rects, lag_ratio=0.25))
        self.wait()

    def get_graph(self, axes, s, get_const):
        def func(t):
            return (get_const() * np.exp(s * t)).real

        graph = axes.get_graph(func, bind=True, stroke_color=TEAL, stroke_width=2)
        return graph
