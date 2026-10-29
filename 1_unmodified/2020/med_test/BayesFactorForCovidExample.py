# ==============================================================================
# Scene:      BayesFactorForCovidExample
# Source:     videos/_2020/med_test.py (lines 6238-6380)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BayesFactorForCovidExample.py BayesFactorForCovidExample -w -m --fps 15
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


class BayesFactorForCovidExample(Scene):
    def construct(self):
        # Titles
        titles = VGroup(
            OldTexText("Prior odds", color=YELLOW),
            OldTexText("Bayes factor", color=GREEN),
            OldTexText("Posterior odds", color=BLUE),
        )
        titles.scale(1.25)
        titles[0].shift(FRAME_WIDTH * LEFT / 3)
        titles[2].shift(FRAME_WIDTH * RIGHT / 3)
        titles.to_edge(UP)

        v_lines = VGroup(*(
            Line(UP, DOWN).set_height(FRAME_HEIGHT).move_to(
                FRAME_WIDTH * x * RIGHT / 6,
            )
            for x in (-1, 1)
        ))
        self.add(titles, v_lines)

        # Prior odds
        prior_odds = OldTexText(
            "1", "\\,:\\,", "999",
            tex_to_color_map={"1": YELLOW}
        )
        prior_odds.next_to(titles[0], DOWN, buff=1)

        population = Population(1000)
        population.set_width(FRAME_WIDTH / 5)
        population[0].set_color(YELLOW)
        population[0].next_to(population[1:], LEFT, MED_LARGE_BUFF)
        colon = OldTex(":")
        colon.move_to(midpoint(population[0].get_right(), population[1:].get_left()))
        pop_ratio = VGroup(population[0], colon, population[1:])
        pop_ratio.next_to(prior_odds, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(prior_odds, shift=0.2 * DOWN, scale=1.2),
            FadeIn(pop_ratio, lag_ratio=0.01),
        )
        self.wait()

        # Bayes factor
        bf_lhs = OldTex(
            """
            {
                P(+ \\,|\\, \\text{COVID})
                \\over
                P(+ \\,|\\, \\text{No COVID})
            }
            """,
            tex_to_color_map={
                "+": GREEN,
                "\\text{COVID}": YELLOW,
                "\\text{No COVID}": GREY_A,
            }
        )
        bf_lhs.next_to(titles[1], DOWN)
        bf_rhs = OldTex(
            "= {90\\%", "\\over", "1\\%}",
            tex_to_color_map={
                "90\\%": GREEN_D,
                "1\\%": GREEN,
            }
        )
        bf = VGroup(bf_lhs, bf_rhs)
        bf.arrange(RIGHT)
        bf.set_width(0.9 * FRAME_WIDTH / 3)
        bf.next_to(titles[1], DOWN, MED_LARGE_BUFF)

        eq_90 = OldTex("=", "90")
        eq_90.next_to(bf, DOWN, MED_LARGE_BUFF)
        eq_90[1].save_state()
        eq_90[1].replace(bf_rhs[1:], stretch=True)
        eq_90[1].set_opacity(0)
        eq_90[1].set_color(GREEN)

        self.play(
            FadeIn(bf_lhs, lag_ratio=0.1),
            FadeIn(bf_rhs[0::2], lag_ratio=0.1),
        )
        self.wait()
        self.play(Write(bf_rhs[1]))
        self.wait()
        self.play(Write(bf_rhs[3]))
        self.wait()
        self.play(
            TransformFromCopy(bf_rhs[0], eq_90[0]),
            Restore(eq_90[1])
        )
        self.wait()

        # Posterior
        post_odds = OldTex("90", ":", "999")
        post_odds.match_x(titles[2])
        post_odds.match_y(prior_odds)

        arrow = Vector(DOWN)
        arrow.next_to(post_odds, DOWN)

        fraction = OldTex(
            "{90", "\\over", "90", "+", "999}",
            "\\approx", "8.3\\%"
        )
        fraction.next_to(arrow, DOWN)

        self.play(LaggedStart(
            TransformFromCopy(eq_90[1], post_odds[0]),
            TransformFromCopy(prior_odds[1:], post_odds[1:]),
            lag_ratio=0.4
        ))
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(fraction, DOWN)
        )

        # Approximate
        approx1 = OldTex("\\approx", "90", ":", "1,000")
        approx2 = OldTex("\\approx", "9", ":", "100")
        approx3 = OldTex("\\approx 9\\%")

        approx1.next_to(arrow, DOWN)
        approx2.move_to(approx1)
        arrow2 = arrow.copy()
        arrow2.next_to(approx2, DOWN)
        approx3.next_to(arrow2, DOWN)

        self.play(
            FadeOut(fraction, 0.5 * DOWN),
            FadeIn(approx1, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            ReplacementTransform(approx1, approx2)
        )
        self.wait()
        self.play(
            GrowArrow(arrow2),
            FadeIn(approx3, DOWN)
        )
        self.wait()
