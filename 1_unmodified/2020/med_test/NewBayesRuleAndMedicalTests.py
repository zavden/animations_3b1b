# ==============================================================================
# Scene:      NewBayesRuleAndMedicalTests
# Source:     videos/_2020/med_test.py (lines 414-813)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewBayesRuleAndMedicalTests.py NewBayesRuleAndMedicalTests -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PersonIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("person", **kwargs)


class Population(VGroup):
    def __init__(self, count, **kwargs):
        super().__init__(**kwargs)
        icon = PersonIcon()
        self.add(*(icon.copy() for x in range(count)))
        self.arrange_in_grid()


def get_covid_clipboard(disease_name="SARS\\\\CoV-2", sign="+", report="Detected", color=GREEN):
    clipboard = SVGMobject("clipboard")
    clipboard.set_stroke(width=0)
    clipboard.set_fill(interpolate_color(GREY_BROWN, WHITE, 0.5), 1)
    clipboard.set_width(2.5)

    result = OldTexText(
        sign + "\\\\",
        disease_name + "\\\\",
        report,
    )
    result[0].scale(1.5, about_point=result[1].get_top())
    result[0].set_fill(color)
    result[0].set_stroke(color, 2)
    result[2].set_width(1.2 * result[1].get_width())
    result[-1].set_fill(color)
    result.set_width(clipboard.get_width() * 0.7)
    result.move_to(clipboard)
    result.shift(0.2 * DOWN)
    clipboard.add(result)
    return clipboard


