# ==============================================================================
# Scene:      HowMuchCanYouChangeThisPrior
# Source:     videos/_2018/eop/bayes_footnote.py (lines 807-882)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowMuchCanYouChangeThisPrior.py HowMuchCanYouChangeThisPrior -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SICKLY_GREEN = "#9BBD37"


class ShowRestrictedSpace(Scene):
    CONFIG = {
        "n_rows" : 25,
        "n_cols" : 40,
        "n_false_positives" : 10,
        "false_positive_color" : YELLOW_E,
    }
    def construct(self):
        self.add_all_creatures()
        self.show_accurate_positive_result()
        self.show_false_positive_conditional()
        self.show_false_positive_individuals()
        self.fade_out_negative_result_individuals()
        self.show_posterior_probability()
        self.contrast_with_prior()

    def add_all_creatures(self):
        title = OldTexText("$1{,}000$ individuals")
        title.to_edge(UP)
        all_creatures = self.get_all_creatures()
        sick_one = all_creatures.sick_one
        healthy_creatures = all_creatures.healthy_creatures

        sick_one.save_state()
        sick_one_words = OldTexText("1 sick")
        sick_one_words.next_to(sick_one, RIGHT)
        sick_one_words.to_edge(RIGHT)
        sick_one_words.set_color(SICKLY_GREEN)
        sick_one_arrow = Arrow(
            sick_one_words, sick_one,
            color = SICKLY_GREEN
        )

        healthy_words = OldTexText("999 healthy")
        healthy_words.next_to(sick_one_words, UP, MED_LARGE_BUFF)
        healthy_words.shift_onto_screen()
        healthy_words.set_color(BLUE)

        self.add(title)
        self.play(LaggedStartMap(FadeIn, all_creatures))
        self.play(
            FadeIn(sick_one_words),
            ShowCreation(sick_one_arrow)
        )
        self.play(
            sick_one.set_height, 2,
            sick_one.next_to, sick_one_words, DOWN,
            sick_one.to_edge, RIGHT,
        )
        self.wait()
        self.play(sick_one.restore)
        self.play(
            Write(healthy_words),
            LaggedStartMap(
                ApplyMethod, healthy_creatures,
                lambda m : (m.shift, MED_SMALL_BUFF*UP),
                rate_func = there_and_back,
                lag_ratio = 0.2,
            )
        )
        self.wait()
        self.play(FadeOut(title))

        self.all_creatures = all_creatures
        self.healthy_creatures = healthy_creatures
        self.sick_one = sick_one
        self.sick_one_label = VGroup(sick_one_words, sick_one_arrow)
        self.healthy_ones_label = healthy_words

    def show_accurate_positive_result(self):
        equation = OldTex(
            "P(", "\\text{Test positive }", "|", 
            "\\text{ sick}", ")", "=", "100\\%"
        )
        equation.set_color_by_tex("positive", YELLOW)
        equation.set_color_by_tex("sick", SICKLY_GREEN)
        equation.to_corner(UP+LEFT)

        self.play(Write(equation, run_time = 1))
        self.wait(2)

        self.disease_conditional = equation

    def show_false_positive_conditional(self):
        equation = OldTex(
            "P(", "\\text{Test positive }", "|", 
            "\\text{ healthy}", ")", "=", "1\\%"
        )
        equation.set_color_by_tex("positive", YELLOW)
        equation.set_color_by_tex("healthy", BLUE)
        equation.to_corner(UP+LEFT)

        self.play(ReplacementTransform(
            self.disease_conditional, equation
        ))
        self.wait()

        self.healthy_conditional = equation

    def show_false_positive_individuals(self):
        all_creatures = self.all_creatures
        false_positives = VGroup(
            *all_creatures[-1][1:1+self.n_false_positives]
        )
        self.healthy_creatures.remove(*false_positives)
        brace = Brace(false_positives, RIGHT)
        words = OldTexText("10 False positives")
        words.scale(0.8)
        words.next_to(brace, RIGHT)

        self.play(
            GrowFromCenter(brace),
            LaggedStartMap(
                ApplyMethod, false_positives,
                lambda pi : (pi.set_color, self.false_positive_color),
                run_time = 1
            )
        )
        self.play(Write(words))
        self.wait()

        self.false_positives = false_positives
        self.false_positives_brace = brace
        self.false_positives_words = words

    def fade_out_negative_result_individuals(self):
        to_fade = VGroup(
            self.healthy_creatures,
            self.healthy_conditional,
            self.sick_one_label,
            self.healthy_ones_label,
        )
        movers = VGroup(self.sick_one, *self.false_positives)
        movers.generate_target()
        movers.target.set_width(1)
        movers.target.arrange(RIGHT)
        movers.target.shift(DOWN)
        brace = Brace(VGroup(*movers.target[1:]))

        words = OldTexText("You are one of these")
        words.to_edge(UP)
        arrows = [
            Arrow(words.get_bottom(), movers.target[i].get_top())
            for i in (0, -1)
        ]

        self.play(FadeOut(to_fade))
        self.play(
            MoveToTarget(movers),
            ReplacementTransform(self.false_positives_brace, brace),
            self.false_positives_words.next_to, brace, DOWN
        )
        self.play(
            Write(words, run_time = 2),
            ShowCreation(arrows[0])
        )
        self.play(Transform(
            *arrows, run_time = 4, rate_func = there_and_back
        ))
        self.play(*list(map(FadeOut, [words, arrows[0]])))

        self.brace = brace

    def show_posterior_probability(self):
        posterior = OldTex(
            "P(", "\\text{Sick }", "|", 
            "\\text{ Positive test result}", ")",
            "\\approx \\frac{1}{11}", "\\approx 9\\%"
        )
        posterior.set_color_by_tex("Sick", SICKLY_GREEN)
        posterior.set_color_by_tex("Positive", YELLOW)
        posterior.to_edge(UP)
        posterior.shift(LEFT)

        self.play(FadeIn(posterior))
        self.wait(2)

        self.posterior = posterior

    def contrast_with_prior(self):
        prior = OldTex(
            "P(", "\\text{Sick}", ")", "= 0.1\\%"
        )
        prior.set_color_by_tex("Sick", SICKLY_GREEN)
        prior.move_to(self.posterior, UP+RIGHT)

        self.revert_to_original_skipping_status()
        self.play(
            Write(prior, run_time = 1),
            self.posterior.shift, DOWN,
        )
        arrow = Arrow(
            prior.get_right(), self.posterior.get_right(),
            path_arc = -np.pi,
        )
        times_90 = OldTex("\\times 90")
        times_90.next_to(arrow, RIGHT)
        self.play(ShowCreation(arrow))
        self.play(Write(times_90, run_time = 1))
        self.wait(2)

    ######

    def get_all_creatures(self):
        creature = PiCreature()
        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(self.n_rows)
            ]).arrange(DOWN, SMALL_BUFF)
            for x in range(self.n_cols)
        ]).arrange(RIGHT, SMALL_BUFF)
        all_creatures.set_height(5)
        all_creatures.center().to_edge(LEFT)

        healthy_creatures = VGroup(*it.chain(*all_creatures))
        sick_one = all_creatures[-1][0]
        sick_one.change_mode("sick")
        sick_one.set_color(SICKLY_GREEN)
        healthy_creatures.remove(sick_one)
        all_creatures.sick_one = sick_one
        all_creatures.healthy_creatures = healthy_creatures
        return all_creatures


