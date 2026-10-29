# ==============================================================================
# Scene:      PrevalenceVsPrior
# Source:     videos/_2020/med_test.py (lines 4444-4541)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrevalenceVsPrior.py PrevalenceVsPrior -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


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


class PrevalenceVsPrior(Scene):
    def construct(self):
        # Prior and prevalence
        eq = OldTexText(
            "Prevalence = Prior",
            tex_to_color_map={
                "Prevalence": WHITE,
                "Prior": YELLOW,
            }
        )
        eq.shift(UP)
        prior = eq[2]
        prev = eq[0]

        strike = Line(eq.get_left(), eq.get_right())
        strike.set_stroke(RED, 4)
        not_words = OldTexText("Not necessarily!")
        not_words.set_color(RED)
        not_words.match_width(eq)
        not_words.next_to(eq, DOWN, MED_LARGE_BUFF)

        factors = VGroup(
            OldTexText("Prevalence"),
            OldTexText("Symptoms"),
            OldTexText("Contacts\\\\", "(if contagious)"),
        )
        factors.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        factors.shift(prev.get_center() - factors[0].get_center())

        prior.generate_target()
        prior.target.match_y(factors[1])
        prior.target.shift(0.5 * RIGHT)
        arrows = VGroup(*(
            Arrow(
                factor.get_right(), prior.target.get_corner(LEFT + u * UP),
                buff=0.1,
                max_tip_length_to_length_ratio=0.25,
            )
            for u, factor in zip([1, 0, -1], factors)
        ))

        population = Population(100)
        population.set_height(7)
        population.to_edge(LEFT)
        population.set_fill(GREY_C)
        random.choice(population).set_color(YELLOW)

        self.play(Write(prev))
        self.play(ShowIncreasingSubsets(population, run_time=3))
        self.wait()
        self.play(Write(eq[1:]))
        self.wait()

        self.play(
            ShowCreation(strike),
            FadeIn(not_words, shift=0.2 * DOWN, rate_func=squish_rate_func(smooth, 0.3, 1))
        )
        self.wait()

        self.play(
            Uncreate(strike),
            MoveToTarget(prior),
            ReplacementTransform(eq[1], arrows),
            LaggedStartMap(FadeIn, factors[1:], shift=0.25 * DOWN),
            FadeOut(not_words, shift=DOWN)
        )
        self.remove(prev)
        self.add(factors)
        self.wait()

        # Symptoms
        randy = Randolph(height=1.5)
        randy.to_corner(UR)
        randy.shift(LEFT)

        self.play(FadeIn(randy))
        self.play(
            ShowCreationThenFadeOut(Underline(factors[1], color=RED)),
            randy.change, "sick",
            randy.set_color, SICKLY_GREEN,
        )
        self.wait()

        # Contagion (implicit)
        self.play(
            ShowCreationThenFadeOut(Underline(factors[2][0], color=RED)),
            ShowCreationThenFadeOut(Underline(factors[2][1], color=RED)),
        )
        self.wait()

        self.play(
            LaggedStartMap(
                FadeOut, VGroup(
                    randy, prior, *arrows, *factors,
                ),
                shift=DOWN,
            )
        )
