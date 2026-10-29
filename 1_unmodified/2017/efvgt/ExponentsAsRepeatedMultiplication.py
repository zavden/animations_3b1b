# ==============================================================================
# Scene:      ExponentsAsRepeatedMultiplication
# Source:     videos/_2017/efvgt.py (lines 2332-2517)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExponentsAsRepeatedMultiplication.py ExponentsAsRepeatedMultiplication -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

MULTIPLIER_COLOR = YELLOW


class ExponentsAsRepeatedMultiplication(TeacherStudentsScene):
    def construct(self):
        self.show_repeated_multiplication()
        self.show_non_counting_exponents()

    def show_repeated_multiplication(self):
        three_twos = OldTex("2 \\cdot 2 \\cdot 2")
        five_twos = OldTex("2 \\cdot "*4 + "2")
        exponents = []
        teacher_corner = self.get_teacher().get_corner(UP+LEFT)
        for twos in three_twos, five_twos:
            twos.next_to(teacher_corner, UP)
            twos.generate_target()
            d = sum(np.array(list(twos.get_tex())) == "2")
            exponents.append(d)
            twos.brace = Brace(twos, UP)
            twos.exp = twos.brace.get_text("$2^%d$"%d)
            twos.generate_target()
            twos.brace_anim = MaintainPositionRelativeTo(
                VGroup(twos.brace, twos.exp), twos
            )

        self.play(
            GrowFromCenter(three_twos.brace),
            Write(three_twos.exp),
            self.get_teacher().change_mode, "raise_right_hand",
        )
        for mob in three_twos:
            self.play(Write(mob, run_time = 1))
        self.play_student_changes(*["pondering"]*3)
        self.wait(2)
        self.play(
            FadeIn(five_twos.brace),
            FadeIn(five_twos.exp),
            three_twos.center,
            three_twos.to_edge, UP, 2*LARGE_BUFF,
            three_twos.brace_anim,
        )
        self.play(FadeIn(
            five_twos, 
            run_time = 3,
            lag_ratio = 0.5
        ))
        self.wait(2)

        cdot = OldTex("\\cdot")
        lhs = OldTex("2^{%d + %d} = "%tuple(exponents))
        rule = VGroup(
            lhs, three_twos.target, cdot, five_twos.target
        )
        rule.arrange()
        lhs.next_to(three_twos.target, LEFT, aligned_edge = DOWN)
        rule.next_to(self.get_pi_creatures(), UP)

        self.play(
            MoveToTarget(three_twos),
            three_twos.brace_anim,
            MoveToTarget(five_twos),
            five_twos.brace_anim,
            Write(cdot),
            self.get_teacher().change_mode, "happy",
        )
        self.wait()
        self.play(Write(lhs))
        self.wait()
        self.play_student_changes(*["happy"]*3)
        self.wait()

        general_equation = OldTex("2^{x+y}=", "2^x", "2^y")
        general_equation.to_edge(UP, buff = MED_LARGE_BUFF)
        general_equation[0].set_color(GREEN_B)
        VGroup(*general_equation[1:]).set_color(MULTIPLIER_COLOR)
        self.play(*[
            ReplacementTransform(
                mob.copy(), term, run_time = 2
            )
            for term, mob in zip(general_equation, [
                lhs, three_twos.exp, five_twos.exp
            ])
        ])
        self.wait(2)

        self.exponential_rule = general_equation
        self.expanded_exponential_rule = VGroup(
            lhs, three_twos, three_twos.brace, three_twos.exp,
            cdot, five_twos, five_twos.brace, five_twos.exp,
        )

    def show_non_counting_exponents(self):
        self.play(
            self.expanded_exponential_rule.scale, 0.5,
            self.expanded_exponential_rule.to_corner, UP+LEFT
        )
        half_power, neg_power, imag_power = alt_powers = VGroup(
            OldTex("2^{1/2}"),
            OldTex("2^{-1}"),
            OldTex("2^{i}"),
        )
        alt_powers.arrange(RIGHT, buff = LARGE_BUFF)
        alt_powers.next_to(self.get_students(), UP, buff = LARGE_BUFF)

        self.play(
            Write(half_power, run_time = 2),
            *[
                ApplyMethod(pi.change_mode, "pondering")
                for pi in self.get_pi_creatures()
            ]
        )
        for mob in alt_powers[1:]:
            self.play(Write(mob, run_time = 1))
            self.wait()
        self.wait()
        self.play(*it.chain(*[
            [pi.change_mode, "confused", pi.look_at, half_power]
            for pi in self.get_students()
        ]))
        for power in alt_powers[:2]:
            self.play(Indicate(power))
            self.wait()
        self.wait()

        self.teacher_says("Extend the \\\\ definition")
        self.play_student_changes("pondering", "confused", "erm")
        self.wait()

        half_expression = OldTex(
            "\\big(", "2^{1/2}", "\\big)", 
            "\\big(2^{1/2}\\big) = 2^{1}"
        )
        neg_one_expression = OldTex(
            "\\big(", "2^{-1}", "\\big)", 
            "\\big( 2^{1} \\big) = 2^{0}"
        )
        expressions = VGroup(half_expression, neg_one_expression)
        expressions.arrange(
            DOWN, aligned_edge = LEFT, buff = MED_LARGE_BUFF
        )
        expressions.next_to(self.get_students(), UP, buff = LARGE_BUFF)
        expressions.to_edge(LEFT)

        self.play(
            Transform(half_power, half_expression[1]),
            Write(half_expression),            
            RemovePiCreatureBubble(self.get_teacher()),            
        )
        self.wait()
        self.play(
            Transform(neg_power, neg_one_expression[1]),
            Write(neg_one_expression)
        )
        self.wait(2)
        self.play(
            self.exponential_rule.next_to,
            self.get_teacher().get_corner(UP+LEFT), UP, MED_LARGE_BUFF,
            self.get_teacher().change_mode, "raise_right_hand",
        )
        self.wait(2)
        self.play(
            imag_power.move_to, UP,
            imag_power.scale, 1.5,
            imag_power.set_color, BLUE,
            self.exponential_rule.to_edge, RIGHT,
            self.get_teacher().change_mode, "speaking"
        )
        self.play(*it.chain(*[
            [pi.change_mode, "pondering", pi.look_at, imag_power]
            for pi in self.get_students()
        ]))
        self.wait()

        group_theory_words = OldTexText("Group theory?")
        group_theory_words.next_to(
            self.exponential_rule, UP, buff = LARGE_BUFF
        )
        arrow = Arrow(
            group_theory_words,
            self.exponential_rule,
            color = WHITE,
            buff = SMALL_BUFF
        )
        group_theory_words.shift_onto_screen()
        self.play(
            Write(group_theory_words), 
            ShowCreation(arrow)
        )
        self.wait(2)
