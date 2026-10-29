# ==============================================================================
# Scene:      ShowHigherMatrixPowers
# Source:     videos/_2021/matrix_exp.py (lines 1246-1316)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowHigherMatrixPowers.py ShowHigherMatrixPowers -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
#   - np.matrix(...) -> np.array(...): Matrix no longer converts with np.array(matrix, ndmin=2) and when iterating an np.matrix each element is an np.matrix (DecimalNumber fails).
# ==============================================================================

from manim_imports_ext import *

class IntroduceTheComputation(Scene):
    def construct(self):
        # Matrix in exponent
        base = OldTex("e")
        base.set_height(1.0)
        matrix = IntegerMatrix(
            [[3, 1, 4],
             [1, 5, 9],
             [2, 6, 5]],
        )
        matrix.move_to(base.get_corner(UR), DL)
        matrix_exp = VGroup(base, matrix)
        matrix_exp.set_height(2)
        matrix_exp.to_corner(UL)
        matrix_exp.shift(3 * RIGHT)

        randy = Randolph()
        randy.set_height(2)
        randy.to_corner(DL)

        matrix.save_state()
        matrix.center()
        matrix.set_height(2.5)

        self.add(randy)
        self.play(
            randy.change("pondering", matrix),
            Write(matrix.get_brackets()),
            ShowIncreasingSubsets(matrix.get_entries()),
        )
        self.play(
            matrix.animate.restore(),
            Write(base),
            randy.change("erm", base),
        )
        self.play(Blink(randy))

        # Question the repeated multiplication implication
        rhs = OldTex("= e \\cdot e \\dots e \\cdot e")
        rhs.set_height(0.75 * base.get_height())
        rhs.next_to(matrix_exp, RIGHT)
        rhs.align_to(base, DOWN)
        brace = Brace(rhs[0][1:], DOWN)
        matrix_copy = matrix.copy()
        matrix_copy.scale(0.5)
        brace_label = VGroup(
            matrix.copy().scale(0.5),
            Text("times?")
        )
        brace_label.arrange(RIGHT)
        brace_label.next_to(brace, DOWN, SMALL_BUFF)

        bubble = randy.get_bubble(
            OldTexText("I'm sorry,\\\\what?!").scale(0.75),
            height=2,
            width=3,
            bubble_type=SpeechBubble,
        )

        self.play(
            TransformMatchingParts(
                base.copy(), rhs,
                path_arc=10 * DEGREES,
                lag_ratio=0.01,
            ),
            GrowFromCenter(brace),
            ReplacementTransform(
                matrix.copy(), brace_label[0],
                path_arc=30 * DEGREES,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.3, 1),
            ),
            Write(
                brace_label[1],
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.5, 1),
            ),
            randy.change("angry", rhs),
            ShowCreation(bubble),
            Write(bubble.content, run_time=1),
        )
        self.wait()

        false_equation = VGroup(
            matrix_exp, rhs, brace, brace_label
        )

        # This is nonsense.
        morty = Mortimer()
        morty.match_height(randy)
        morty.to_corner(DR)
        morty.set_opacity(0)
        false_equation.generate_target()
        false_equation.target.scale(0.5)
        false_equation.target.next_to(morty, UL)
        fe_rect = SurroundingRectangle(false_equation.target)
        fe_rect.set_color(GREY_BROWN)
        cross = Cross(false_equation.target[1])
        cross.insert_n_curves(1)
        cross.set_stroke(RED, width=[1, 5, 1])
        nonsense = Text("This would be nonsense")
        nonsense.match_width(fe_rect)
        nonsense.next_to(fe_rect, UP)
        nonsense.set_color(RED)

        randy.bubble = bubble
        self.play(
            MoveToTarget(false_equation),
            RemovePiCreatureBubble(randy, target_mode="hesitant"),
            morty.animate.set_opacity(1).change("raise_right_hand"),
            ShowCreation(fe_rect),
        )
        self.play(
            ShowCreation(cross),
            FadeIn(nonsense),
        )
        self.play(Blink(morty))
        self.wait()

        false_group = VGroup(false_equation, fe_rect, cross, nonsense)

        # Show Taylor series
        real_equation = OldTex(
            "e^x = x^0 + x^1 + \\frac{1}{2} x^2 + \\frac{1}{6} x^3 + \\cdots + \\frac{1}{n!} x^n + \\cdots",
            isolate=["x"]
        )
        xs = real_equation.get_parts_by_tex("x")
        xs.set_color(YELLOW)
        real_equation.set_width(FRAME_WIDTH - 2.0)
        real_equation.to_edge(UP)
        real_rhs = real_equation[3:]

        real_label = Text("Real number", color=YELLOW, font_size=24)
        # real_label.next_to(xs[0], DOWN, buff=0.8)
        # real_label.to_edge(LEFT, buff=MED_SMALL_BUFF)
        # real_arrow = Arrow(real_label, xs[0], buff=0.1, fill_color=GREY_B, thickness=0.025)
        real_label.to_corner(UL, buff=MED_SMALL_BUFF)
        real_arrow = Arrow(real_label, real_equation[1], buff=0.1)

        taylor_brace = Brace(real_rhs, DOWN)
        taylor_label = taylor_brace.get_text("Taylor series")

        self.play(
            TransformFromCopy(base, real_equation[0]),
            FadeTransform(matrix.copy(), real_equation[1]),
            FadeIn(real_label, UR),
            GrowArrow(real_arrow),
            randy.change("thinking", real_label),
            morty.animate.look_at(real_label),
        )
        self.wait()
        self.play(
            Write(real_equation[2], lag_ratio=0.2),
            FadeTransformPieces(xs[:1].copy(), xs[1:], path_arc=20 * DEGREES),
            LaggedStart(*(
                FadeIn(part)
                for part in real_equation[4:]
                if part not in xs
            )),
            randy.change("pondering", real_equation),
            morty.change("pondering", real_equation),
        )
        self.add(real_equation)
        self.play(Blink(morty))
        self.play(
            false_group.animate.scale(0.7).to_edge(DOWN),
            GrowFromCenter(taylor_brace),
            FadeIn(taylor_label, 0.5 * DOWN)
        )
        self.wait()

        # Taylor series example
        ex_rhs = OldTex(
            """
            {2}^0 +
            {2}^1 +
            { {2}^2 \\over 2} +
            { {2}^3 \\over 6} +
            { {2}^4 \\over 24} +
            { {2}^5 \\over 120} +
            { {2}^6 \\over 720} +
            { {2}^7 \\over 5040} +
            \\cdots
            """,
            tex_to_color_map={"{2}": YELLOW, "+": WHITE},
        )
        ex_rhs.next_to(real_equation[3:], DOWN, buff=0.75)

        ex_parts = VGroup(*(
            ex_rhs[i:j] for i, j in [
                (0, 2),
                (3, 5),
                (6, 8),
                (9, 11),
                (12, 14),
                (15, 17),
                (18, 20),
                (21, 23),
                (24, 25),
            ]
        ))
        term_brace = Brace(ex_parts[0], DOWN)
        frac = OldTex("1", font_size=36)
        frac.next_to(term_brace, DOWN, SMALL_BUFF)

        rects = VGroup(*(
            Rectangle(height=2**n / math.factorial(n), width=1)
            for n in range(11)
        ))
        rects.arrange(RIGHT, buff=0, aligned_edge=DOWN)
        rects.set_fill(opacity=1)
        rects.set_submobject_colors_by_gradient(BLUE, GREEN)
        rects.set_stroke(WHITE, 1)
        rects.set_width(7)
        rects.to_edge(DOWN)

        self.play(
            ReplacementTransform(taylor_brace, term_brace),
            FadeTransform(real_equation[3:].copy(), ex_rhs),
            FadeOut(false_group, shift=DOWN),
            FadeOut(taylor_label, shift=DOWN),
            FadeIn(frac),
        )
        term_values = VGroup()
        for n in range(11):
            rect = rects[n]
            fact = math.factorial(n)
            ex_part = ex_parts[min(n, len(ex_parts) - 1)]
            value = DecimalNumber(2**n / fact)
            value.set_color(GREY_A)
            max_width = 0.6 * rect.get_width()
            if value.get_width() > max_width:
                value.set_width(max_width)
            value.next_to(rects[n], UP, SMALL_BUFF)
            new_brace = Brace(ex_part, DOWN)
            if fact == 1:
                new_frac = OldTex(f"{2**n}", font_size=36)
            else:
                new_frac = OldTex(f"{2**n} / {fact}", font_size=36)
            new_frac.next_to(new_brace, DOWN, SMALL_BUFF)
            self.play(
                term_brace.animate.become(new_brace),
                FadeTransform(frac, new_frac),
            )
            frac = new_frac
            rect.save_state()
            rect.stretch(0, 1, about_edge=DOWN)
            rect.set_opacity(0)
            value.set_value(0)
            self.play(
                Restore(rect),
                ChangeDecimalToValue(value, 2**n / math.factorial(n)),
                UpdateFromAlphaFunc(value, lambda m, a: m.next_to(rect, UP, SMALL_BUFF).set_opacity(a)),
                randy.animate.look_at(rect),
                morty.animate.look_at(rect),
            )
            term_values.add(value)
        self.play(FadeOut(frac))

        new_brace = Brace(ex_rhs, DOWN)
        sum_value = DecimalNumber(math.exp(2), num_decimal_places=4, font_size=36)
        sum_value.next_to(new_brace, DOWN)
        self.play(
            term_brace.animate.become(new_brace),
            randy.change("thinking", sum_value),
            morty.change("tease", sum_value),
            *(FadeTransform(dec.copy().set_opacity(0), sum_value) for dec in term_values)
        )
        self.play(Blink(randy))

        lhs = OldTex("e \\cdot e =")
        lhs.match_height(real_equation[0])
        lhs.next_to(ex_rhs, LEFT)
        self.play(Write(lhs))
        self.play(Blink(morty))
        self.play(Blink(randy))

        # Increment input
        twos = ex_rhs.get_parts_by_tex("{2}")
        threes = VGroup(*(
            OldTex("3").set_color(YELLOW).replace(two)
            for two in twos
        ))
        new_lhs = OldTex("e \\cdot e \\cdot e = ")
        new_lhs.match_height(lhs)
        new_lhs[0].space_out_submobjects(0.8)
        new_lhs[0][-1].shift(SMALL_BUFF * RIGHT)
        new_lhs.move_to(lhs, RIGHT)

        anims = []
        unit_height = 0.7 * rects[0].get_height()
        for n, rect, value_mob in zip(it.count(0), rects, term_values):
            rect.generate_target()
            new_value = 3**n / math.factorial(n)
            rect.target.set_height(unit_height * new_value, stretch=True, about_edge=DOWN)
            value_mob.rect = rect
            anims += [
                MoveToTarget(rect),
                ChangeDecimalToValue(value_mob, new_value),
                UpdateFromFunc(value_mob, lambda m: m.next_to(m.rect, UP, SMALL_BUFF))
            ]

        self.play(
            FadeOut(twos, 0.5 * UP),
            FadeIn(threes, 0.5 * UP),
        )
        twos.set_opacity(0)
        self.play(
            ChangeDecimalToValue(sum_value, math.exp(3)),
            *anims,
        )
        self.play(
            FadeOut(lhs, 0.5 * UP),
            FadeIn(new_lhs, 0.5 * UP),
        )
        self.wait()

        # Isolate polynomial
        real_lhs = VGroup(real_equation[:3], real_label, real_arrow)

        self.play(
            LaggedStartMap(FadeOut, VGroup(
                *new_lhs, *threes, *ex_rhs,
                term_brace, sum_value,
                *rects, *term_values,
            )),
            real_lhs.animate.set_opacity(0.2),
            randy.change("erm", real_equation),
            morty.change("thinking", real_equation),
            run_time=1,
        )
        self.play(Blink(morty))

        # Alternate inputs
        rhs_tex = "X^0 + X^1 + \\frac{1}{2} X^2 + \\frac{1}{6} X^3 + \\cdots + \\frac{1}{n!} X^n + \\cdots"
        pii_rhs = OldTex(
            rhs_tex.replace("X", "(\\pi i)"),
            tex_to_color_map={"(\\pi i)": BLUE},
        )
        pii_rhs.match_width(real_rhs)

        mat_tex = "\\left[ \\begin{array}{ccc} 3 & 1 & 4 \\\\ 1 & 5 & 9 \\\\ 2 & 6 & 5 \\end{array} \\right]"
        mat_rhs = OldTex(
            rhs_tex.replace("X", mat_tex),
            tex_to_color_map={mat_tex: TEAL},
        )
        mat_rhs.scale(0.5)

        pii_rhs.next_to(real_rhs, DOWN, buff=0.7)
        mat_rhs.next_to(pii_rhs, DOWN, buff=0.7)

        self.play(FlashAround(real_rhs))
        self.wait()
        self.play(
            morty.change("raise_right_hand", pii_rhs),
            FadeTransformPieces(real_rhs.copy(), pii_rhs),
        )
        self.play(Blink(randy))
        self.play(
            FadeTransformPieces(real_rhs.copy(), mat_rhs),
        )
        self.play(
            randy.change("maybe", mat_rhs),
        )
        self.wait()

        why = Text("Why?", font_size=36)
        why.next_to(randy, UP, aligned_edge=LEFT)
        self.play(
            randy.change("confused", mat_rhs.get_corner(UL)),
            Write(why),
        )
        self.play(Blink(randy))

        reassurance = VGroup(
            Text("I know it looks complicated.", font_size=24),
            Text("Don't panic.", font_size=24),
        )
        reassurance.arrange(DOWN)
        reassurance.next_to(morty, LEFT, aligned_edge=UP)
        reassurance.set_color(GREY_A)

        for words in reassurance:
            self.play(FadeIn(words))
        self.play(Blink(morty))

        # Describe exp
        to_right_group = VGroup(real_lhs, real_rhs, mat_rhs, pii_rhs)
        to_right_group.generate_target()
        to_right_group.target.to_edge(RIGHT, buff=SMALL_BUFF)
        to_right_group.target[2].to_edge(RIGHT, buff=SMALL_BUFF)
        self.play(
            MoveToTarget(to_right_group),
            FadeOut(why),
            FadeOut(reassurance),
            randy.change("pondering", mat_rhs),
            morty.change("tease"),
        )

        pii_lhs = OldTex("\\text{exp}\\left(\\pi i \\right) = ")[0]
        pii_lhs.next_to(pii_rhs, LEFT)
        mat_lhs = OldTex("\\text{exp}\\left(" + mat_tex + "\\right) = ")[0]
        mat_lhs.match_height(mat_rhs)
        mat_lhs[:3].match_height(pii_lhs[:3])
        mat_lhs[:3].next_to(mat_lhs[3:5], LEFT, SMALL_BUFF)
        mat_lhs.next_to(mat_rhs, LEFT)

        pii_lhs_pi_part = pii_lhs[4:6]
        pii_lhs_pi_part.set_color(BLUE)
        mat_lhs_mat_part = mat_lhs[5:18]
        mat_lhs_mat_part.set_color(TEAL)

        self.play(
            FadeIn(pii_lhs),
            randy.change("thinking", pii_lhs),
            randy.change("tease", pii_lhs),
        )
        self.play(FadeIn(mat_lhs))
        self.play(Blink(randy))
        self.play(
            LaggedStart(
                FlashAround(pii_lhs[:3]),
                FlashAround(mat_lhs[:3]),
                lag_ratio=0.3,
                run_time=2
            ),
            randy.change("raise_left_hand", pii_lhs),
        )
        self.wait()

        # Transition to e^x notation
        crosses = VGroup(*(
            Cross(lhs[:3], stroke_width=[0, 3, 3, 3, 0]).scale(1.3)
            for lhs in [pii_lhs, mat_lhs]
        ))
        bases = VGroup()
        powers = VGroup()
        equals = VGroup()
        for part, lhs in (pii_lhs_pi_part, pii_lhs), (mat_lhs_mat_part, mat_lhs):
            power = part.copy()
            part.set_opacity(0)
            self.add(power)
            base = OldTex("e", font_size=60)
            equal = OldTex(":=")
            power.generate_target()
            if power.target.get_height() > 0.7:
                power.target.set_height(0.7)
            power.target.next_to(base, UR, buff=0.05)
            group = VGroup(base, power.target, equal)
            equal.next_to(group[:2], RIGHT, MED_SMALL_BUFF)
            equal.match_y(base)
            if lhs is mat_lhs:
                equal.shift(0.1 * UP)
            group.shift(lhs.get_right() - equal.get_right())
            bases.add(base)
            powers.add(power)
            equals.add(equal)

        self.play(
            ShowCreation(crosses),
            randy.change("hesitant", crosses),
        )
        self.play(Blink(randy))
        self.play(real_lhs.animate.set_opacity(1))

        self.play(
            FadeOut(pii_lhs),
            FadeOut(mat_lhs),
            FadeOut(crosses),
            *(MoveToTarget(power) for power in powers),
            *(TransformFromCopy(real_equation[0], base) for base in bases),
            Write(equals),
            randy.change("sassy", powers),
        )
        self.wait()

        # Theorem vs. definition
        real_part = VGroup(real_lhs, real_rhs)
        pii_part = VGroup(bases[0], powers[0], equals[0], pii_rhs)
        mat_part = VGroup(bases[1], powers[1], equals[1], mat_rhs)
        def_parts = VGroup(pii_part, mat_part)

        self.play(
            FadeOut(randy, DOWN),
            FadeOut(morty, DOWN),
            real_part.animate.set_x(0).shift(DOWN),
            def_parts.animate.set_x(0).to_edge(DOWN),
        )

        real_rect = SurroundingRectangle(real_part)
        real_rect.set_stroke(YELLOW, 2)
        theorem_label = Text("Theorem")
        theorem_label.next_to(real_rect, UP)

        def_rect = SurroundingRectangle(def_parts)
        def_rect.set_stroke(BLUE, 2)
        def_label = Text("Definition")
        def_label.next_to(def_rect, UP)

        self.play(
            ShowCreation(real_rect),
            FadeIn(theorem_label, 0.5 * UP),
        )
        self.wait()
        self.play(
            ShowCreation(def_rect),
            FadeIn(def_label, 0.5 * UP),
        )
        self.wait()

        # Abuse?  Or the beauty of discovery...
        randy2 = Randolph()
        randy2.set_height(1.5)
        randy2.next_to(def_rect, UP, SMALL_BUFF, aligned_edge=LEFT)

        self.play(
            ApplyMethod(randy2.change, "angry", mat_rhs),
            UpdateFromAlphaFunc(randy2, lambda m, a: m.set_opacity(a)),
        )
        self.play(Blink(randy2))

        discovery_label = Text("Discovery")
        discovery_label.move_to(theorem_label, DOWN)
        invention_label = Text("Invention")
        invention_label.move_to(def_label, DOWN)

        self.play(
            FadeOut(theorem_label, UP),
            FadeIn(discovery_label, UP),
            randy2.change("hesitant", theorem_label),
        )
        self.play(
            FadeOut(def_label, UP),
            FadeIn(invention_label, UP),
        )
        self.wait(2)

        # Isolate matrix right hand side
        to_fade = VGroup(
            randy2, discovery_label, invention_label,
            real_rect, def_rect,
            real_arrow, real_label, real_part, pii_part,
            bases, powers, equals,
        )

        self.play(
            mat_rhs.animate.set_width(FRAME_WIDTH - 1).center().to_edge(UP),
            LaggedStartMap(FadeOut, to_fade),
            FadeIn(VGroup(randy, morty), run_time=2, rate_func=squish_rate_func(smooth, 0.5, 1))
        )

        # Matrix powers
        mat = mat_rhs[4]
        mat_brace = Brace(VGroup(mat, mat_rhs[5][0]), DOWN, buff=SMALL_BUFF)
        matrix = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
        matrix_square = np.dot(matrix, matrix)
        result = IntegerMatrix(matrix_square, h_buff=1.3, v_buff=0.7)
        result.match_height(mat)
        square_eq = VGroup(mat.copy(), mat.copy(), OldTex("="), result)
        square_eq.arrange(RIGHT, buff=SMALL_BUFF)
        square_eq.next_to(mat_brace, DOWN)

        self.play(GrowFromCenter(mat_brace))
        self.play(
            LaggedStart(
                TransformFromCopy(mat, square_eq[0], path_arc=45 * DEGREES),
                TransformFromCopy(mat, square_eq[1]),
                Write(square_eq[2]),
                Write(result.brackets),
            ),
            randy.change("pondering", square_eq),
        )
        self.show_mat_mult(matrix, matrix, square_eq[0][2:11], square_eq[1][2:11], result.elements)

        # Show matrix cubed
        mat_brace.generate_target()
        mat_brace.target.next_to(mat_rhs[6], DOWN, SMALL_BUFF)

        mat_squared = result
        mat_cubed = IntegerMatrix(
            np.dot(matrix, matrix_square),
            h_buff=1.8, v_buff=0.7,
            element_alignment_corner=ORIGIN,
        )
        mat_cubed.match_height(mat)
        cube_eq = VGroup(
            VGroup(mat.copy(), mat.copy(), mat.copy()).arrange(RIGHT, buff=SMALL_BUFF),
            OldTex("=").rotate(90 * DEGREES),
            VGroup(mat.copy(), mat_squared.deepcopy()).arrange(RIGHT, buff=SMALL_BUFF),
            OldTex("=").rotate(90 * DEGREES),
            mat_cubed
        )
        cube_eq.arrange(DOWN)
        cube_eq.next_to(mat_brace.target, DOWN)

        self.play(
            MoveToTarget(mat_brace),
            ReplacementTransform(square_eq[0], cube_eq[0][1]),
            ReplacementTransform(square_eq[1], cube_eq[0][2]),
            ReplacementTransform(square_eq[2], cube_eq[1]),
            ReplacementTransform(square_eq[3], cube_eq[2][1]),
            randy.change("happy", cube_eq),
        )
        self.play(
            LaggedStart(
                FadeIn(cube_eq[0][0]),
                FadeIn(cube_eq[2][0]),
                FadeIn(cube_eq[3]),
                FadeIn(cube_eq[4].brackets),
            ),
            randy.change("tease", cube_eq),
        )
        self.show_mat_mult(
            matrix, matrix_square,
            cube_eq[2][0][2:11],
            cube_eq[2][1].get_entries(),
            cube_eq[4].get_entries(),
            0.1, 0.1,
        )
        self.play(Blink(morty))

        # Scaling
        example_matrix = Matrix([
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"],
        ])
        example_scaled_matrix = Matrix([
            ["a / n!", "b / n!", "c / n!"],
            ["d / n!", "e / n!", "f / n!"],
            ["g / n!", "h / n!", "i / n!"],
        ])
        factor = OldTex("1 \\over n!")
        factor.scale(1.5)
        factor.next_to(example_matrix, LEFT, MED_SMALL_BUFF)

        self.play(
            LaggedStartMap(FadeOut, VGroup(mat_brace, *cube_eq[:-1])),
            FadeIn(factor),
            FadeTransformPieces(cube_eq[-1], example_matrix),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                VGroup(*factor, *example_matrix),
                example_scaled_matrix,
            ),
            randy.change("pondering", example_scaled_matrix),
        )
        self.wait()

        # Adding
        mat1 = np.array([[2, 7, 1], [8, 2, 8], [1, 8, 2]])
        mat2 = np.array([[8, 4, 5], [9, 0, 4], [5, 2, 3]])

        sum_eq = VGroup(
            IntegerMatrix(mat1),
            OldTex("+"),
            IntegerMatrix(mat2),
            OldTex("="),
            Matrix(
                np.array([
                    f"{m1} + {m2}"
                    for m1, m2 in zip(mat1.flatten(), mat2.flatten())
                ]).reshape((3, 3)),
                h_buff=1.8,
            )
        )
        sum_eq.set_height(1.5)
        sum_eq.arrange(RIGHT)
        sum_eq.center()

        self.play(
            FadeOut(example_scaled_matrix, UP),
            FadeIn(sum_eq[:-1], UP),
            FadeIn(sum_eq[-1].brackets, UP),
            morty.change("raise_right_hand", sum_eq),
            randy.change("thinking", sum_eq),
        )

        last_rects = VGroup()
        for e1, e2, e3 in zip(sum_eq[0].elements, sum_eq[2].elements, sum_eq[4].elements):
            rects = VGroup(SurroundingRectangle(e1), SurroundingRectangle(e2))
            self.add(e3, rects)
            self.play(FadeOut(last_rects), run_time=0.2)
            self.wait(0.1)
            last_rects = rects
        self.play(FadeOut(last_rects))

        # Ask about infinity
        bubble = randy.get_bubble(OldTexText("But...going\\\\to $\\infty$?"))
        bubble.shift(SMALL_BUFF * RIGHT)
        self.play(
            Write(bubble),
            Write(bubble.content),
            FadeOut(sum_eq, UP),
            randy.change("sassy", mat_rhs),
            morty.change("guilty", randy.eyes),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeOut(bubble),
            bubble.content.animate.next_to(randy, RIGHT, aligned_edge=UP),
            randy.change("pondering", mat_rhs),
            morty.change("pondering", mat_rhs),
        )

        # Replace matrix
        pi_mat_tex = ""
        pi_mat_tex = "\\left[ \\begin{array}{cc} 0 & -\\pi \\\\ \\pi & 0 \\end{array} \\right]"
        pi_mat_rhs = OldTex(
            rhs_tex.replace("X", pi_mat_tex),
            tex_to_color_map={pi_mat_tex: BLUE},
        )
        pi_mat_rhs.match_width(mat_rhs)
        pi_mat_rhs.move_to(mat_rhs)

        pi_mat = pi_mat_rhs.get_part_by_tex(pi_mat_tex).copy()
        pi_mat.scale(1.5)
        pi_mat.next_to(morty, UL)

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(pi_mat, UP)
        )
        self.play(Blink(morty))
        self.play(
            FadeTransformPieces(mat_rhs, pi_mat_rhs),
            Transform(
                VGroup(pi_mat),
                pi_mat_rhs.get_parts_by_tex(pi_mat_tex),
                remover=True,
            ),
            morty.change("tease"),
        )
        self.wait()

        # Show various partial sum values
        matrix = np.array([[0, -np.pi], [np.pi, 0]])
        curr_matrix = np.identity(2)
        curr_sum = np.identity(2)
        curr_sum_mob = IntegerMatrix(curr_matrix)
        curr_sum_mob.set_height(1.5)
        mat_parts = pi_mat_rhs.get_parts_by_tex(pi_mat_tex)

        brace = Brace(mat_parts[0], DOWN)
        brace.stretch(1.1, 0, about_edge=LEFT)
        curr_sum_mob.next_to(brace, DOWN)
        curr_sum_mob.shift_onto_screen()

        self.play(
            GrowFromCenter(brace),
            FadeTransform(mat_parts[0].copy(), curr_sum_mob),
            randy.change("erm", curr_sum_mob),
        )
        self.wait()

        last_n_label = VMobject()
        partial_sum_mobs = [curr_sum_mob]
        for n in range(1, 18):
            if n < 5:
                new_brace = Brace(mat_parts[:n + 1])
                new_brace.set_width(new_brace.get_width() + 0.2, about_edge=LEFT)
                brace.generate_target()
                brace.target.become(new_brace)
                anims = [
                    MoveToTarget(brace),
                ]
            else:
                n_label = OldTex(f"n = {n}", font_size=24)
                n_label.next_to(brace.get_corner(DR), DL, SMALL_BUFF)
                anims = [
                    FadeIn(n_label),
                    FadeOut(last_n_label),
                ]
                last_n_label = n_label

            curr_matrix = np.dot(curr_matrix, matrix) / n
            curr_sum += curr_matrix
            nd = min(n + 1, 4)
            if n < 2:
                h_buff = 1.3
            else:
                sample = DecimalMatrix(curr_sum[0], num_decimal_places=nd)
                sample.replace(curr_sum_mob.get_entries()[0], 1)
                h_buff = 1.3 * sample.get_width()
            new_sum_mob = DecimalMatrix(
                curr_sum,
                element_alignment_corner=RIGHT,
                # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
                num_decimal_places=nd, decimal_config={"font_size": 36},
                h_buff=h_buff,
            )
            new_sum_mob.match_height(curr_sum_mob)
            new_sum_mob.next_to(brace.target, DOWN)

            self.play(
                FadeOut(curr_sum_mob),
                FadeIn(new_sum_mob),
                randy.animate.look_at(new_sum_mob),
                *anims,
                run_time=(1 if n < 5 else 1 / 60)
            )
            self.wait()
            curr_sum_mob = new_sum_mob
            partial_sum_mobs.append(new_sum_mob)
        self.play(
            FadeOut(last_n_label),
            randy.change("confused", curr_sum_mob),
        )

        # Ask why
        why = Text("Why?")
        why.move_to(bubble.content, UL)
        epii = OldTex("e^{\\pi i} = -1")
        epii.next_to(morty, UL)
        later_text = Text("...but that comes later", font_size=24)
        later_text.set_color(GREY_A)
        later_text.next_to(epii, DOWN, aligned_edge=RIGHT)

        self.play(
            randy.change("maybe"),
            FadeIn(why, UP),
            FadeOut(bubble.content, UP),
        )
        self.wait()
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(epii, UP),
        )
        self.play(Blink(morty))
        self.play(
            Write(later_text, run_time=1),
            randy.change("hesitant", morty.eyes)
        )

        # Show partial sums
        new_mat_rhs = OldTex(
            rhs_tex.replace("X", mat_tex),
            tex_to_color_map={mat_tex: TEAL},
            isolate=["+"]
        )
        new_mat_rhs.replace(mat_rhs)
        self.play(
            FadeOut(pi_mat_rhs),
            FadeIn(new_mat_rhs),
            FadeOut(new_sum_mob, DOWN),
            brace.animate.become(Brace(new_mat_rhs, DOWN)),
            LaggedStartMap(
                FadeOut, VGroup(
                    why, epii, later_text,
                ),
                shift=DOWN,
            ),
            randy.change("pondering", new_mat_rhs),
            morty.change("pondering", new_mat_rhs),
        )

        matrix = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
        partial_sum_mobs = VGroup()
        curr_matrix = np.identity(3)
        partial_sum = np.array(curr_matrix)
        for n in range(50):
            psm = DecimalMatrix(
                partial_sum,
                # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
                num_decimal_places=2,
                element_alignment_corner=ORIGIN,
                h_buff=1.5 * DecimalNumber(partial_sum[0, 0]).get_width(),
                v_buff=1.0,
            )
            psm.next_to(brace, DOWN, MED_LARGE_BUFF)
            partial_sum_mobs.add(psm)
            curr_matrix = np.dot(curr_matrix, matrix) / (n + 1)
            partial_sum += curr_matrix

        new_mat_rhs[2:].set_opacity(0.1)
        self.add(partial_sum_mobs[0])
        self.wait(0.5)
        for n, k in zip(it.count(1), [5, 9, 13, 19, 21]):
            self.remove(partial_sum_mobs[n - 1])
            self.add(partial_sum_mobs[n])
            new_mat_rhs[:k].set_opacity(1)
            self.wait(0.5)
        brace.become(Brace(new_mat_rhs, DOWN))
        n_label = VGroup(OldTex("n = "), Integer(n))
        n_label[1].set_height(n_label[0].get_height() * 1.2)
        n_label.arrange(RIGHT, SMALL_BUFF)
        n_label.set_color(GREY_B)
        n_label.next_to(brace.get_corner(DR), DL, SMALL_BUFF)
        self.add(n_label)
        for n in range(6, 50):
            self.remove(partial_sum_mobs[n - 1])
            self.add(partial_sum_mobs[n])
            n_label[1].set_value(n)
            n_label[1].set_color(GREY_B)
            n_label[1].next_to(n_label[0], RIGHT, SMALL_BUFF)
            self.wait(0.1)
        self.play(
            randy.change("erm"),
            morty.change("tease"),
            # LaggedStartMap(
            #     FadeOut, VGroup(brace, n_label, partial_sum_mobs[n]),
            #     shift=DOWN,
            # )
        )
        self.play(Blink(morty))
        self.play(Blink(randy))
        self.wait()

    def show_mat_mult(self, m1, m2, m1_terms, m2_terms, rhs_terms, per_term=0.1, between_terms=0.35):
        dim = m1.shape[0]
        m1_color = m1_terms[0].get_fill_color()
        m2_color = m2_terms[0].get_fill_color()
        for n in range(dim * dim):
            i = n // dim
            j = n % dim
            row = m1_terms[dim * i:dim * i + dim]
            col = m2_terms[j::dim]
            row_rect = SurroundingRectangle(row, buff=0.05)
            col_rect = SurroundingRectangle(col, buff=0.05)
            row_rect.set_stroke(YELLOW, 2)
            col_rect.set_stroke(YELLOW, 2)
            right_elem = Integer(0, edge_to_fix=ORIGIN)
            right_elem.replace(rhs_terms[n], dim_to_match=1)
            right_elem.set_value(0)

            self.add(row_rect, col_rect, right_elem)
            for k in range(dim):
                self.wait(per_term)
                right_elem.increment_value(m1[i, k] * m2[k, j])
                right_elem.scale(rhs_terms[0][0].get_height() / right_elem[-1].get_height())
                row[k].set_color(YELLOW)
                col[k].set_color(YELLOW)
            self.remove(right_elem)
            self.add(rhs_terms[n])
            self.wait(between_terms)
            m1_terms.set_color(m1_color)
            m2_terms.set_color(m2_color)
            self.remove(row_rect, col_rect)


