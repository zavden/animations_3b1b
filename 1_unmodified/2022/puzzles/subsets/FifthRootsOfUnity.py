# ==============================================================================
# Scene:      FifthRootsOfUnity
# Source:     videos/_2022/puzzles/subsets.py (lines 2548-3251)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FifthRootsOfUnity.py FifthRootsOfUnity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_set_tex(values, max_shown=7, **kwargs):
    if len(values) > max_shown:
        value_mobs = [
            *map(Integer, values[:max_shown - 2]),
            Tex("\\dots"),
            Integer(values[-1], group_with_commas=False),
        ]
    else:
        value_mobs = list(map(Integer, values))

    commas = Tex(",").replicate(len(value_mobs) - 1)
    result = VGroup()
    result.add(Tex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if len(value_mobs) > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(Tex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if len(values) > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if len(values) > max_shown:
        result[-4].match_y(commas)
    result.values = values
    return result


def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))


class FifthRootsOfUnity(InteractiveScene):
    def construct(self):
        # Setup plane
        plane = ComplexPlane((-2, 2), (-2, 2))
        plane.set_height(FRAME_HEIGHT - 0.5)
        plane.add_coordinate_labels(font_size=24)
        for coord in plane.coordinate_labels:
            coord.shift_onto_screen(buff=SMALL_BUFF)
            coord.set_fill(WHITE)
        plane.to_edge(LEFT, buff=0.1)
        self.disable_interaction(plane)

        unit_circle = Circle(radius=plane.x_axis.get_unit_size())
        unit_circle.move_to(plane.get_origin())
        unit_circle.set_stroke(GREY_C, 2)
        self.disable_interaction(unit_circle)

        complex_plane_title = Text("Complex plane", font_size=42)
        complex_plane_title.next_to(plane.get_corner(UL), DR, buff=SMALL_BUFF)
        complex_plane_title.set_backstroke(width=8)

        self.add(plane)
        self.add(unit_circle)
        self.add(complex_plane_title)

        # Setup roots
        roots = [np.exp(complex(0, n * TAU / 5)) for n in range(5)]
        root_points = list(map(plane.n2p, roots))
        root_dots = Group(*(
            GlowDot(point)
            for point in root_points
        ))
        root_lines = VGroup(*(
            Arrow(
                plane.get_origin(), point, buff=0,
                stroke_width=2,
                stroke_color=YELLOW,
                stroke_opacity=0.7
            )
            for point in root_points
        ))
        self.disable_interaction(root_dots)

        pentagon = Polygon(*root_points)
        pentagon.set_stroke(TEAL, 2)
        pentagon.set_fill(TEAL, 0.25)
        self.add(pentagon)

        # Add function label
        function = Tex(
            "f(x) = \\sum_{n = 0}^N c_n x^n",
            tex_to_color_map={"x": BLUE}
        )
        function.move_to(midpoint(plane.get_right(), RIGHT_SIDE))
        function.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(function)

        # Roots of unity
        arc = Arc(0, TAU / 5, radius=0.2, arc_center=plane.get_origin())
        arc.set_stroke(WHITE, 2)
        arc_label = Tex("2\\pi / 5", font_size=24)
        arc_label.next_to(arc.pfp(0.5), UR, buff=SMALL_BUFF)
        arc_label.set_color(GREY_A)

        root_kw = dict(
            tex_to_color_map={"\\zeta": YELLOW},
            isolate=["\\cos(72^\\circ)", "\\sin(72^\\circ)"],
            font_size=36,
        )
        zeta_labels = VGroup(
            Tex("\\zeta^0 = 1", **root_kw),
            Tex("\\zeta", **root_kw),
            Tex("\\zeta^2", **root_kw),
            Tex("\\zeta^3", **root_kw),
            Tex("\\zeta^4", **root_kw),
        )
        zeta_labels.set_backstroke(width=4)
        for point, label in zip(root_points, zeta_labels):
            vect = normalize(point - plane.get_origin())
            if point is root_points[0]:
                vect = UR
            label.next_to(point, vect, buff=SMALL_BUFF)
        exp_rhs = Tex(" = e^{2\\pi i / 5}", **root_kw)
        trig_rhs = Tex("= \\cos(72^\\circ) + i\\cdot \\sin(72^\\circ)", **root_kw)
        last = zeta_labels[1]
        for rhs in exp_rhs, trig_rhs:
            rhs.set_backstroke(width=4)
            rhs.next_to(last, RIGHT, SMALL_BUFF)
            last = rhs
        exp_rhs.shift((trig_rhs[0].get_y() - exp_rhs[0].get_y()) * UP)

        self.play(
            FadeInFromPoint(
                root_dots[1], plane.n2p(1),
                path_arc=TAU / 5,
            ),
            pentagon.animate.set_fill(opacity=0.1)
        )
        self.play(Write(zeta_labels[1]))
        self.wait()
        self.play(
            ShowCreation(arc), Write(arc_label),
            TransformFromCopy(root_lines[0], root_lines[1], path_arc=-TAU / 5)
        )
        self.wait()
        self.play(Write(exp_rhs))
        self.wait()

        # Show trig
        x_line = Line(plane.n2p(0), plane.n2p(math.cos(TAU / 5)))
        y_line = Line(plane.n2p(math.cos(TAU / 5)), plane.n2p(np.exp(complex(0, TAU / 5))))
        x_line.set_stroke(RED, 2)
        y_line.set_stroke(PINK, 2)
        low_cos = Tex("\\cos(72^\\circ)", font_size=24)
        low_sin = Tex("\\sin(72^\\circ)", font_size=24)
        low_cos.next_to(x_line, DOWN, SMALL_BUFF, aligned_edge=LEFT)
        low_cos.shift(SMALL_BUFF * RIGHT)
        low_sin.next_to(y_line, RIGHT, SMALL_BUFF)
        VGroup(low_cos, low_sin).set_backstroke(BLACK)

        self.play(Write(trig_rhs))
        self.wait()
        self.play(
            TransformFromCopy(trig_rhs.select_part("\\cos(72^\\circ)"), low_cos),
            ShowCreation(x_line),
            FadeOut(arc_label)
        )
        self.wait()
        self.play(
            TransformFromCopy(trig_rhs.select_part("\\sin(72^\\circ)"), low_sin),
            ShowCreation(y_line),
        )
        self.wait()

        self.play(LaggedStartMap(FadeOut, VGroup(
            trig_rhs, x_line, low_cos, y_line, low_sin
        )))

        # Show all roots of unity
        for i in range(2, 6):
            self.play(*(
                TransformFromCopy(group[i - 1], group[i % 5], path_arc=-TAU / 5)
                for group in [root_lines, root_dots, zeta_labels]
            ))
            self.wait()

        # Name the roots of unity
        title = OldTexText("``Fifth roots of unity''")
        title.set_color(YELLOW)
        title.match_y(plane)
        title.match_x(function)
        equation = OldTex("z^5 = 1")
        equation.set_color(WHITE)
        equation.next_to(title, DOWN)

        self.play(
            Write(title),
            LaggedStart(*(
                FlashAround(zl, time_width=1.5)
                for zl in zeta_labels
            ), lag_ratio=0.1, run_time=3)
        )
        self.wait()
        self.play(FadeIn(equation, 0.5 * DOWN))
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(title, equation), shift=DOWN),
            FadeOut(VGroup(arc, arc_label)),
        )

        # Key expression
        expr = Tex("+".join([f"f(\\zeta^{{{n}}})" for n in range(5)]), **root_kw)
        expr.next_to(function, DOWN, LARGE_BUFF)

        self.play(
            TransformMatchingShapes(function[:4].copy(), expr, run_time=1.5),
            FadeOut(pentagon),
        )
        self.wait()

        # Examples, f(x) = x, f(x) = x^2, etc.
        ex_kw = dict(tex_to_color_map={"{x}": BLUE}, font_size=36)
        example_texts = [
            Tex(
                "\\text{Example: } f({x}) = {x}" + ("^" + str(n) if n > 1 else ""),
                **ex_kw
            )
            for n in range(1, 6)
        ]
        example_sums = [
            Tex(
                "+".join([f"\\zeta^{{{k * n}}}" for n in range(5)]) + ("=5" if k == 5 else "=0"),
                **root_kw
            )
            for k in range(1, 6)
        ]

        def update_root_lines(rl):
            for line, dot in zip(rl, root_dots):
                line.put_start_and_end_on(plane.get_center(), dot.get_center())
            return rl

        root_lines.add_updater(update_root_lines)

        for k, ex_text, ex_sum in zip(it.count(1), example_texts, example_sums):
            ex_text.next_to(expr, DOWN, LARGE_BUFF)
            ex_sum.next_to(ex_text, DOWN, LARGE_BUFF)

            if k == 1:
                self.play(Write(ex_text))
                self.wait()
                self.play(FadeTransform(expr.copy(), ex_sum))
                root_lines.save_state()
                self.wait(note="Move root vectors tip to tail (next animation they restore)")
                self.play(root_lines.animate.restore())
                self.wait()
            else:
                self.play(
                    FadeOut(example_texts[k - 2], 0.5 * UP),
                    FadeIn(ex_text, 0.5 * UP),
                    FadeOut(example_sums[k - 2])
                )
                self.wait()
                self.play(FadeTransform(expr.copy(), ex_sum))
                self.wait()
                # Show permutation
                arrows = VGroup(*(
                    Arrow(root_dots[n], root_dots[(k * n) % 5], buff=0, stroke_width=3)
                    for n in range(1, 5)
                ))
                arrows.set_opacity(0.8)
                for arrow in arrows:
                    self.play(ShowCreation(arrow))
                    self.wait()
                self.play(FadeOut(arrows))
                # Animate kth power
                self.animate_kth_power(
                    plane,
                    root_dots, k,
                )
                self.wait()

        # Emphasize the upshot
        example = VGroup(example_texts[-1], example_sums[-1])
        example.generate_target()
        example.target.arrange(DOWN)
        example.target.match_x(expr)
        example.target.to_edge(DOWN)
        brace = Brace(expr, DOWN, color=GREY_B)

        func_kw = dict(tex_to_color_map={"x": BLUE})
        relations = VGroup(
            Tex("x^n \\rightarrow 0 \\qquad \\text{ if } 5 \\nmid n", **func_kw),
            Tex("x^n \\rightarrow 5 \\qquad \\text{ if } 5 \\mid n", **func_kw),
        )
        relations.arrange(DOWN)
        relations.next_to(brace, DOWN)

        self.play(
            GrowFromCenter(brace),
            MoveToTarget(example)
        )
        for relation in relations:
            self.play(Write(relation))
            self.wait()

        # Write answer expression
        relation_group = VGroup(expr, brace, relations)

        answer = Tex(
            "c_0 + c_5 + c_{10} + \\cdots"
            "=\\frac{1}{5}\\sum_{k = 0}^4 f(\\zeta^k)",
            tex_to_color_map={"\\zeta": YELLOW}
        )
        answer.set_width(5)
        answer.next_to(function, DOWN, LARGE_BUFF)
        answer_rect = SurroundingRectangle(answer, buff=0.2)
        answer_rect.round_corners()
        answer_rect.set_stroke(YELLOW, 2)
        self.disable_interaction(answer_rect)

        self.play(
            FadeOut(example, DOWN),
            relation_group.animate.set_width(4.5).to_edge(DOWN),
            Write(answer)
        )
        self.play(
            VShowPassingFlash(answer_rect.copy()),
            FadeIn(answer_rect)
        )
        self.add(answer_rect, answer)
        self.wait()

        # Bring back original definition
        factored = Tex(
            "f(x) = (1 + x)(1 + x^2)(1 + x^3)(1 + x^4)(1 + x^5)\\cdots\\left(1 + x^{2{,}000}\\right)",
            **func_kw
        )
        factored.to_edge(UP)

        lower_group = VGroup(
            VGroup(answer_rect, answer),
            relation_group,
        )
        lower_group.generate_target()
        lower_group.target.arrange(RIGHT, buff=MED_LARGE_BUFF)
        lower_group.target.set_width(8.5)
        lower_group.target.to_corner(DR)

        plane_group = Group(
            plane, unit_circle,
            root_lines, root_dots, zeta_labels, exp_rhs,
            complex_plane_title
        )
        plane_group.generate_target()
        plane_group.target.set_height(4.5, about_edge=DL)

        self.play(
            Write(factored),
            function.animate.next_to(factored, DOWN, buff=0.4, aligned_edge=LEFT),
            MoveToTarget(lower_group),
            MoveToTarget(plane_group),
        )
        self.wait()

        # Evaluate f at zeta
        eq_kw = dict(
            tex_to_color_map={"\\zeta": YELLOW, "{z}": GREY_A},
        )
        f_zeta = Tex(
            "f(\\zeta) = \\Big("
            "(1+\\zeta)(1+\\zeta^{2})(1+\\zeta^{3})(1+\\zeta^{4})(1+\\zeta^{5})"
            "\\Big)^{400}",
            **eq_kw
        )
        f_zeta.next_to(factored, DOWN, aligned_edge=LEFT)

        expr_copy = expr.copy()
        expr_copy.generate_target()
        expr_copy.target.scale(2).next_to(plane, RIGHT, LARGE_BUFF, UP)
        fz1 = expr_copy.target[6:11]
        fz1_rect = SurroundingRectangle(fz1, buff=SMALL_BUFF).round_corners()
        fz1_rect.set_stroke(TEAL, 2)

        want_label = Text("What we want")
        want_label.next_to(expr_copy.target, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStart(MoveToTarget(expr_copy), Write(want_label)))
        self.wait()
        self.play(ShowCreation(fz1_rect))
        self.play(
            TransformFromCopy(fz1, f_zeta[:5]),
            FadeOut(function, DOWN)
        )
        self.wait()
        self.play(*map(FadeOut, [expr_copy, fz1_rect, want_label]))
        for i, n in zip([5, 10, 16, 22, 28], it.chain([5], it.cycle([6]))):
            self.play(TransformFromCopy(factored[i:i + n], f_zeta[i + 1:i + n + 1]))
        self.wait()
        self.play(Write(f_zeta[5]), Write(f_zeta[35:]))
        self.wait(note="Shift zeta values on next move")

        # Visualize roots moving
        shift_vect = plane.n2p(1) - plane.n2p(0)
        zp1_labels = VGroup(*(
            Tex(f"\\zeta^{{{n}}} + 1", **root_kw)
            for n in range(5)
        ))
        zp1_labels.match_height(zeta_labels[0])
        for zp1_label, z_label in zip(zp1_labels, zeta_labels):
            zp1_label.set_backstroke(width=5)
            zp1_label.move_to(z_label, DL)
            zp1_label.shift(shift_vect)
        zp1_labels[0].next_to(root_dots[0].get_center() + shift_vect, UL, SMALL_BUFF)

        new_circle = unit_circle.copy()
        new_circle.set_stroke(GREY_B, opacity=0.5)
        self.disable_interaction(new_circle)
        self.replace(unit_circle, unit_circle, new_circle)

        self.remove(zeta_labels)
        self.play(
            root_dots.animate.shift(shift_vect),
            new_circle.animate.shift(shift_vect),
            TransformFromCopy(zeta_labels, zp1_labels),
            FadeOut(exp_rhs),
            run_time=2,
        )
        self.wait()

        # Estimate answer
        faders = VGroup(lower_group, f_zeta[:6], f_zeta[-4:], factored)
        faders.save_state()

        estimate = Tex(
            "= 2 \\cdot L_1^2 \\cdot L_2^2",
            isolate=["= 2", "\\cdot L_1^2", "\\cdot L_2^2"],
            **eq_kw
        )
        roughly_two = Tex("\\approx 2")
        estimate.next_to(plane, RIGHT, buff=1.5, aligned_edge=UP)
        roughly_two.next_to(estimate, DOWN, MED_LARGE_BUFF, LEFT)

        L1_label = Tex("L_1", font_size=24)
        L2_label = Tex("L_2", font_size=24)
        L1_label.next_to(root_lines[1].pfp(0.75), DR, buff=0.05)
        L2_label.next_to(root_lines[2].get_center(), LEFT, SMALL_BUFF)
        VGroup(L1_label, L2_label).set_backstroke()

        root_groups = Group(*(
            Group(*parts)
            for parts in zip(root_dots, root_lines, zp1_labels)
        ))

        self.wait()
        self.play(faders.animate.fade(0.75))
        self.remove(faders)
        self.add(*faders)
        self.wait()
        self.play(
            root_groups[1:].animate.set_opacity(0.1),
        )
        self.wait()
        self.play(Write(estimate.select_part("= 2")))
        self.wait()
        self.play(
            root_groups[0].animate.set_opacity(0.1),
            root_groups[1:5:3].animate.set_opacity(1),
        )
        self.wait()
        self.play(Write(L1_label))
        self.wait()
        self.play(FadeTransform(L1_label.copy(), estimate.select_part("\\cdot L_1^2")))
        self.wait()
        self.play(
            root_groups[1:5:3].animate.set_opacity(0.1),
            root_groups[2:4].animate.set_opacity(1),
        )
        self.wait()
        self.play(Write(L2_label))
        self.wait()
        self.play(FadeTransform(L2_label.copy(), estimate.select_part("\\cdot L_2^2")))
        self.wait()
        self.play(root_groups.animate.set_opacity(1))
        self.wait()
        self.play(Write(roughly_two))
        self.wait()
        self.play(
            FadeOut(estimate),
            FadeOut(roughly_two),
            faders.animate.restore(),
        )

        # Setup for the trick
        box = Rectangle(
            height=plane.get_height(),
            width=abs(plane.get_right()[0] - RIGHT_SIDE[0]) - 1,
        )
        box.set_stroke(WHITE, 1)
        box.set_fill(GREY_E, 1)
        box.next_to(plane, RIGHT, buff=0.5)
        self.disable_interaction(box)
        trick_title = Text("The trick")
        trick_title.next_to(box.get_top(), DOWN, SMALL_BUFF)

        subsets = get_subsets(range(1, 6))
        binom_pairs = [
            (f_zeta[i], f_zeta[j:k])
            for i, j, k in [(7, 9, 10), (12, 14, 16), (18, 20, 22), (24, 26, 28), (30, 32, 34)]
        ]
        rect_groups = VGroup(*(
            VGroup(*(
                SurroundingRectangle(bp[int(n + 1 in ss)], buff=SMALL_BUFF).round_corners().set_stroke(TEAL, 2)
                for n, bp in enumerate(binom_pairs)
            ))
            for ss in subsets
        ))
        terms = VGroup(*(
            Tex(f"\\zeta^{{{sum(ss)}}}")
            for ss in subsets
        ))
        terms.arrange_in_grid(4, 8, buff=MED_LARGE_BUFF)
        terms.set_width(7)
        terms.next_to(plane, RIGHT, LARGE_BUFF, UP)
        for term in terms:
            term[0].set_color(YELLOW)
            plus = Tex("+", font_size=36)
            plus.next_to(term, RIGHT, buff=(0.15 if term in terms[:25] else 0.05))
            term.add(plus)
        terms[-1].remove(terms[-1][-1])
        term_rects = VGroup(*(
            SurroundingRectangle(term).round_corners().set_stroke(TEAL, 2)
            for term in terms
        ))

        self.play(FadeOut(lower_group, DOWN))
        self.play(
            ShowSubmobjectsOneByOne(rect_groups, int_func=np.ceil),
            ShowSubmobjectsOneByOne(term_rects, int_func=np.ceil),
            ShowIncreasingSubsets(terms, int_func=np.ceil),
            run_time=8,
            rate_func=linear,
        )
        self.play(FadeOut(rect_groups[-1]), FadeOut(term_rects[-1]))
        self.wait()

        self.play(
            FadeOut(terms, DOWN),
            Write(box),
            Write(trick_title),
        )
        self.wait()

        # The trick
        root_kw["tex_to_color_map"]["{z}"] = GREY_A
        root_kw["tex_to_color_map"]["{-1}"] = GREY_A
        root_kw["tex_to_color_map"]["="] = WHITE
        texs = [
            "{z}^5 - 1 = ({z} - \\zeta^0)({z} - \\zeta^1)({z} - \\zeta^2)({z} - \\zeta^3)({z} - \\zeta^4)",
            "({-1})^5 - 1 = ({-1} - \\zeta^0)({-1} - \\zeta^1)({-1} - \\zeta^2)({-1} - \\zeta^3)({-1} - \\zeta^4)",
            "2 = (1 + \\zeta^0)(1 + \\zeta^1)(1 + \\zeta^2)(1 + \\zeta^3)(1 + \\zeta^4)",
        ]
        equations = VGroup(*(Tex(tex, **root_kw) for tex in texs))
        equations[1].set_width(box.get_width() - 0.5)
        equations.arrange(DOWN, buff=0.75)
        equals_x = equations[0].get_part_by_tex("=").get_x()
        for eq in equations[1:]:
            eq.shift((equals_x - eq.get_part_by_tex("=").get_x()) * RIGHT)
        equations.next_to(trick_title, DOWN, MED_LARGE_BUFF)

        self.play(Write(equations[0]))
        self.wait()
        self.play(FadeTransform(equations[0].copy(), equations[1]))
        self.wait()
        self.play(FadeTransform(equations[1].copy(), equations[2]))
        self.wait()

        # Show value of 2
        brace = Brace(f_zeta[6:35], DOWN).set_color(WHITE)
        brace.stretch(0.75, 1, about_edge=UP)
        two_label = brace.get_tex("2").set_color(WHITE)
        self.play(GrowFromCenter(brace))
        self.play(TransformFromCopy(equations[2][0], two_label))
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(box, trick_title, *equations)))
        self.play(FadeIn(lower_group))
        self.wait()

        # Evaluate answer
        ans_group, expr_group = lower_group
        self.play(
            ans_group.animate.scale(0.5, about_edge=UL),
            expr_group.animate.scale(1.5, about_edge=DR),
        )
        self.wait()

        parts = [expr.get_part_by_tex(f"f(\\zeta^{{{n}}})") for n in range(5)]
        arrows = VGroup(*(
            Vector(0.5 * UP).next_to(part, UP, SMALL_BUFF)
            for part in parts
        ))
        values = VGroup(
            Tex("2^{2{,}000}", font_size=36),
            *(Tex("2^{400}", font_size=36) for x in range(4))
        )
        for value, arrow in zip(values, arrows):
            value.next_to(arrow, UP, SMALL_BUFF)

        self.play(
            ShowCreation(arrows[1]),
            FadeIn(values[1], 0.5 * UP)
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, arrows[2:], lag_ratio=0.5),
            LaggedStartMap(FadeIn, values[2:], shift=0.5 * UP, lag_ratio=0.5),
        )
        self.wait()
        self.play(
            ShowCreation(arrows[0]),
            FadeIn(values[0], 0.5 * UP)
        )
        self.wait()
        self.remove(arrows, values)
        expr_group.add(*arrows, *values)

        # Rescale answer group
        plane_group = Group(
            plane, unit_circle, new_circle,
            root_lines, root_dots, zp1_labels,
            complex_plane_title,
        )

        ans_group.generate_target()
        ans_group.target.set_width(6.5, about_edge=LEFT)
        ans_group.target.next_to(brace, DOWN)
        ans_group.target.shift(1 * LEFT)
        ans_group.target[0].set_stroke(opacity=0)

        f_zeta_rhs = OldTex("=2^{400}").set_color(WHITE)
        f_zeta_rhs.next_to(f_zeta, RIGHT)

        self.play(
            MoveToTarget(ans_group),
            expr_group.animate.scale(1 / 1.5, about_edge=DR),
            plane_group.animate.scale(0.7, about_edge=DL),
            TransformMatchingShapes(two_label, f_zeta_rhs),
            FadeOut(brace),
            run_time=2
        )
        self.wait()

        # Final answer
        final_answer = Tex(
            "= \\frac{1}{5}\\Big("
            "2^{2{,}000} + 4 \\cdot 2^{400}\\Big)"
        )
        final_answer.next_to(answer, RIGHT)

        final_answer_rect = SurroundingRectangle(final_answer[1:], buff=0.2)
        final_answer_rect.round_corners()
        final_answer_rect.set_stroke(YELLOW, 2)
        self.disable_interaction(final_answer_rect)

        self.play(
            Write(final_answer[:5]),
            Write(final_answer[-1]),
        )
        self.wait()
        self.play(
            FadeTransform(values.copy(), final_answer[5:-1])
        )
        self.play(ShowCreation(final_answer_rect))
        self.wait(note="Comment on dominant term")

        # Smaller case
        box = Rectangle(
            width=(RIGHT_SIDE[0] - plane.get_right()[0]) - 1,
            height=plane.get_height()
        )
        box.to_corner(DR)
        box.align_to(plane, DOWN)
        box.set_stroke(WHITE, 1)
        box.set_fill(GREY_E, 1)
        set_tex = get_set_tex(range(1, 6))
        set_tex.next_to(box.get_left(), RIGHT, SMALL_BUFF)

        rhs = Tex(
            "\\rightarrow \\frac{1}{5}"
            "\\Big(2^5 + 4 \\cdot 2^1\\Big)"
            "= \\frac{1}{5}(32 + 8)"
            "=8"
        )
        rhs.scale(0.9)
        rhs.next_to(set_tex, RIGHT)

        self.play(
            FadeOut(expr_group),
            Write(box),
            Write(set_tex),
        )
        self.wait()
        self.play(
            Write(rhs[0]),
            FadeTransform(final_answer.copy(), rhs[1:13])
        )
        self.wait()
        self.play(Write(rhs[13:]))
        self.wait()

    def animate_kth_power(self, plane, dots, k):
        # Try the rotation
        angles = np.angle([plane.p2n(dot.get_center()) for dot in dots])
        angles = angles % TAU
        paths = [
            ParametricCurve(
                lambda t: plane.n2p(np.exp(complex(0, interpolate(angle, k * angle, t)))),
                t_range=(0, 1, 0.01),
            )
            for angle in angles
        ]
        dots.save_state()
        # pentagon.add_updater(lambda p: p.set_points_as_corners([
        #     d.get_center() for d in [*dots, dots[0]]
        # ]))

        self.play(*(
            MoveAlongPath(dot, path)
            for dot, path in zip(dots, paths)
        ), run_time=4)
        if k == 5:
            self.wait()
            self.play(dots.animate.restore())
        else:
            # self.play(FadeOut(pentagon))
            dots.restore()
            # self.play(FadeInFromDown(pentagon))
        # pentagon.clear_updaters()

    def get_highlight(self, mobject):
        result = super().get_highlight(mobject)
        if isinstance(mobject, Arrow):
            result.set_stroke(width=result.get_stroke_width())
        return result
