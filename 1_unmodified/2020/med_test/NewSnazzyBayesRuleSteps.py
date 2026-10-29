# ==============================================================================
# Scene:      NewSnazzyBayesRuleSteps
# Source:     videos/_2020/med_test.py (lines 3781-4129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewSnazzyBayesRuleSteps.py NewSnazzyBayesRuleSteps -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WomanIcon(SVGMobject):
    CONFIG = {
        "fill_color": GREY_B,
        "stroke_width": 0,
    }

    def __init__(self, **kwargs):
        super().__init__("woman_icon", **kwargs)
        self.remove(self[0])


class NewSnazzyBayesRuleSteps(Scene):
    def construct(self):
        # Add title
        title = OldTexText(
            "Bayes' rule, the snazzy way",
            font_size=72
        )
        title.to_edge(UP)
        title.set_stroke(BLACK, 2, background=True)
        underline = Underline(title)
        underline.scale(1.2)
        underline.shift(0.2 * UP)
        underline.set_stroke(GREY, 3)
        self.add(underline, title)

        # Completely accurate
        accurate_words = OldTexText(
            *"Completely accurate\\\\ Not even approximating things".split(" "),
            font_size=72,
            arg_separator=" "
        )
        accurate_words.set_color(BLUE)
        for word in accurate_words:
            self.add(word)
            self.wait(0.05 * len(word))

        # Population
        population = VGroup(*(
            WomanIcon()
            for x in range(100)
        ))
        population.arrange_in_grid(h_buff=1, v_buff=0.5, fill_rows_first=False)
        population.set_height(5)
        population.to_corner(DR)
        population[0].set_color(YELLOW)

        # Step labels
        step_labels = VGroup(
            OldTexText("Step 1)"),
            OldTexText("Step 2)"),
            OldTexText("Step 3)"),
        )
        step_labels.arrange(DOWN, buff=1.5, aligned_edge=LEFT)
        step_labels.next_to(title, DOWN, MED_LARGE_BUFF)
        step_labels.to_edge(LEFT)

        step1, step2, step3 = steps = VGroup(
            OldTexText("Express the prior with odds"),
            OldTexText("Compute Bayes' factor"),
            OldTexText("Multiply"),
        )

        colors = [YELLOW, GREEN, BLUE]
        for step, label, color in zip(steps, step_labels, colors):
            step.set_color(color)
            step.next_to(label, RIGHT)

        self.play(
            LaggedStartMap(FadeIn, step_labels, shift=0.5 * RIGHT),
            LaggedStartMap(FadeIn, steps, shift=RIGHT),
            FadeOut(accurate_words),
        )
        self.wait()

        # Step 2 details
        tex_to_color_map = {
            "+": GREEN,
            "\\text{Cancer}": YELLOW,
            "\\text{No cancer}": GREY_B,
            "=": WHITE,
            "\\over": WHITE,
            "{90\\%": GREEN,
            "9\\%}": GREEN,
            "1\\%}": TEAL,
            "10": WHITE,
        }
        bf_computation = OldTex(
            """
            {
            P(+ \\, | \\, \\text{Cancer}) \\over
            P(+ \\, | \\, \\text{No cancer})
            } =
            {90\\% \\over 9\\%} = 10
            """,
            tex_to_color_map=tex_to_color_map
        )
        bf_computation[-1].scale(1.2)
        bf_computation.scale(0.6)
        bf_computation.next_to(step2, DOWN, aligned_edge=LEFT)
        bf_computation.save_state()
        bf_computation.scale(1.5)
        bf_computation.next_to(steps[1], RIGHT, LARGE_BUFF)

        lr_words = OldTexText("``Likelihood ratio''", font_size=30)
        lr_words.next_to(bf_computation[-1], RIGHT, MED_LARGE_BUFF, DOWN)
        lr_words.set_color(GREY_A)

        sens_part = bf_computation.get_part_by_tex("90\\%")
        sens_word = OldTexText("Sensitivity")
        sens_word.next_to(sens_part, UP, buff=1)
        sens_arrow = Arrow(sens_word.get_bottom(), sens_part.get_top(), buff=0.1)

        fpr_part = bf_computation.get_part_by_tex("9\\%")
        fpr_word = OldTexText("FPR")
        fpr_word.next_to(fpr_part, DOWN, buff=1)
        fpr_arrow = Arrow(fpr_word.get_top(), fpr_part.get_bottom(), buff=0.1)

        self.play(FadeIn(bf_computation, lag_ratio=0.1))
        self.wait()
        self.play(
            Indicate(sens_part),
            FadeIn(sens_word),
            GrowArrow(sens_arrow)
        )
        self.wait()
        self.play(
            Indicate(fpr_part),
            FadeIn(fpr_word),
            GrowArrow(fpr_arrow),
        )
        self.wait(2)
        self.play(
            Restore(bf_computation),
            FadeOut(VGroup(sens_word, sens_arrow, fpr_word, fpr_arrow))
        )

        # Step 1 details
        step1_subtext = OldTexText("E.g.", " 1\\% ", " $\\rightarrow$ ", "1:99")
        step1_subtext.set_color(GREY_A)
        step1_subtext.scale(0.9)
        step1_subtext.next_to(step1, DOWN, aligned_edge=LEFT)

        self.play(
            FadeIn(step1_subtext[:2]),
            ShowIncreasingSubsets(population),
        )
        self.wait()
        self.play(
            TransformFromCopy(step1_subtext[1], step1_subtext[3]),
            Write(step1_subtext[2]),
        )
        self.play(ShowCreationThenFadeAround(step1_subtext[3]))
        self.wait()

        # Step 3
        multiplication = OldTex(
            "(", "1:99", ")", "\\times", "10",
            "=", "10:99",
            "\\rightarrow", "{10 \\over 109}",
            "\\approx", "{1 \\over 11}",
            font_size=36,
        )
        multiplication.next_to(step3, DOWN, aligned_edge=LEFT)

        odds_rect = SurroundingRectangle(step1_subtext[-1], color=YELLOW)
        bf_rect = SurroundingRectangle(bf_computation[-1], color=GREEN)
        self.play(
            ShowCreation(odds_rect),
            ShowCreation(bf_rect),
        )
        self.play(
            Write(VGroup(*(multiplication[i] for i in [0, 2, 3]))),
            TransformFromCopy(step1_subtext[-1], multiplication[1]),
            odds_rect.move_to, multiplication[1],
            odds_rect.set_opacity, 0,
            TransformFromCopy(bf_computation[-1], multiplication[4]),
            bf_rect.move_to, multiplication[4],
            bf_rect.set_opacity, 0,
        )
        self.remove(odds_rect, bf_rect)
        self.wait()

        self.play(
            FadeIn(multiplication.get_part_by_tex("=")),
            TransformFromCopy(
                multiplication.get_part_by_tex("1:99"),
                multiplication.get_part_by_tex("10:99"),
                path_arc=30 * DEGREES,
            ),
        )
        self.wait()
        self.play(
            FadeIn(multiplication.get_part_by_tex("\\rightarrow")),
            FadeIn(multiplication.get_part_by_tex("10 \\over 109")),
        )
        self.play(
            FadeIn(multiplication.get_part_by_tex("\\approx")),
            FadeIn(multiplication.get_part_by_tex("1 \\over 11")),
        )
        self.wait()

        # 10% prior example
        prior_odds = step1_subtext[1:]
        alt_prior_odds = OldTex(
            "10\\%", "\\rightarrow", "\\text{1:9}"
        )
        alt_prior_odds.match_height(prior_odds)
        alt_prior_odds.move_to(prior_odds, LEFT)
        alt_prior_odds.match_style(prior_odds)

        self.play(
            FadeOut(multiplication, shift=DOWN),
            FadeOut(prior_odds, shift=DOWN),
        )
        self.play(
            FadeIn(alt_prior_odds[0], scale=2),
        )
        self.play(
            population[:10].set_color, YELLOW,
            LaggedStartMap(
                ShowCreationThenFadeOut,
                VGroup(*(
                    SurroundingRectangle(person, buff=0.05)
                    for person in population[:10]
                ))
            )
        )
        self.wait()
        self.play(
            Write(alt_prior_odds[1]),
            FadeIn(alt_prior_odds[2], shift=0.5 * RIGHT)
        )
        self.wait()

        new_multiplication = OldTex(
            "(1:9)", "\\times", "10",
            "=", "10:9",
            "\\rightarrow", "{10 \\over 19}",
            "\\approx", "0.53",
            font_size=36,
        )
        new_multiplication.move_to(multiplication, LEFT)
        rects = VGroup(
            SurroundingRectangle(alt_prior_odds.get_part_by_tex("1:9"), color=YELLOW),
            SurroundingRectangle(bf_computation.get_part_by_tex("10"), color=GREEN),
            SurroundingRectangle(new_multiplication.get_part_by_tex("10:9"), color=RED),
        )

        self.play(
            FadeIn(rects[:2], lag_ratio=0.6, run_time=1.5)
        )
        self.play(
            ReplacementTransform(rects[0], rects[2]),
            ReplacementTransform(rects[1], rects[2]),
            FadeIn(new_multiplication[:5]),
        )
        self.wait()

        alt_rhs = OldTex("> 1:1", font_size=36)
        alt_rhs.next_to(new_multiplication[4], RIGHT)
        self.play(
            FadeOut(rects[2]),
            Write(alt_rhs)
        )
        self.wait()

        self.play(
            FadeOut(alt_rhs, shift=0.5 * UP),
            FadeIn(new_multiplication[5:7], shift=0.5 * UP),
        )
        self.wait()
        self.play(Write(new_multiplication[7:]))
        self.wait()

        # Return to original prior
        self.play(
            FadeOut(new_multiplication, shift=DOWN),
            FadeOut(alt_prior_odds, shift=DOWN),
            FadeIn(prior_odds, shift=DOWN)
        )
        self.play(population[1:].set_color, GREY_B)
        self.play(Indicate(population[0], color=RED))
        self.play(LaggedStartMap(
            Indicate, population[1:], color=GREY_A,
            lag_ratio=0.01
        ))
        self.wait()

        # Change test accuracy
        new_bf_computation = OldTex(
            """
            {
            P(+ \\, | \\, \\text{Cancer}) \\over
            P(+ \\, | \\, \\text{No cancer})
            } =
            {90\\% \\over 1\\%} = 90
            """,
            tex_to_color_map=tex_to_color_map
        )
        new_bf_computation.replace(bf_computation)
        new_bf_computation[-2:].scale(1.5, about_edge=LEFT)

        rects = VGroup(*(
            SurroundingRectangle(bf_computation[i:j], buff=0.05)
            for (i, j) in [(5, 8), (14, 15)]
        ))
        rects.set_color(RED)

        self.play(ShowCreation(rects))
        self.wait()
        self.play(
            FadeOut(bf_computation),
            FadeIn(new_bf_computation[:-2])
        )
        self.play(FadeOut(rects))
        self.wait()
        self.play(Write(new_bf_computation[-2:]))
        self.wait()

        # New posterior (largely copy-pasted)
        final_multiplication = OldTex(
            "(1:99)", "\\times", "90",
            "=", "90:99",
            "\\rightarrow", "{90 \\over 189}",
            "\\approx", "0.48",
            font_size=36,
        )
        final_multiplication.move_to(multiplication, LEFT)
        rects = VGroup(
            SurroundingRectangle(step1_subtext.get_part_by_tex("1:99"), color=YELLOW),
            SurroundingRectangle(new_bf_computation.get_parts_by_tex("90")[1], color=GREEN),
            SurroundingRectangle(final_multiplication.get_part_by_tex("90:99"), color=RED),
        )

        self.play(
            FadeIn(rects[:2], lag_ratio=0.6, run_time=1.5)
        )
        self.play(
            ReplacementTransform(rects[0], rects[2]),
            ReplacementTransform(rects[1], rects[2]),
            FadeIn(final_multiplication[:5]),
        )
        self.wait()

        alt_rhs = OldTex("< 1:1", font_size=36)
        alt_rhs.next_to(final_multiplication[4], RIGHT)
        self.play(
            FadeOut(rects[2]),
            Write(alt_rhs)
        )
        self.wait()

        self.play(
            FadeOut(alt_rhs, shift=0.5 * UP),
            FadeIn(final_multiplication[5:7], shift=0.5 * UP),
        )
        self.wait()
        self.play(Write(final_multiplication[7:]))
        self.wait()