class ShowHigherMatrixPowers(IntroduceTheComputation):
    matrix = [[3, 1, 4], [1, 5, 9], [2, 6, 5]]
    per_term = 0.1
    between_terms = 0.1
    N_powers = 10

    def construct(self):
        # Show many matrix powers
        def get_mat_mob(matrix):
            term = Integer(matrix[0, 0])
            return IntegerMatrix(
                matrix,
                h_buff=max(0.8 + 0.3 * len(term), 1.0)
            )

        N = self.N_powers
        # CHANGE: np.matrix -> np.array: Matrix no longer converts the input with np.array(matrix, ndmin=2) and when iterating an np.matrix each row is another np.matrix
        matrix = np.array(self.matrix)
        matrix_powers = [np.identity(len(matrix)), matrix]
        for x in range(N):
            matrix_powers.append(np.dot(matrix, matrix_powers[-1]))

        mat_mobs = [get_mat_mob(mat) for mat in matrix_powers]
        for mob in mat_mobs:
            mob.set_height(1)
        mat_mobs[1].set_color(TEAL)

        equation = VGroup(
            mat_mobs[1].deepcopy(),
            Integer(2, font_size=18),
            OldTex("="),
            mat_mobs[1].deepcopy(),
            mat_mobs[1].deepcopy(),
            OldTex("="),
            mat_mobs[2].deepcopy()
        )
        equation.arrange(RIGHT)
        equation.to_edge(LEFT)
        equation[1].set_y(equation[0].get_top()[1])
        equation[0].set_x(equation[1].get_left()[0] - SMALL_BUFF, RIGHT)
        self.add(equation)

        exp = equation[1]
        m1, m2, eq, rhs = equation[-4:]
        self.remove(*rhs.get_entries())
        for n in range(3, N):
            self.show_mat_mult(
                matrix_powers[1], matrix_powers[n - 2],
                m1.get_entries(), m2.get_entries(), rhs.get_entries(),
                between_terms=self.between_terms,
                per_term=self.per_term
            )
            self.wait(0.5)
            rhs.generate_target()
            eq.generate_target()
            rhs.target.move_to(m2, LEFT)
            eq.target.next_to(rhs.target, RIGHT)
            new_rhs = mat_mobs[n].deepcopy()
            new_rhs.next_to(eq.target, RIGHT)
            new_exp = Integer(n)
            new_exp.replace(exp, dim_to_match=1)

            self.play(
                MoveToTarget(rhs, path_arc=PI / 2),
                MoveToTarget(eq),
                FadeOut(m2, DOWN),
                FadeIn(new_rhs.get_brackets()),
                FadeIn(new_exp, 0.5 * DOWN),
                FadeOut(exp, 0.5 * DOWN),
            )
            m2, rhs = rhs, new_rhs
            exp = new_exp
