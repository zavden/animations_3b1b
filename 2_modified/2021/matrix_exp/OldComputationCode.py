# ==============================================================================
# Scene:      OldComputationCode
# Source:     videos/_2021/matrix_exp.py (lines 6285-6431)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OldComputationCode.py OldComputationCode -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The variables of IntroduceTheComputation that the original uses without defining (randy, morty, real_equation, taylor_brace, taylor_label, false_group) are rebuilt at the start: NameError in the original.
#   - false_equation changes from a one-piece OldTex to a VGroup of two OldTex (left side and product): false_equation[1] gave IndexError.
# ==============================================================================

from manim_imports_ext import *

class OldComputationCode(Scene):
    def construct(self):
        # CHANGE: in the original this scene uses variables of IntroduceTheComputation (randy, morty, real_equation,
        # CHANGE: taylor_brace, taylor_label, false_group) that do not exist here (NameError); they are rebuilt as
        # CHANGE: they are left at the end of that scene so that the Taylor series animation can run.
        randy = Randolph()
        randy.set_height(2)
        randy.to_corner(DL)
        morty = Mortimer()
        morty.match_height(randy)
        morty.to_corner(DR)

        # CHANGE: false_equation was a one-piece OldTex and false_equation[1] gave IndexError; now there are two pieces (left side and product), as in the original
        false_equation = VGroup(OldTex("e^{M} ="), OldTex("e \\cdot e \\dots e \\cdot e"))
        false_equation.arrange(RIGHT)
        fe_rect = SurroundingRectangle(false_equation)
        fe_rect.set_color(GREY_BROWN)
        cross = Cross(false_equation[1])
        cross.insert_n_curves(1)
        cross.set_stroke(RED, width=[1, 5, 1])
        nonsense = Text("This would be nonsense")
        nonsense.match_width(fe_rect)
        nonsense.next_to(fe_rect, UP)
        nonsense.set_color(RED)
        false_group = VGroup(false_equation, fe_rect, cross, nonsense)
        false_group.scale(0.7).to_edge(DOWN)

        real_equation = OldTex(
            "e^x = x^0 + x^1 + \\frac{1}{2} x^2 + \\frac{1}{6} x^3 + \\cdots + \\frac{1}{n!} x^n + \\cdots",
            isolate=["x"]
        )
        xs = real_equation.get_parts_by_tex("x")
        xs.set_color(YELLOW)
        real_equation.set_width(FRAME_WIDTH - 2.0)
        real_equation.to_edge(UP)
        taylor_brace = Brace(real_equation[3:], DOWN)
        taylor_label = taylor_brace.get_text("Taylor series")
        self.add(randy, morty, false_group, real_equation, taylor_brace, taylor_label)

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
