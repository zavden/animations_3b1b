# ==============================================================================
# Scene:      CentralQuestionFor1e2
# Source:     videos/_2019/clacks/solution1.py (lines 2389-2450)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CentralQuestionFor1e2.py CentralQuestionFor1e2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Separate the comparison sign and pi as OldTex arguments to keep the two indexed terms.
# ==============================================================================

from manim_imports_ext import *

class AddTwoThetaManyTimes(Scene):
    def construct(self):
        expression = OldTex(
            "2\\theta", "+",
            "2\\theta", "+",
            "2\\theta", "+",
            "\\cdots", "+",
            "2\\theta",
            "<", "2\\pi",
        )
        expression.to_corner(UL)

        brace = Brace(expression[:-2], DOWN)
        question = brace.get_text("Max number of times?")
        question.set_color(YELLOW)

        central_question_group = self.get_central_question()
        simplified, lil_brace, new_question = central_question_group
        central_question_group.next_to(question, DOWN, LARGE_BUFF)
        new_question.align_to(question, LEFT)

        for n in range(5):
            self.add(expression[:2 * n + 1])
            self.wait(0.25)
        self.play(
            FadeIn(expression[-2:], LEFT),
            GrowFromCenter(brace),
            FadeIn(question, UP)
        )
        self.wait(3)
        self.play(
            TransformFromCopy(expression[:-2], simplified[:3]),
            TransformFromCopy(expression[-2:], simplified[3:]),
            TransformFromCopy(brace, lil_brace),
        )
        self.play(Write(new_question))
        self.wait()

        self.central_question_group = central_question_group
        self.show_example()

    def get_central_question(self, brace_vect=DOWN):
        expression = OldTex(
            "N", "\\cdot", "\\theta", "<", "\\pi"
        )
        N = expression[0]
        N.set_color(BLUE)
        brace = Brace(N, brace_vect, buff=SMALL_BUFF)
        question = brace.get_text(
            "Maximal integer?",
        )
        question.set_color(YELLOW)
        result = VGroup(expression, brace, question)
        result.to_corner(UL)
        return result

    def show_example(self):
        equation = self.get_changable_equation(0.01, n_decimal_places=2)
        expression, brace, question = self.central_question_group
        N_mob, dot_theta_eq, rhs, comp_pi = equation

        equation.next_to(expression, DOWN, 2, aligned_edge=LEFT)

        self.play(
            TransformFromCopy(expression[0], N_mob),
            TransformFromCopy(expression[1:4], dot_theta_eq),
            TransformFromCopy(expression[4], rhs),
            TransformFromCopy(expression[4], comp_pi),
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(N_mob, 314, run_time=5)
        )
        self.wait()
        self.play(ChangeDecimalToValue(N_mob, 315))
        self.wait()
        self.play(ChangeDecimalToValue(N_mob, 314))
        self.wait()
        self.play(ShowCreationThenFadeAround(N_mob))

    #
    def get_changable_equation(self, value, tex_string=None, n_decimal_places=10):
        int_mob = Integer(1)
        int_mob.set_color(BLUE)
        formatter = "({:0." + str(n_decimal_places) + "f})"
        tex_string = tex_string or formatter.format(value)
        tex_mob = OldTex("\\cdot", tex_string, "=")
        rhs = DecimalNumber(value, num_decimal_places=n_decimal_places)

        def align_number(mob):
            y0 = mob[0].get_center()[1]
            y1 = tex_mob[1][1:-1].get_center()[1]
            mob.shift((y1 - y0) * UP)

        int_mob.add_updater(
            lambda m: m.next_to(tex_mob, LEFT, SMALL_BUFF)
        )
        int_mob.add_updater(align_number)
        rhs.add_updater(
            lambda m: m.set_value(value * int_mob.get_value())
        )
        rhs.add_updater(
            lambda m: m.next_to(tex_mob, RIGHT, SMALL_BUFF)
        )
        rhs.add_updater(align_number)

        # CHANGE: keep the comparison sign and pi as separate OldTex parts.
        def get_comp_pi():
            if rhs.get_value() < np.pi:
                result = OldTex("<", "\\pi")
                result.set_color(GREEN)
            elif rhs.get_value() > np.pi:
                result = OldTex(">", "\\pi")
                result.set_color(RED)
            else:
                result = OldTex("=", "\\pi")
            result.next_to(rhs, RIGHT, 2 * SMALL_BUFF)
            result[1].scale(1.5, about_edge=LEFT)
            return result

        comp_pi = always_redraw(get_comp_pi)

        return VGroup(int_mob, tex_mob, rhs, comp_pi)


class CentralQuestionFor1e2(AddTwoThetaManyTimes):
    CONFIG = {
        "exp": 2,
    }

    def construct(self):
        exp = self.exp
        question = self.get_central_question(UP)
        pi_value = OldTex(" = {:0.10f}\\dots".format(PI))
        pi_value.next_to(question[0][-1], RIGHT, SMALL_BUFF)
        pi_value.shift(0.3 * SMALL_BUFF * UP)
        question.add(pi_value)

        max_count = int(PI * 10**exp)

        question.center().to_edge(UP)
        self.add(question)

        b10_equation = self.get_changable_equation(
            10**(-exp), n_decimal_places=exp
        )
        b10_equation.next_to(question, DOWN, buff=1.5)
        arctan_equation = self.get_changable_equation(
            np.arctan(10**(-exp)), n_decimal_places=10,
        )
        arctan_equation.next_to(b10_equation, DOWN, MED_LARGE_BUFF)
        eq_centers = [
            eq[1][2].get_center()
            for eq in [b10_equation, arctan_equation]
        ]
        arctan_equation.shift((eq_centers[1][0] - eq_centers[1][0]) * RIGHT)

        # b10_brace = Brace(b10_equation[1][1][1:-1], UP)
        arctan_brace = Brace(arctan_equation[1][1][1:-1], DOWN)
        # b10_tex = b10_brace.get_tex("1 / 10")
        arctan_tex = arctan_brace.get_tex(
            "\\theta = \\arctan(1 / {:,})".format(10**exp)
        )

        int_mobs = b10_equation[0], arctan_equation[0]

        self.add(*b10_equation, *arctan_equation)
        # self.add(b10_brace, b10_tex)
        self.add(arctan_brace, arctan_tex)

        self.wait()
        self.play(*[
            ChangeDecimalToValue(int_mob, max_count, run_time=8)
            for int_mob in int_mobs
        ])
        self.wait()
        self.play(*[
            ChangeDecimalToValue(int_mob, max_count + 1, run_time=1)
            for int_mob in int_mobs
        ])
        self.wait()
        self.play(*[
            ChangeDecimalToValue(int_mob, max_count, run_time=1)
            for int_mob in int_mobs
        ])
        self.play(ShowCreationThenFadeAround(int_mobs[1]))
        self.wait()
