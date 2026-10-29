# ==============================================================================
# Scene:      BayesTheorem
# Source:     videos/_2020/med_test.py (lines 4658-4950)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BayesTheorem.py BayesTheorem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Brace.direction is now get_direction()
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


class BayesTheorem(Scene):
    def construct(self):
        # Add title
        title = OldTexText("The usual version of Bayes' rule", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title_line = Underline(title)
        title_line.set_stroke(GREY, 2)
        title_line.shift(SMALL_BUFF * UP)
        title.add(title_line)

        # Population
        prior = 1 / 12
        sensitivity = 0.8
        specificity = 0.9

        rects = VGroup(*[Square() for x in range(4)])
        rects.set_stroke(WHITE, 2)
        rects[:2].set_stroke(YELLOW)
        rects.set_fill(GREY_D, 1)
        rects.set_height(3)
        rects.set_width(3, stretch=True)
        rects.move_to(3.5 * LEFT + DOWN)

        rects[:2].stretch(prior, 0, about_edge=LEFT)
        rects[2:].stretch(1 - prior, 0, about_edge=RIGHT)
        rects[0].stretch(sensitivity, 1, about_edge=UP)
        rects[1].stretch(1 - sensitivity, 1, about_edge=DOWN)
        rects[2].stretch(1 - specificity, 1, about_edge=UP)
        rects[3].stretch(specificity, 1, about_edge=DOWN)

        rects[0].set_fill(GREEN_D)
        rects[1].set_fill(interpolate_color(RED_E, BLACK, 0.5))
        rects[2].set_fill(GREEN_E, 0.75)
        rects[3].set_fill(interpolate_color(RED_E, BLACK, 0.75))

        icons = VGroup(*(WomanIcon() for x in range(120)))
        icons.arrange_in_grid(
            10, 12,
            h_buff=1, v_buff=0.5,
            fill_rows_first=False,
        )
        icons.replace(rects, dim_to_match=1)
        icons.scale(0.98)
        icons.set_fill(GREY_C)
        icons[:10].set_fill(YELLOW)

        # Add terminology
        t2c = {
            "\\text{Disease}": YELLOW,
            "\\text{D}": YELLOW,
            "\\text{$\\neg$D}": GREY_B,
            "\\text{Not sick}": GREY_B,
            "{+}": GREEN,
            "{-}": RED,
            "\\text{Prior}": YELLOW,
            "\\text{Sensitivity}": GREEN,
            "\\text{FPR}": GREEN_D,
            "\\text{TP}": GREEN,
            "\\text{FP}": GREEN_D,
            "(": WHITE,
            ")": WHITE,
            "\\over": WHITE,
        }
        kw = {
            "tex_to_color_map": t2c,
            "font_size": 30,
        }

        braces = VGroup(
            Brace(rects[1], DOWN, buff=SMALL_BUFF),
            *(
                Brace(rect, u * RIGHT, buff=SMALL_BUFF)
                for rect, u in zip(rects, [-1, -1, 1, 1])
            )
        )
        braces.set_fill(GREY_B)
        terms = VGroup(
            OldTexText("Prior"),
            OldTexText("Sens."),
            OldTexText("FNR"),
            OldTexText("FPR"),
            OldTexText("Spec."),
        )
        terms[0].set_color(YELLOW)
        symbols = VGroup(
            OldTex("P(\\text{D})", **kw),
            OldTex("P({+} | \\text{D})", **kw),
            OldTex("P({-} | \\text{D})", **kw),
            OldTex("P({+} | \\text{$\\neg$D})", **kw),
            OldTex("P({-} | \\text{$\\neg$D})", **kw),
        )
        for term, symbol, brace in zip(terms, symbols, braces):
            term.scale(0.75)
            # CHANGE: Brace.direction is now get_direction()
            term.next_to(brace, brace.get_direction(), buff=SMALL_BUFF)
            symbol.next_to(brace, brace.get_direction(), buff=SMALL_BUFF)

        pop_group = VGroup(rects, icons, braces, symbols)
        pop_group.save_state()
        pop_group.set_height(5)
        pop_group.center().to_edge(DOWN)

        # Formula with jargon
        lhs = OldTex("P(\\text{Disease} \\text{ given } {+})", **kw)
        lhs.scale(48 / 30)

        term_formula = OldTex(
            """
            {(\\text{Prior})(\\text{Sensitivity})
            \\over
            (\\text{Prior})(\\text{Sensitivity})
            +
            (1 - \\text{Prior})(\\text{FPR})
            """,
            **kw,
        )

        tp_formula = OldTex("{\\text{TP} \\over \\text{TP} + \\text{FP}}", **kw)
        tp_formula.scale(1.25)

        prob_formula = OldTex(
            """
            P(\\text{D}) P({+} \\,|\\, \\text{D})
            \\over
            P(\\text{D}) P({+} \\,|\\, \\text{D})
            +
            """,
            """
            P(\\text{$\\neg$D}) P({+} \\,|\\, \\text{$\\neg$D})
            """,
            **kw
        )
        simple_prob_formula = OldTex(
            "P(\\text{D}) P({+} \\,|\\, \\text{D}) \\over P({+})",
            **kw
        )
        simple_prob_formula.scale(48 / 30)

        equals = VGroup(*(OldTex("=") for x in range(4)))
        equals[2:].scale(1.5).rotate(90 * DEGREES)

        formula = VGroup(lhs, equals[0], tp_formula, equals[1], term_formula)
        formula.arrange(RIGHT)
        formula.next_to(title, DOWN, MED_LARGE_BUFF)

        prob_group = VGroup(
            equals[2], prob_formula, equals[3], simple_prob_formula,
        )
        prob_group.arrange(DOWN, buff=0.35)
        prob_group.next_to(term_formula, DOWN, buff=0.35)

        # Show population
        self.add(title)
        self.play(FadeIn(lhs, DL))
        self.play(Write(equals[0]))
        self.wait()
        self.play(ShowIncreasingSubsets(icons, run_time=2))
        self.add(*pop_group)
        self.play(
            FadeIn(rects),
            LaggedStartMap(GrowFromCenter, braces),
            LaggedStartMap(FadeIn, symbols),
            run_time=1,
        )
        self.wait()

        pop_to_fade = VGroup(*icons[8:])
        pop_to_fade.remove(*icons[10::10])
        self.play(
            FadeIn(tp_formula),
            pop_to_fade.set_opacity, 0.1,
            symbols.set_opacity, 0.25,
            braces.set_fill, GREY_E, 1,
        )
        self.wait()

        # Show formula piece by piece
        prob_formula.save_state()
        prob_formula.move_to(term_formula, LEFT)

        srkw = {"buff": 0.025}
        blank_rects = VGroup(
            SurroundingRectangle(VGroup(prob_formula[0:10]), **srkw),
            SurroundingRectangle(VGroup(prob_formula[11:21]), **srkw),
            SurroundingRectangle(VGroup(prob_formula[22:]), **srkw),
        )
        blank_rects.set_stroke(GREEN, 2)
        blank_rects.set_fill(GREEN, 0.2)

        self.play(
            Write(equals[1]),
            LaggedStartMap(FadeIn, VGroup(
                prob_formula.get_part_by_tex("\\over"),
                prob_formula[21],
                *blank_rects
            ))
        )
        self.wait()
        self.play(
            symbols[0].set_opacity, 1,
            braces[0].set_fill, GREY_B,
            FadeIn(prob_formula[0:4]),
        )
        self.wait()
        self.play(
            symbols[1].set_opacity, 1,
            braces[1].set_fill, GREY_B,
            FadeIn(prob_formula[4:10]),
        )
        self.wait()
        self.play(
            TransformFromCopy(prob_formula[0:10], prob_formula[11:21])
        )
        self.wait()
        self.play(
            FadeIn(prob_formula[22:26])
        )
        self.wait()
        self.play(
            FadeIn(prob_formula[26:]),
            braces[3].set_fill, GREY_B,
            symbols[3].set_opacity, 1,
        )
        self.wait()
        self.play(FadeOut(blank_rects))
        self.wait()

        # Words over symbols
        self.play(
            pop_group.replace, pop_group.saved_state,
            Restore(prob_formula),
            FadeIn(term_formula, scale=2),
            FadeIn(equals[2], DOWN),
        )
        terms[2::2].set_opacity(0.2)
        self.play(
            FadeOut(symbols),
            FadeIn(terms),
        )
        self.wait()

        # Show confused
        randy = Randolph(height=2)
        randy.to_edge(DOWN)
        randy.shift(RIGHT)

        self.play(
            VFadeIn(randy),
            randy.change, 'maybe', prob_formula
        )
        self.play(Blink(randy))
        self.play(randy.change, 'confused', prob_formula)
        self.wait()
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change, 'pondering', pop_group,
        )
        self.play(Blink(randy))
        self.wait()

        # Show simplify denominator
        denom_rects = VGroup(
            SurroundingRectangle(prob_formula[11:], buff=0.025),
            SurroundingRectangle(simple_prob_formula[11:], buff=0.05),
        )
        denom_rects.set_stroke(GREY_B, 2)

        self.play(
            ShowCreation(denom_rects[0]),
            randy.look_at, denom_rects[0],
        )
        self.wait()
        self.play(
            TransformFromCopy(*denom_rects),
            FadeIn(simple_prob_formula, DOWN),
            FadeIn(equals[3], DOWN),
            randy.change, 'erm', simple_prob_formula
        )
        self.play(FadeOut(denom_rects))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change, "thinking")
        self.play(Blink(randy))
        self.wait()

        self.play(ShowCreation(denom_rects[1]))
        self.play(
            TransformFromCopy(*reversed(denom_rects)),
            randy.change, "sassy", denom_rects[0],
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()