class HowMuchCanYouChangeThisPrior(ShowRestrictedSpace, PiCreatureScene):
    def construct(self):
        self.single_out_new_sick_one()
        self.show_subgroups()
        self.isolate_special_group()

    def create_pi_creatures(self):
        creatures = self.get_all_creatures()
        creatures.set_height(6.5)
        creatures.center()
        creatures.submobjects  = list(it.chain(*creatures))

        self.add(creatures)
        self.sick_one = creatures.sick_one
        return creatures

    def single_out_new_sick_one(self):
        creatures = self.pi_creatures
        sick_one = self.sick_one
        new_sick_one = sick_one.copy()
        new_sick_one.shift(1.3*sick_one.get_width()*RIGHT)
        sick_one.change_mode("plain")
        sick_one.set_color(BLUE_E)

        self.add(new_sick_one)
        self.sick_one = new_sick_one

    def show_subgroups(self):
        subgroups = VGroup(*[
            VGroup(*it.chain(
                self.pi_creatures[i:i+5],
                self.pi_creatures[i+25:i+25+5:]
            ))
            for i in range(0, 1000)
            if i%5 == 0 and (i/25)%2 == 0
        ])
        special_group = subgroups[-5]
        special_group.add(self.sick_one)
        subgroups.generate_target()
        width_factor = FRAME_WIDTH/subgroups.get_width()
        height_factor = FRAME_HEIGHT/subgroups.get_height()
        subgroups.target.stretch_in_place(width_factor, 0)
        subgroups.target.stretch_in_place(height_factor, 1)
        for subgroup in subgroups.target:
            subgroup.stretch_in_place(1./width_factor, 0)
            subgroup.stretch_in_place(1./height_factor, 1)

        self.wait()
        self.play(MoveToTarget(subgroups))
        subgroups.remove(special_group)

        rects = VGroup(*[
            SurroundingRectangle(
                group, buff = 0, color = GREEN
            )
            for group in subgroups
        ])
        special_rect = SurroundingRectangle(
            special_group, buff = 0, color = RED
        )
        self.play(FadeIn(rects), FadeIn(special_rect))
        self.wait()

        self.to_fade = VGroup(subgroups, rects)
        self.special_group = special_group
        self.special_rect = special_rect

    def isolate_special_group(self):
        to_fade, special_group = self.to_fade, self.special_group
        self.play(FadeOut(to_fade))
        self.play(
            FadeOut(self.special_rect),
            special_group.set_height, 6,
            special_group.center,
        )
        self.wait()
