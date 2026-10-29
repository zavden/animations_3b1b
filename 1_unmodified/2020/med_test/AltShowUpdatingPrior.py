# ==============================================================================
# Scene:      AltShowUpdatingPrior
# Source:     videos/_2020/med_test.py (lines 2604-2790)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltShowUpdatingPrior.py AltShowUpdatingPrior -w -m --fps 15
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


class AltShowUpdatingPrior(Scene):
    def construct(self):
        N = 100
        post_denom = 11
        N_str = "{:,}".format(N)

        # Show prior
        woman = WomanIcon()
        population = VGroup(*[woman.copy() for x in range(N)])
        population.arrange_in_grid()
        population.set_fill(GREY)
        population[0].set_fill(YELLOW)
        population.set_height(5)

        prior_prob = OldTexText("1", " in ", N_str)
        prior_prob.set_color_by_tex("1", YELLOW)
        prior_prob.set_color_by_tex(N_str, GREY_B)
        prior_prob.next_to(population, UP, MED_LARGE_BUFF)
        prior_brace = Brace(prior_prob, UP, buff=SMALL_BUFF)
        prior_words = prior_brace.get_text("Prior")
        prior_words.add_updater(lambda m: m.next_to(prior_brace, UP, SMALL_BUFF))

        thousand_part = prior_prob.get_part_by_tex(N_str)
        pop_count = Integer(N, edge_to_fix=UL)
        pop_count.replace(thousand_part)
        pop_count.match_color(thousand_part)
        pop_count.set_value(0)
        prior_prob.replace_submobject(2, pop_count)

        VGroup(population, prior_prob, prior_brace, prior_words).to_corner(UL)

        self.add(prior_prob)

        # Before word
        before_words = OldTexText(
            "Probability of having the disease\\\\ ",
            "\\emph{before} taking a test"
        )
        before_words.set_color(BLUE_B)
        before_words.next_to(prior_words, RIGHT, buff=3, aligned_edge=UP)
        before_arrow1 = Arrow(before_words[0][0].get_left(), prior_prob.get_right() + MED_SMALL_BUFF * RIGHT)
        before_arrow2 = Arrow(before_words[0][0].get_left(), prior_words.get_right())
        before_arrow1.match_color(before_words)
        before_arrow2.match_color(before_words)

        self.play(
            FadeIn(before_words, lag_ratio=0.1),
            GrowArrow(before_arrow1),
            ShowIncreasingSubsets(population, run_time=2),
            ChangeDecimalToValue(pop_count, len(population), run_time=2),
        )
        self.wait()
        self.play(
            GrowFromCenter(prior_brace),
            FadeIn(prior_words, shift=0.5 * UP),
            ReplacementTransform(before_arrow1, before_arrow2)
        )
        self.wait()

        # Update arrow
        update_arrow = Arrow(2 * LEFT, 2 * RIGHT)
        update_arrow.set_thickness(0.1)
        update_arrow.center()
        update_arrow.match_y(pop_count)
        update_words = OldTexText("See positive test", tex_to_color_map={"positive": GREEN})
        update_words.next_to(update_arrow, UP, SMALL_BUFF)
        low_update_words = OldTexText("Update probability", font_size=36)
        low_update_words.next_to(update_arrow, DOWN, MED_SMALL_BUFF)

        # Posterior
        post_pop = population[:post_denom].copy()
        post_pop.arrange_in_grid(
            buff=get_norm(population[1].get_left() - population[0].get_right())
        )
        post_pop.match_height(population)
        post_pop.next_to(
            update_arrow, RIGHT,
            buff=abs(population.get_right()[0] - update_arrow.get_left()[0])
        )
        post_pop.align_to(population, UP)

        def give_pop_plusses(pop):
            for icon in pop:
                plus = OldTex("+")
                plus.set_color(GREEN)
                plus.set_width(icon.get_width() / 2)
                plus.move_to(icon.get_corner(UR))
                icon.add(plus)

        give_pop_plusses(post_pop)

        post_prob = prior_prob.copy()
        post_prob[2].set_value(post_denom)
        post_prob.next_to(post_pop, UP, buff=MED_LARGE_BUFF)

        roughly = OldTexText("(roughly)", font_size=24)
        roughly.next_to(post_prob, RIGHT, buff=0.2)

        post_prob[2].set_value(0)
        self.play(
            FadeIn(update_words, lag_ratio=0.2),
            FadeOut(before_words),
            ReplacementTransform(before_arrow2, update_arrow, path_arc=30 * DEGREES),
            FadeIn(low_update_words, lag_ratio=0.2),
        )
        self.add(post_prob)
        self.play(
            ShowIncreasingSubsets(post_pop, run_time=1),
            ChangeDecimalToValue(post_prob[2], post_denom, run_time=1),
            FadeIn(roughly),
        )
        self.wait()

        post_brace = Brace(post_prob, UP, buff=SMALL_BUFF)
        post_words = post_brace.get_text("Posterior")
        post_words.add_updater(lambda m: m.next_to(post_brace, UP, SMALL_BUFF))
        post_words.update(0)

        self.play(
            GrowFromCenter(post_brace),
            FadeIn(post_words, shift=0.5 * UP)
        )
        self.wait()

        post_group = VGroup(
            update_arrow, update_words,
            post_pop, post_prob, post_brace, post_words,
        )
        post_group.save_state()

        return
        # Change prior and posterior
        pop100, pop11, pop10, pop2 = pops = [
            VGroup(*[woman.copy() for x in range(n)])
            for n in [100, 11, 10, 2]
        ]
        for pop in pops:
            pop.arrange_in_grid()
            pop.set_fill(GREY)
            pop[0].set_fill(YELLOW)
            pop.scale(
                post_pop[0].get_height() / pop[0].get_height()
            )

        pop100.replace(population)
        pop11.move_to(post_pop, UP)
        pop11.shift(0.2 * LEFT)
        pop10.move_to(population, UP)
        pop10.shift(0.4 * LEFT)
        pop2.move_to(post_pop, UP)
        pop2.shift(0.3 * LEFT)

        give_pop_plusses(pop11)
        give_pop_plusses(pop2)

        def replace_population_anims(old_pop, new_pop, count, brace):
            count.set_value(len(new_pop))
            brace.generate_target()
            brace.target.match_width(
                Line(brace.get_left(), count.get_right()),
                about_edge=LEFT,
                stretch=True,
            )
            count.set_value(len(old_pop))

            return [
                FadeOut(old_pop, lag_ratio=0.1),
                ShowIncreasingSubsets(new_pop),
                ChangeDecimalToValue(count, len(new_pop)),
                MoveToTarget(brace)
            ]

        self.play(
            *replace_population_anims(population, pop100, prior_prob[2], prior_brace)
        )
        self.play(
            *replace_population_anims(post_pop, pop11, post_prob[2], post_brace),
        )
        self.wait(2)
        self.play(
            *replace_population_anims(pop100, pop10, prior_prob[2], prior_brace),
            prior_words.shift, 0.1 * LEFT
        )
        self.play(
            *replace_population_anims(pop11, pop2, post_prob[2], post_brace)
        )
        self.wait(2)
