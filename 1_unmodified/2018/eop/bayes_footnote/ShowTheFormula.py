# ==============================================================================
# Scene:      ShowTheFormula
# Source:     videos/_2018/eop/bayes_footnote.py (lines 884-990)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowTheFormula.py ShowTheFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class ShowTheFormula(TeacherStudentsScene):
    CONFIG = {
        "seconds_to_blink" : 3,
    }
    def construct(self):
        scale_factor = 0.7
        sick = "\\text{sick}"
        positive = "\\text{positive}"
        formula = OldTex(
            "P(", sick, "\\,|\\,", positive, ")", "=",
            "{\\quad P(", sick, "\\text{ and }", positive, ") \\quad",
            "\\over",
            "P(", positive, ")}", "=",
            "{1/1{,}000", "\\over", "1/1{,}000", "+", "(999/1{,}000)(0.01)}"
        )
        formula.scale(scale_factor)
        formula.next_to(self.pi_creatures, UP, LARGE_BUFF)
        formula.shift_onto_screen(buff = MED_LARGE_BUFF)
        equals_group = formula.get_parts_by_tex("=")
        equals_indices = [
            formula.index_of_part(equals)
            for equals in equals_group
        ]

        lhs = VGroup(*formula[:equals_indices[0]])
        initial_formula = VGroup(*formula[:equals_indices[1]])
        initial_formula.save_state()
        initial_formula.shift(3*RIGHT)

        over = formula.get_part_by_tex("\\over")
        num_start_index = equals_indices[0] + 1
        num_end_index = formula.index_of_part(over)
        numerator = VGroup(
            *formula[num_start_index:num_end_index]
        )
        numerator_rect = SurroundingRectangle(numerator)

        alt_numerator = OldTex(
            "P(", sick, ")", "P(", positive, "\\,|\\,", sick, ")"
        )
        alt_numerator.scale(scale_factor)
        alt_numerator.move_to(numerator)

        number_fraction = VGroup(*formula[equals_indices[-1]:])

        rhs = OldTex("\\approx 0.09")
        rhs.scale(scale_factor)
        rhs.move_to(equals_group[-1], LEFT)
        rhs.set_color(YELLOW)

        for mob in formula, alt_numerator:
            mob.set_color_by_tex(sick, SICKLY_GREEN)
            mob.set_color_by_tex(positive, YELLOW)


        #Ask question
        self.student_says("What does the \\\\ formula look like here?")
        self.play(self.teacher.change, "happy")
        self.wait()
        self.play(
            Write(lhs),
            RemovePiCreatureBubble(
                self.students[1], target_mode = "pondering",
            ),
            self.teacher.change, "raise_right_hand",
            self.students[0].change, "pondering",
            self.students[2].change, "pondering",
        )
        self.wait()

        #Show initial formula
        lhs_copy = lhs.copy()
        self.play(
            LaggedStartMap(
                FadeIn, initial_formula, 
                lag_ratio = 0.7
            ),
            Animation(lhs_copy, remover = True),
        )
        self.wait(2)
        self.play(ShowCreation(numerator_rect))
        self.play(FadeOut(numerator_rect))
        self.wait()
        self.play(Transform(numerator, alt_numerator))
        initial_formula.add(*numerator)
        formula.add(*numerator)
        self.wait(3)

        #Show number_fraction
        self.play(
            initial_formula.move_to, initial_formula.saved_state,
            FadeIn(VGroup(*number_fraction[:3]))
        )
        self.wait(2)
        self.play(LaggedStartMap(
            FadeIn, VGroup(*number_fraction[3:]),
            run_time = 3,
            lag_ratio = 0.7
        ))
        self.wait(2)

        #Show rhs
        self.play(formula.shift, UP)
        self.play(Write(rhs))
        self.play_student_changes(*["happy"]*3)
        self.look_at(rhs)
        self.wait(2)