class NewBayesRuleAndMedicalTests(Scene):
    def construct(self):
        # Mention paradox
        paradox_name = OldTexText("Medical Test Paradox", font_size=60)
        paradox_name.to_corner(UL)
        paradox_name.shift(MED_SMALL_BUFF * DOWN)
        paradox_line = Underline(paradox_name)
        paradox_line.set_stroke(GREY_B, 2)

        clipboard = get_covid_clipboard("Virus", color=BLUE)
        clipboard.set_height(3)
        clipboard.next_to(paradox_line, DOWN, LARGE_BUFF)
        clipboard[2][0].shift(SMALL_BUFF * DOWN)
        clipboard[2][0].set_stroke(BLUE, 4)
        clipboard[2].set_opacity(0)

        self.play(
            FadeIn(paradox_name, lag_ratio=0.1),
            ShowCreation(paradox_line),
            FadeIn(clipboard, DOWN),
        )
        clipboard[2].set_opacity(1)
        self.play(
            Write(clipboard[2], run_time=1)
        )
        self.wait()

        # Show Bayes rule
        bayes_title = OldTexText("Bayes' rule", font_size=60)
        bayes_title.move_to(paradox_name, UL)
        bayes_title.to_edge(RIGHT, buff=1.5)
        bayes_underline = Underline(bayes_title)
        bayes_underline.scale(1.5)
        bayes_underline.set_stroke(GREY_B, 2)
        bayes_underline.match_y(paradox_line)

        formula = OldTex(
            "P(H|E) = {P(H)P(E|H) \\over P(E)}",
            tex_to_color_map={
                "H": YELLOW,
                "E": BLUE,
            },
        )
        formula.next_to(bayes_underline, DOWN, buff=LARGE_BUFF)

        self.play(
            Write(bayes_title, run_time=1),
            GrowFromCenter(bayes_underline),
            FadeIn(formula, shift=0.5 * DOWN, scale=1.2)
        )
        self.wait()

        # Show high accuracy
        accuracy_words = OldTexText("High accuracy")
        accuracy_words.next_to(paradox_line, DOWN, MED_LARGE_BUFF)
        accuracy_words.set_color(GREEN)

        population = Population(100)
        population.arrange_in_grid(buff=LARGE_BUFF)
        population.set_height(5)
        population.next_to(accuracy_words, DOWN)

        marks = VGroup()
        for icon in population:
            icon.generate_target()
            if random.random() < 0.025:
                mark = Exmark()
                icon.target.set_opacity(0.5)
            else:
                mark = Checkmark()
            mark.set_height(icon.get_height() / 2)
            mark.move_to(icon.get_corner(UL))
            marks.add(mark)

        accuracy_group = VGroup(accuracy_words, population, marks)

        self.play(
            FadeIn(accuracy_words),
            FadeIn(population, lag_ratio=0.01),
            clipboard.scale, 0.5,
            clipboard.to_corner, DR,
        )
        self.play(
            ShowIncreasingSubsets(marks, run_time=2),
            LaggedStartMap(MoveToTarget, population, run_time=2),
        )
        self.wait()

        # Show test result
        randy = Randolph(height=2)
        randy.next_to(population, RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
        clipboard.generate_target()
        clipboard.target.set_height(2)
        clipboard.target.next_to(randy.get_corner(UR), RIGHT)

        self.play(
            VFadeIn(randy),
            randy.change, "guilty", clipboard.target,
            MoveToTarget(clipboard),
            formula.match_width, bayes_underline,
            formula.next_to, bayes_underline, DOWN, MED_SMALL_BUFF,
        )
        self.play(randy.change, "horrified", clipboard)
        self.play(Blink(randy))
        self.wait()

        # Show low predictive value
        prob_expression = OldTex(
            "P(\\text{Sick} \\text{ given } +) = ",
            tex_to_color_map={
                "+": BLUE,
                "\\text{Sick}": YELLOW,
            }
        )
        prob = DecimalNumber(0.9, font_size=60)
        prob.next_to(prob_expression, RIGHT)
        prob.set_color(WHITE)
        prob.set_opacity(0)
        prob_expression.add(prob)
        p_line = Underline(prob)
        p_line.shift(0.1 * DOWN)
        p_line.scale(1.5)
        p_line.set_stroke(WHITE, 2)
        prob_expression.add(p_line)
        prob_expression.next_to(VGroup(randy, clipboard), UP, aligned_edge=LEFT)

        self.play(
            FadeIn(prob_expression),
            randy.change, "pondering", prob_expression
        )
        self.play(
            ChangeDecimalToValue(prob, 0.09),
            UpdateFromAlphaFunc(prob, lambda m, a: m.set_opacity(a)),
            run_time=2
        )
        self.play(Blink(randy))
        self.play(
            randy.change, "confused", prob,
            ChangeDecimalToValue(prob, 0.01),
        )
        self.play(Blink(randy))
        self.wait()

        predictive_group = VGroup(
            randy, clipboard,
            prob_expression, prob,
        )

        # Accurate does not imply predictive
        implication = OldTexText(
            "Accurate ", "$\\Rightarrow$", " Predictive",
        )
        implication.set_color_by_tex("Accurate", GREEN)
        implication.set_color_by_tex("Predictive", YELLOW)
        implication.match_width(paradox_line)
        implication.next_to(paradox_line, DOWN)

        strike = Line(DL, UR).replace(implication[1], stretch=True)
        strike.set_stroke(RED, 4)

        self.play(
            FadeIn(implication, scale=1.1),
            accuracy_group.scale, 0.8, {"about_edge": DOWN},
            randy.change, 'pondering', implication,
        )
        self.play(ShowCreation(strike))
        self.wait()
        implication.add(strike)

        paradox_group = VGroup(paradox_name, paradox_line, implication)

        # Get rid of medical test stuff
        p_rect = SurroundingRectangle(paradox_group, buff=MED_SMALL_BUFF)
        p_rect.set_stroke(WHITE, 2)
        p_rect.set_fill(GREY_E, 1)
        self.add(p_rect, paradox_group),
        self.play(
            FadeOut(accuracy_group, DL),
            FadeOut(predictive_group, 2 * DL),
            DrawBorderThenFill(p_rect)
        )
        paradox_group.add_to_back(p_rect)
        self.wait()

        # Alternate framing
        odds_formula = OldTex(
            "O(H|E) = O(H){P(E|H) \\over P(E|\\neg H)}",
            tex_to_color_map={
                "H": YELLOW,
                "E": BLUE,
                "\\neg": RED,
            }
        )
        odds_formula.match_height(formula)
        odds_formula.next_to(formula, DOWN, LARGE_BUFF)
        odds_formula.shift_onto_screen()

        bf_rect = SurroundingRectangle(odds_formula[7:], buff=0.025)
        bf_rect.set_stroke(TEAL, 2)
        bf_name = OldTexText("Bayes\\\\factor", font_size=36)
        bf_name.match_color(bf_rect)
        bf_name.next_to(bf_rect, DOWN, buff=0.2)
        odds_formula.add(bf_rect, bf_name)

        arrow = Vector(1.5 * RIGHT)
        arrow.next_to(formula, LEFT)

        self.play(
            paradox_group.next_to, arrow, LEFT,
            GrowArrow(arrow),
        )
        self.wait()

        self.play(
            VGroup(paradox_group, arrow).next_to, odds_formula[0], LEFT,
            FadeIn(odds_formula, DOWN)
        )
        self.wait()

        # Reflections on this formula
        morty = Mortimer(height=2.2)
        morty.to_corner(DR)
        morty.shift(2 * LEFT)
        randy = Randolph(height=2)
        randy.next_to(morty, LEFT, LARGE_BUFF, aligned_edge=DOWN)

        bubble = ThoughtBubble()
        bubble.pin_to(morty)

        self.play(
            LaggedStart(*(
                ShowCreationThenFadeOut(SurroundingRectangle(mob, color=BLUE))
                for mob in (formula, odds_formula)
            ), lag_ratio=0.4, run_time=3),
            VFadeIn(randy),
            randy.change, "confused", formula,
        )
        self.play(Blink(randy))
        self.wait()

        self.add(bubble, odds_formula)
        odds_formula.save_state()
        self.play(
            VFadeIn(morty),
            morty.change, "maybe", bubble[-1],
            randy.look_at, bubble,
            FadeIn(bubble, lag_ratio=0.5),
            odds_formula.move_to, bubble.get_bubble_center(),
            odds_formula.shift, 0.2 * LEFT + 0.1 * DOWN,
            FadeOut(arrow, scale=0.5),
            paradox_group.scale, 0.5,
            paradox_group.to_corner, DL,
        )
        self.play(Blink(morty))
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change, "pondering")
        self.play(Blink(randy))
        self.wait()

        paradox_group.generate_target()
        paradox_group.target.scale(1.5)
        paradox_group.target.next_to(randy.get_corner(UL), UP)
        paradox_group.target.shift(LEFT)
        self.play(
            FadeOut(bubble, lag_ratio=0.4),
            Restore(odds_formula),
            morty.change, 'tease', paradox_group.target,
            randy.change, 'raise_left_hand', paradox_group.target,
            MoveToTarget(paradox_group),
        )
        self.play(Blink(morty))
        self.wait()
        return

        # Unprocessed
        # Show rule
        formula = OldTex(
            "P(H|E) = {P(H)P(E|H) \\over P(E)}",
            tex_to_color_map={
                "H": YELLOW,
                "E": BLUE,
            },
            font_size=60
        )

        h_part = formula.get_part_by_tex("H")
        hyp_word = OldTexText("Hypothesis", color=YELLOW)
        hyp_word.next_to(h_part, UP, LARGE_BUFF)
        hyp_arrow = Arrow(hyp_word.get_bottom(), h_part.get_top(), buff=0.1)

        e_part = formula.get_part_by_tex("E")
        ev_word = OldTexText("Evidence", color=BLUE)
        ev_word.next_to(e_part, DOWN, LARGE_BUFF)
        ev_arrow = Arrow(ev_word.get_top(), e_part.get_bottom(), buff=0.1)

        self.play(
            ShowCreation(h_line),
            FadeIn(formula, scale=1.1),
        )
        self.play(
            LaggedStart(
                FadeIn(hyp_word, shift=0.25 * UP, scale=1.1),
                FadeIn(ev_word, shift=0.25 * DOWN, scale=1.1),
            ),
            LaggedStart(
                GrowArrow(hyp_arrow),
                GrowArrow(ev_arrow),
            ),
        )
        self.wait()
        formula_annoations = VGroup(hyp_word, hyp_arrow, ev_word, ev_arrow)

        # Randys
        pis = VGroup(Randolph(), Randolph())
        pis.set_height(2)
        pis[1].flip()
        pis[1].set_color(TEAL_E)
        pis.arrange(RIGHT, buff=5)
        pis.to_corner(DL)

        self.play(
            VFadeIn(pis[0]),
            pis[0].change, "hooray", formula
        )
        self.play(Blink(pis[0]))
        self.play(
            VFadeIn(pis[1]),
            pis[1].change, "maybe", formula
        )
        self.play(Blink(pis[1]))
        self.wait()

        # Sweep aside
        title.add(h_line)
        formula.generate_target()
        formula.target.scale(0.6)
        formula.target.to_corner(DR)

        self.play(
            VFadeOut(formula_annoations),
            MaintainPositionRelativeTo(formula_annoations, formula),
            MoveToTarget(formula),
            title.scale, 0.7,
            title.next_to, formula.target, UP,
            FadeOut(pis, DOWN),
        )

        # Question the formulas
        self.play(FadeIn(morty))
        self.play(morty.change, "hesitant", formula)
        self.play(Blink(morty))
        self.wait()
        formulas = VGroup(formula, odds_formula)
        self.play(
            LaggedStart(
                *(
                    ShowCreationThenFadeOut(Underline(mob, color=GREY_BROWN))
                    for mob in formulas
                ),
                lag_ratio=0.3
            ),
            morty.change, "raise_right_hand", formula,
        )
        self.play(Blink(morty))
        self.wait()

        mover = VGroup(paradox_group, title, formula, odds_formula, arrow)
        bubbles = VGroup(*(ThoughtBubble(height=1, width=1) for x in range(2)))
        bubbles.set_fill(GREY_E, 1)
        for bubble, form in zip(bubbles, formulas):
            bubble.move_to(form, RIGHT)

        self.play(
            morty.change, "raise_left_hand", bubble,
            mover.to_edge, LEFT,
            LaggedStartMap(DrawBorderThenFill, bubbles, lag_ratio=0.7, run_time=2),
        )
        self.play(Blink(morty))
        self.wait()

        self.play(
            Rotate(arrow, PI),
            morty.change, "pondering", paradox_group,
        )
        arrow2 = Arrow(formula.get_left(), paradox_group.get_corner(UR))
        self.play(GrowArrow(arrow2))
        self.play(Blink(morty))
        self.wait(2)

        self.play(
            LaggedStart(*(
                FadeOut(mob, RIGHT)
                for mob in [arrow2, arrow, title, formula, odds_formula, *bubbles]
            )),
            morty.change, "raise_right_hand",
            paradox_group.next_to, morty.get_corner(UR), UP,
            paradox_group.shift_onto_screen,
        )
        self.wait()
