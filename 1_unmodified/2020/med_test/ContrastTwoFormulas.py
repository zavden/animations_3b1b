# ==============================================================================
# Scene:      ContrastTwoFormulas
# Source:     videos/_2020/med_test.py (lines 4953-5254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContrastTwoFormulas.py ContrastTwoFormulas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


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


class ContrastTwoFormulas(Scene):
    def construct(self):
        # Talk through odds formula
        t2c = {
            "\\text{D}": YELLOW,
            "\\text{$\\neg$D}": GREY_B,
            "{+}": GREEN,
            "(": WHITE,
            ")": WHITE,
            "\\over": WHITE,
            "O": WHITE,
            "=": WHITE,
            "\\text{Prior}": YELLOW,
            "\\text{Sensitivity}": GREEN,
            "\\text{Sens.}": GREEN,
            "\\text{FPR}": GREEN_D,
        }
        kw = {"tex_to_color_map": t2c}

        odds_formula = OldTex(
            "O(\\text{D} | {+}) ="
            "O(\\text{D})"
            "{P({+} | \\text{D}) \\over P({+} | \\text{$\\neg$D})}",
            **kw
        )
        odds_formula.scale(1.25)
        bf_part = odds_formula[11:]
        post_part = odds_formula[:6]
        prior_part = odds_formula[7:11]

        post_words = OldTexText(
            "Odds of having the disease\\\\ \\emph{given} a positive test result",
            tex_to_color_map={
                "disease": YELLOW,
                "positive": GREEN,
            }
        )
        post_words.next_to(post_part, UP, buff=1.5)
        post_words.shift(LEFT)
        post_arrow = Arrow(post_words.get_bottom(), post_part[:2].get_top(), buff=0.2)
        prior_words = OldTexText("Prior odds")
        prior_words.next_to(prior_part, DOWN, buff=1.5)
        prior_words.shift(LEFT)
        prior_arrow = Arrow(prior_words.get_top(), prior_part[:2].get_bottom(), buff=0.2)

        bf_rect = SurroundingRectangle(bf_part, buff=0.1)
        bf_rect.set_stroke(TEAL, 2)
        bf_words = OldTexText("Bayes factor")
        bf_words.next_to(bf_rect, UP)
        bf_words.match_color(bf_rect)

        self.play(Write(odds_formula))
        self.wait()
        self.play(
            FadeIn(post_words, lag_ratio=0.1),
            GrowArrow(post_arrow),
        )
        self.wait()
        self.play(
            FadeIn(prior_words),
            GrowArrow(prior_arrow),
        )
        self.wait()
        VGroup(bf_rect, bf_words).shift(SMALL_BUFF * RIGHT)
        self.play(
            FadeIn(bf_words, 0.25 * UP),
            ShowCreation(bf_rect),
            bf_part.shift, SMALL_BUFF * RIGHT,
        )
        self.wait()

        # Sweep aside
        to_fade = VGroup(post_words, post_arrow, prior_words, prior_arrow)
        odds_formula.add(bf_rect, bf_words)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY_B, 2)

        titles = VGroup(
            OldTexText("Using probability"),
            OldTexText("Using odds"),
        )
        titles.scale(1.25)
        for title, u in zip(titles, [-1, 1]):
            title.set_x(u * FRAME_WIDTH / 4)
        titles.to_edge(UP)

        self.play(
            ShowCreation(v_line),
            FadeOut(to_fade, shift=UR, scale=0.5),
            odds_formula.scale, 0.7,
            odds_formula.next_to, titles[1], DOWN, LARGE_BUFF,
            FadeIn(titles[0], LEFT),
            FadeIn(titles[1], RIGHT),
        )
        self.wait()

        # Contrast with usual formula
        prob_formula = OldTex(
            """
            P(\\text{D} | {+}) =
            {P(\\text{D}) P({+} \\,|\\, \\text{D})
            \\over
            P(\\text{D}) P({+} \\,|\\, \\text{D})
            +
            P(\\text{$\\neg$D}) P({+} \\,|\\, \\text{$\\neg$D})}
            """,
            **kw
        )
        prob_rhs = prob_formula[7:]
        prob_formula.set_width(FRAME_WIDTH / 2 - 1)
        prob_formula.set_x(-FRAME_WIDTH / 4)
        prob_formula.match_y(bf_part)

        self.play(FadeIn(prob_formula, shift=0.25 * DOWN, scale=1.2))
        self.wait()

        # Use term-based formulas
        term_formula = OldTex(
            """
            {(\\text{Prior})(\\text{Sensitivity})
            \\over
            (\\text{Prior})(\\text{Sensitivity})
            +
            (1 - \\text{Prior})(\\text{FPR})
            """,
            **kw
        )
        term_formula.replace(prob_rhs, 0)
        bf_terms = OldTex(
            "\\text{Sensitivity} \\over \\text{FPR}",
            **kw
        )
        bf_terms.replace(bf_part, 0)

        self.play(
            FadeOut(prob_rhs, 0.5 * UP),
            FadeIn(term_formula, 0.5 * UP),
            FadeOut(bf_part, 0.5 * UP),
            FadeIn(bf_terms, 0.5 * UP),
        )
        self.wait()

        # Comment on prior/test separation
        kw2 = {
            "tex_to_color_map": {
                "Prior": YELLOW,
                "test accuracy": GREEN,
                "separate": GREY_A,
                "intermingled": GREY_A,
            }
        }
        pt_comments = VGroup(
            OldTexText("Prior and test accuracy\\\\are intermingled", **kw2),
            OldTexText("Prior and test accuracy\\\\are separate", **kw2),
        )
        for comment, formula in zip(pt_comments, [prob_formula, odds_formula]):
            comment.match_x(formula)
        pt_comments.set_y(-2)

        self.play(Write(pt_comments[1], run_time=1))
        self.play(
            VGroup(bf_terms, bf_rect, bf_words).shift, 0.25 * UR,
            prior_part.shift, 0.25 * UL,
            rate_func=there_and_back_with_pause,
            run_time=2,
        )
        self.wait()
        self.play(
            TransformFromCopy(pt_comments[1][:-1], pt_comments[0][:-1], path_arc=-20 * DEGREES),
            GrowFromPoint(pt_comments[0][-1], pt_comments[1][-1].get_left(), path_arc=20 * DEGREES),
            run_time=1,
        )
        words_to_move = VGroup(
            *term_formula.get_parts_by_tex("\\text{Prior}"),
            *term_formula.get_parts_by_tex("\\text{Sensitivity}"),
            *term_formula.get_parts_by_tex("\\text{FPR}"),
        )
        self.play(LaggedStart(*(
            ApplyMethod(
                part.shift, 0.25 * vect,
                rate_func=there_and_back_with_pause,
                run_time=2,
            )
            for part, vect in zip(words_to_move, [UP, DOWN, DOWN, UP, DOWN, DOWN])
        ), lag_ratio=0.05))
        self.wait()

        # Comment on multiple updates
        kw["tex_to_color_map"].update({
            "{E_1}": GREEN,
            "{E_2}": BLUE,
        })
        mult_formula = OldTex(
            "O(\\text{D} | {E_1}, {E_2}) =",
            "O(\\text{D})\\,\\,",
            "{P({E_1} | \\text{D}) \\over P({E_1} | \\text{$\\neg$D})}\\,\\,",
            "{P({E_2} | \\text{D}, {E_1}) \\over P({E_2} | \\text{$\\neg$D}, {E_1})}",
            **kw
        )
        mult_formula.set_width(FRAME_WIDTH / 2 - 1)
        mult_formula.next_to(odds_formula, DOWN, buff=1.5)

        new_bf_parts = VGroup(mult_formula[14:27], mult_formula[27:])
        new_bf_rects = VGroup(*(
            SurroundingRectangle(part, buff=0.05)
            for part in new_bf_parts
        ))
        new_bf_rects[0].set_stroke(GREEN, 2)
        new_bf_rects[1].set_stroke(BLUE, 2)
        new_bf_labels = VGroup()
        for n, rect in zip(it.count(1), new_bf_rects):
            words = OldTexText(f"Bayes\\\\Factor {n}", font_size=28)
            parens = OldTex(*"()")
            parens.set_height(1.2 * words.get_height(), stretch=True)
            parens[0].next_to(words, LEFT, buff=0)
            parens[1].next_to(words, RIGHT, buff=0)
            words.add(parens)
            words.match_color(rect)
            words.next_to(rect, UP, MED_SMALL_BUFF)
            new_bf_labels.add(words)
            words.save_state()

        new_bf_labels.match_y(new_bf_parts)
        for part in new_bf_parts:
            part.save_state()
            part.set_color(BLACK)

        clipboards = VGroup(*(
            get_covid_clipboard("Disease").set_height(1.5).next_to(rect, DOWN)
            for rect in new_bf_rects
        ))
        sick_randy = Randolph(height=1.5)
        sick_randy.move_to(clipboards[1])

        self.play(
            FadeOut(pt_comments),
            FadeIn(mult_formula, lag_ratio=0.1),
            FadeIn(new_bf_labels, lag_ratio=0.1),
            FadeIn(new_bf_rects, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, clipboards, shift=0.5 * DOWN, lag_ratio=0.3)
        )
        self.wait()
        self.play(
            FadeIn(sick_randy, 0.5 * DOWN),
            FadeOut(clipboards[1], 0.5 * DOWN),
        )
        self.play(
            sick_randy.change, "sick",
            sick_randy.set_color, SICKLY_GREEN,
        )
        self.play(Blink(sick_randy))
        self.wait()
        for i in (0, 1):
            new_bf_parts[i].restore()
            self.play(
                Restore(new_bf_labels[i]),
                FadeIn(new_bf_parts[i]),
                sick_randy.look_at, new_bf_labels[i],
            )
            self.wait()
        self.play(Blink(sick_randy))
        self.wait()

        to_fade = VGroup(mult_formula, new_bf_labels, new_bf_rects, clipboards[0], sick_randy)
        self.play(LaggedStartMap(FadeOut, to_fade, shift=DOWN))

        # Comment
        randy = Randolph(height=1.5)
        morty = Mortimer(height=1.5)
        pis = VGroup(randy, morty)
        pis.arrange(RIGHT, buff=2)
        pis.to_corner(DR)
        pis.to_edge(DOWN)

        self.play(FadeIn(pis))
        self.play(PiCreatureSays(
            randy, "How accurate is\\\\the test?",
            bubble_config={"height": 2, "width": 3},
            content_introduction_class=FadeIn,
            bubble_creation_class=FadeIn,
            target_mode="raise_left_hand",
            look_at=morty.eyes,
            run_time=1,
        ))
        content = OldTexText("Bayes factor 100", tex_to_color_map={"$+$": GREEN})
        self.play(PiCreatureSays(
            morty, content,
            target_mode="hooray",
            bubble_config={"height": 2, "width": 3},
            content_introduction_class=FadeIn,
            bubble_creation_class=FadeIn,
            look_at=randy.eyes,
            run_time=1
        ))
        for x in range(2):
            self.play(Blink(randy))
            self.play(Blink(morty))
            self.wait()
