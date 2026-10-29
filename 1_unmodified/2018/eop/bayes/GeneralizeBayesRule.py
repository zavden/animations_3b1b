# ==============================================================================
# Scene:      GeneralizeBayesRule
# Source:     videos/_2018/eop/bayes.py (lines 1241-1534)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GeneralizeBayesRule.py GeneralizeBayesRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralizeBayesRule(SampleSpaceScene):
    def construct(self):
        self.add_sample_space()
        self.add_title()
        self.add_posterior_rectangles()
        self.add_bayes_rule()
        self.talk_through_terms()
        self.name_likelihood()
        self.dont_memorize()
        self.show_space_restriction()

    def add_sample_space(self):
        sample_space = SampleSpace(
            full_space_config = {
                "height" : 3,
                "width" : 3,
                "fill_opacity" : 0
            }
        )
        sample_space.divide_horizontally(0.4)
        sample_space.horizontal_parts.set_fill(opacity = 0)
        labels = [
            OldTex("P(", "B", ")"),
            OldTex("P(\\text{not }", "B", ")"),
        ]
        for label in labels:
            label.scale(0.7)
            self.color_label(label)
        sample_space.get_side_braces_and_labels(labels)
        sample_space.add_braces_and_labels()

        parts = sample_space.horizontal_parts
        values = [0.8, 0.4]
        given_strs = ["", "\\text{not }"]
        color_pairs = [(GREEN, BLUE), (GREEN_E, BLUE_E)]
        vects = [UP, DOWN]
        for tup in zip(parts, values, given_strs, color_pairs, vects):
            part, value, given_str, colors, vect = tup
            part.divide_vertically(value, colors = colors)
            part.vertical_parts.set_fill(opacity = 0.8)
            label = OldTex(
                "P(", "I", "|", given_str, "B", ")"
            )
            label.scale(0.7)
            self.color_label(label)
            part.get_subdivision_braces_and_labels(
                part.vertical_parts, [label], vect
            )
            sample_space.add(
                part.vertical_parts.braces,
                part.vertical_parts.labels,
            )
        sample_space.to_edge(LEFT)

        self.add(sample_space)
        self.sample_space = sample_space

    def add_title(self):
        title = OldTexText(
            "Updating", "Beliefs", "from new", "Information"
        )
        self.color_label(title)
        title.scale(0.8)
        title.to_corner(UP+LEFT)

        self.add(title)

    def add_posterior_rectangles(self):
        prior_rects = self.get_prior_rectangles()
        post_rects = self.get_posterior_rectangles()

        label = OldTex("P(", "B", "|", "I", ")")
        label.scale(0.7)
        self.color_label(label)
        braces, labels = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [label]
        )

        self.play(ReplacementTransform(
            prior_rects.copy(), post_rects,
            run_time = 2
        ))
        self.play(
            GrowFromCenter(braces),
            Write(label)
        )

        self.post_rects = post_rects
        self.posterior_tex = label

    def add_bayes_rule(self):
        rule = OldTex(
             "=", "{P(", "B", ")", "P(", "I", "|", "B", ")",
            "\\over", "P(", "I", ")}",
        )
        self.color_label(rule)
        rule.scale(0.7)
        rule.next_to(self.posterior_tex, RIGHT)

        bayes_rule_words = OldTexText("Bayes' rule")
        bayes_rule_words.next_to(VGroup(*rule[1:]), UP, LARGE_BUFF)
        bayes_rule_words.shift_onto_screen()

        self.play(FadeIn(rule))
        self.play(Write(bayes_rule_words))
        self.wait(2)

        self.bayes_rule_words = bayes_rule_words
        self.bayes_rule = rule

    def talk_through_terms(self):
        prior = self.sample_space.horizontal_parts.labels[0]
        posterior = self.posterior_tex
        prior_target = VGroup(*self.bayes_rule[1:4])
        likelihood = VGroup(*self.bayes_rule[4:9])
        P_I = VGroup(*self.bayes_rule[-3:])

        prior_word = OldTexText("Prior")
        posterior_word = OldTexText("Posterior")
        words = [prior_word, posterior_word]
        for word in words:
            word.set_color(YELLOW)
            word.scale(0.7)
        prior_rect = SurroundingRectangle(prior)
        posterior_rect = SurroundingRectangle(posterior)
        for rect in prior_rect, posterior_rect:
            rect.set_stroke(YELLOW, 2)

        prior_word.next_to(prior, UP, LARGE_BUFF)
        posterior_word.next_to(posterior, DOWN, LARGE_BUFF)
        for word in words:
            word.shift_onto_screen()
        prior_arrow = Arrow(
            prior_word.get_bottom(), prior.get_top(),
            tip_length = 0.15
        )
        posterior_arrow = Arrow(
            posterior_word.get_top(), posterior.get_bottom(),
            tip_length = 0.15
        )

        self.play(
            Write(prior_word), 
            ShowCreation(prior_arrow), 
            ShowCreation(prior_rect),
        ) 
        self.wait()
        self.play(Transform(
            prior.copy(), prior_target,
            run_time = 2,
            path_arc = -np.pi/3,
            remover = True,
        ))
        self.wait()
        parts = self.sample_space[0].vertical_parts
        self.play(
            Indicate(likelihood),
            Indicate(parts.labels),
            Indicate(parts.braces),
        )
        self.wait()
        self.play(Indicate(P_I))
        self.play(FocusOn(self.sample_space[0][0]))
        for i in range(2):
            self.play(Indicate(
                self.sample_space[i][0], 
                scale_factor = 1
            ))
        self.wait()
        self.play(
            Write(posterior_word), 
            ShowCreation(posterior_arrow), 
            ShowCreation(posterior_rect),
        )

        self.prior_label = VGroup(prior_word, prior_arrow, prior_rect)
        self.posterior_label = VGroup(posterior_word, posterior_arrow, posterior_rect)
        self.likelihood = likelihood

    def name_likelihood(self):
        likelihoods = [
            self.sample_space[0].vertical_parts.labels[0],
            self.likelihood
        ]
        rects = [
            SurroundingRectangle(mob, buff = SMALL_BUFF)
            for mob in likelihoods
        ]
        name = OldTexText("Likelihood")
        name.scale(0.7)
        name.next_to(self.posterior_tex, UP, 1.5*LARGE_BUFF)
        arrows = [
            Arrow(
                name, rect.get_edge_center(vect), 
                tip_length = 0.15
            )
            for rect, vect in zip(rects, [RIGHT, UP])
        ]
        VGroup(name, *arrows+rects).set_color(YELLOW)

        morty = Mortimer()
        morty.scale(0.5)
        morty.next_to(rects[1], UP, buff = 0)
        morty.shift(SMALL_BUFF*RIGHT)

        self.play(
            self.bayes_rule_words.to_edge, UP,
            Write(name),
            *list(map(ShowCreation, arrows+rects))
        )
        self.wait()

        self.play(FadeIn(morty))
        self.play(morty.change, "confused", name)
        self.play(Blink(morty))
        self.play(morty.look, DOWN)
        self.wait()
        self.play(morty.look_at, name)
        self.play(Blink(morty))
        self.play(morty.change, "shruggie")

        self.play(FadeOut(VGroup(name, *arrows+rects)))
        self.play(FadeOut(morty))
        self.play(FadeOut(self.posterior_label))
        self.play(FadeOut(self.prior_label))

    def dont_memorize(self):
        rule = VGroup(*self.bayes_rule[1:])
        word = OldTexText("Memorize")
        word.scale(0.7)
        word.next_to(rule, DOWN)
        cross = VGroup(
            Line(UP+LEFT, DOWN+RIGHT),
            Line(UP+RIGHT, DOWN+LEFT),
        )
        cross.set_stroke(RED, 6)
        cross.replace(word, stretch = True)

        self.play(Write(word))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
        self.play(FadeOut(VGroup(cross, word)))
        self.play(FadeOut(self.bayes_rule))
        self.play(
            FadeOut(self.post_rects),
            FadeOut(self.post_rects.braces),
            FadeOut(self.post_rects.labels),
        )

    def show_space_restriction(self):
        prior_rects = self.get_prior_rectangles()
        non_I_rects = VGroup(*[
            self.sample_space[i][1]
            for i in range(2)
        ])
        post_rects = self.post_rects

        self.play(non_I_rects.fade, 0.8)
        self.play(LaggedStartMap(
            ApplyMethod,
            prior_rects,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back,
            lag_ratio = 0.7
        ))
        self.wait(2)
        self.play(ReplacementTransform(
            prior_rects.copy(), post_rects,
            run_time = 2
        ))
        self.play(*list(map(FadeIn, [
            post_rects.braces, post_rects.labels
        ])))
        self.wait()
        self.play(*self.get_conditional_change_anims(1, 0.2, post_rects))
        self.play(*self.get_conditional_change_anims(0, 0.6, post_rects))
        self.wait()
        self.play(*it.chain(
            self.get_division_change_animations(
                self.sample_space, 
                self.sample_space.horizontal_parts,
                0.1
            ),
            self.get_posterior_rectangle_change_anims(post_rects)
        ))
        self.wait(3)


    ####

    def color_label(self, label):
        label.set_color_by_tex("B", RED)
        label.set_color_by_tex("I", GREEN)
