# ==============================================================================
# Scene:      UpdatePokerPrior
# Source:     videos/_2018/eop/bayes.py (lines 450-1068)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UpdatePokerPrior.py UpdatePokerPrior -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the GL SuitSymbol has no CONFIG dict; use Cairo SuitSymbol.CONFIG["red"] (#D02028) directly
# ==============================================================================

from manim_imports_ext import *

class UpdatePokerPrior(SampleSpaceScene):
    CONFIG = {
        "double_heart_template" : "HH",
        "cash_string" : "\\$\\$\\$",
    }
    def construct(self):
        self.add_sample_space()
        self.add_top_conditionals()
        self.react_to_top_conditionals()
        self.add_bottom_conditionals()
        self.ask_where_conditionals_come_from()
        self.vary_conditionals()
        self.show_restricted_space()
        self.write_P_flush_given_bet()
        self.reshape_rectangles()
        self.compare_prior_to_posterior()
        self.preview_tweaks()
        self.tweak_non_flush_case()
        self.tweak_flush_case()
        self.tweak_prior()
        self.compute_posterior()

    def add_sample_space(self):
        p = 1./22
        sample_space = SampleSpace(fill_opacity = 0)
        sample_space.shift(LEFT)
        sample_space.divide_horizontally(p, colors = [
            # CHANGE: the GL SuitSymbol has no CONFIG dict; use Cairo SuitSymbol.CONFIG["red"] (#D02028) directly
            "#D02028", BLUE_E
        ])
        labels = self.get_prior_labels(p)
        braces_and_labels = sample_space.get_side_braces_and_labels(labels)

        self.play(
            LaggedStartMap(FadeIn, sample_space),
            Write(braces_and_labels)
        )
        self.wait()

        sample_space.add(braces_and_labels)
        self.sample_space = sample_space

    def add_top_conditionals(self):
        top_part = self.sample_space.horizontal_parts[0]
        color = average_color(YELLOW, GREEN, GREEN)
        p = 0.97
        top_part.divide_vertically(p, colors = [color, BLUE])
        label = self.get_conditional_label(p, True)
        brace, _ignore = top_part.get_top_braces_and_labels([label])

        explanation = OldTexText(
            "Probability of", "high bet", "given", "flush"
        )
        explanation.set_color_by_tex("high bet", GREEN)
        explanation.set_color_by_tex("flush", RED)
        explanation.scale(0.6)
        explanation.next_to(label, UP)

        self.play(
            FadeIn(top_part.vertical_parts),
            FadeIn(label),
            GrowFromCenter(brace),
        )
        self.play(Write(explanation, run_time = 3))
        self.wait(2)

        self.sample_space.add(brace, label)

        self.top_explanation = explanation
        self.top_conditional_rhs = label[-1]

    def react_to_top_conditionals(self):
        her = PiCreature(color = BLUE_B).flip()
        her.next_to(self.sample_space, RIGHT)
        her.to_edge(RIGHT)
        glasses = SunGlasses(her)
        glasses.save_state()
        glasses.shift(UP)
        glasses.set_fill(opacity = 0)
        her.glasses = glasses

        self.play(FadeIn(her))
        self.play(glasses.restore)
        self.play(
            her.change_mode, "happy", 
            Animation(glasses)
        )
        self.wait(2)

        self.her = her
        
    def add_bottom_conditionals(self):
        her = self.her
        bottom_part = self.sample_space.horizontal_parts[1]
        p = 0.3
        bottom_part.divide_vertically(p, colors = [GREEN_E, BLUE_E])
        label = self.get_conditional_label(p, False)
        brace, _ignore = bottom_part.get_bottom_braces_and_labels([label])

        explanation = OldTexText(
            "Probability of", "high bet", "given", "no flush"
        )
        explanation.set_color_by_tex("high bet", GREEN)
        explanation.set_color_by_tex("no flush", RED)
        explanation.scale(0.6)
        explanation.next_to(label, DOWN)

        self.play(DrawBorderThenFill(bottom_part.vertical_parts))
        self.play(
            GrowFromCenter(brace),
            FadeIn(label)
        )
        self.play(
            her.change_mode, "shruggie",
            MaintainPositionRelativeTo(her.glasses, her.eyes)
        )
        self.wait()
        self.play(*[
            ReplacementTransform(
                VGroup(*label[i1:i2]).copy(),
                VGroup(explanation[j]),
                run_time = 2,
                rate_func = squish_rate_func(smooth, a, a+0.5)
            )
            for a, (i1, i2, j) in zip(np.linspace(0, 0.5, 4), [
                (0, 1, 0),
                (1, 2, 1),
                (2, 3, 2),
                (3, 6, 3),
            ])
        ])
        self.wait()
        self.play(Write(VGroup(*label[-2:])))
        self.wait(2)
        self.play(*list(map(FadeOut, [her, her.glasses])))

        self.sample_space.add(brace, label)
        self.bottom_explanation = explanation
        self.bottom_conditional_rhs = label[-1]

    def ask_where_conditionals_come_from(self):
        randy = Randolph().flip()
        randy.scale(0.75)
        randy.to_edge(RIGHT)
        randy.shift(2*DOWN)
        words = OldTexText("Where do these \\\\", "numbers", "come from?")
        numbers_word = words.get_part_by_tex("numbers")
        numbers_word.set_color(YELLOW)
        words.scale(0.7)
        bubble = ThoughtBubble(height = 3, width = 4)
        bubble.pin_to(randy)
        bubble.shift(MED_LARGE_BUFF*RIGHT)
        bubble.add_content(words)

        numbers = VGroup(
            self.top_conditional_rhs, 
            self.bottom_conditional_rhs
        )
        numbers.save_state()
        arrows = VGroup(*[
            Arrow(
                numbers_word.get_left(), 
                num.get_right(), 
                buff = 2*SMALL_BUFF
            )
            for num in numbers
        ])

        questions = VGroup(*list(map(TexText, [
            "Does she bluff?",
            "How much does she have?",
            "Does she take risks?",
            "What's her model of me?",
            "\\vdots"
        ])))
        questions.arrange(DOWN, aligned_edge = LEFT)
        questions[-1].next_to(questions[-2], DOWN)
        questions.scale(0.7)
        questions.next_to(randy, UP)
        questions.shift_onto_screen()

        self.play(
            randy.change_mode, "confused",
            ShowCreation(bubble),
            Write(words, run_time = 2)
        )
        self.play(*list(map(ShowCreation, arrows)))
        self.play(numbers.set_color, YELLOW)
        self.play(Blink(randy))
        self.play(randy.change_mode, "maybe")
        self.play(*list(map(FadeOut, [
            bubble, words, arrows
        ])))
        for question in questions:
            self.play(
                FadeIn(question),
                randy.look_at, question
            )
        self.wait()
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change_mode, "pondering",
            FadeOut(questions)
        )

        self.randy = randy

    def vary_conditionals(self):
        randy = self.randy
        rects = VGroup(*[
            SurroundingRectangle(
                VGroup(explanation),
                buff = SMALL_BUFF,
            )
            for explanation, rhs in zip(
                [self.top_explanation, self.bottom_explanation],
                [self.top_conditional_rhs, self.bottom_conditional_rhs],
            )
        ])

        new_conditionals = [
            (0.91, 0.4),
            (0.83, 0.1),
            (0.99, 0.2),
            (0.97, 0.3),
        ]

        self.play(*list(map(ShowCreation, rects)))
        self.play(FadeOut(rects))
        for i, value in enumerate(it.chain(*new_conditionals)):
            self.play(
                randy.look_at, rects[i%2],
                *self.get_conditional_change_anims(i%2, value)
            )
            if i%2 == 1:
                self.wait()
        self.play(FadeOut(randy))

    def show_restricted_space(self):
        high_bet_space, low_bet_space = [
            VGroup(*[
                self.sample_space.horizontal_parts[i].vertical_parts[j]
                for i in range(2)
            ])
            for j in range(2)
        ]
        words = OldTex("P(", self.cash_string, ")")
        words.set_color_by_tex(self.cash_string, GREEN)
        words.next_to(self.sample_space, RIGHT)
        low_bet_space.generate_target()
        for submob in low_bet_space.target:
            submob.set_color(average_color(
                submob.get_color(), *[BLACK]*4
            ))
        arrows = VGroup(*[
            Arrow(
                words.get_left(),
                submob.get_edge_center(vect),
                color = submob.get_color()
            )
            for submob, vect in zip(high_bet_space, [DOWN, RIGHT])
        ])

        self.play(MoveToTarget(low_bet_space))
        self.play(
            Write(words),
            *list(map(ShowCreation, arrows))
        )
        self.wait()
        for rect in high_bet_space:
            self.play(Indicate(rect, scale_factor = 1))
        self.play(*list(map(FadeOut, [words, arrows])))

        self.high_bet_space = high_bet_space

    def write_P_flush_given_bet(self):
        posterior_tex = OldTex(
            "P(", self.double_heart_template, 
            "|", self.cash_string, ")"
        )
        posterior_tex.scale(0.7)
        posterior_tex.set_color_by_tex(self.cash_string, GREEN)
        self.insert_double_heart(posterior_tex)
        rects = self.high_bet_space.copy()
        rects = [rects[0].copy()] + list(rects)
        for rect in rects:
            rect.generate_target()
        numerator = rects[0].target
        plus = OldTex("+")
        denominator = VGroup(rects[1].target, plus, rects[2].target)
        denominator.arrange(RIGHT, buff = SMALL_BUFF)
        frac_line = OldTex("\\over")
        frac_line.stretch_to_fit_width(denominator.get_width())
        fraction = VGroup(numerator, frac_line, denominator)
        fraction.arrange(DOWN)

        arrow = OldTex("\\downarrow")
        group = VGroup(posterior_tex, arrow, fraction)
        group.arrange(DOWN)
        group.to_corner(UP+RIGHT)

        self.play(LaggedStartMap(FadeIn, posterior_tex))
        self.play(Write(arrow))
        self.play(MoveToTarget(rects[0]))
        self.wait()
        self.play(*it.chain(
            list(map(Write, [frac_line, plus])),
            list(map(MoveToTarget, rects[1:]))
        ))
        self.wait(3)
        self.play(*list(map(FadeOut, [arrow, fraction] + rects)))

        self.posterior_tex = posterior_tex

    def reshape_rectangles(self):
        post_rects = self.get_posterior_rectangles()
        prior_rects = self.get_prior_rectangles()
        braces, labels = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [self.posterior_tex.copy()]
        )
        height_rect = SurroundingRectangle(braces)

        self.play(
            ReplacementTransform(
                prior_rects.copy(), post_rects,
                run_time = 2,
            ),
        )
        self.wait(2)
        self.play(ReplacementTransform(self.posterior_tex, labels[0]))
        self.posterior_tex = labels[0]
        self.play(GrowFromCenter(braces))
        self.wait()
        self.play(ShowCreation(height_rect))
        self.play(FadeOut(height_rect))
        self.wait()

        self.post_rects = post_rects

    def compare_prior_to_posterior(self):
        prior_tex = self.sample_space.horizontal_parts.labels[0]
        post_tex = self.posterior_tex
        prior_rect, post_rect = [
            SurroundingRectangle(tex, stroke_width = 2)
            for tex in [prior_tex, post_tex]
        ]

        post_words = OldTexText("Posterior", "probability")
        post_words.scale(0.8)
        post_words.to_corner(UP+RIGHT)
        post_arrow = Arrow(
            post_words[0].get_bottom(), post_tex.get_top(),
            color = WHITE
        )

        self.play(ShowCreation(prior_rect))
        self.wait()
        self.play(ReplacementTransform(prior_rect, post_rect))
        self.wait()
        self.play(FadeOut(post_rect))
        self.play(Indicate(post_tex.get_part_by_tex(self.cash_string)))
        self.wait()
        self.play(
            Write(post_words),
            ShowCreation(post_arrow)
        )
        self.wait()
        self.play(post_words[1].fade, 0.8)
        self.wait(2)
        self.play(*list(map(FadeOut, [post_words, post_arrow])))

    def preview_tweaks(self):
        post_rects = self.post_rects
        new_value_lists = [
            (0.85, 0.1, 0.11),
            (0.97, 0.3, 1./22),
        ]
        for new_values in new_value_lists:
            for i, value in zip(list(range(2)), new_values):
                self.play(*self.get_conditional_change_anims(
                    i, value, post_rects
                ))
            self.play(*self.get_prior_change_anims(
                new_values[-1], post_rects
            ))
        self.wait(2)

    def tweak_non_flush_case(self):
        her = self.her
        her.scale(0.7)
        her.change_mode("plain")
        her.shift(DOWN)
        her.glasses = SunGlasses(her)
        post_rects = self.post_rects
        posterior = VGroup(post_rects.braces, post_rects.labels)
        prior_rects = self.get_prior_rectangles()
        risk_averse_words = OldTexText(
            "Suppose risk \\\\ averse \\dots"
        )
        risk_averse_words.scale(0.7)
        risk_averse_words.next_to(her, DOWN)
        risk_averse_words.shift_onto_screen()

        arrows = VGroup(*[
            Arrow(ORIGIN, LEFT, tip_length = SMALL_BUFF)
            for x in range(3)
        ])
        arrows.arrange(DOWN)
        arrows.next_to(prior_rects[1], RIGHT, SMALL_BUFF)

        self.wait(2)
        self.play(*list(map(FadeIn, [her, her.glasses])))
        self.play(LaggedStartMap(FadeIn, risk_averse_words))
        self.play(her.change_mode, "sad", Animation(her.glasses))
        self.wait()
        self.play(ShowCreation(arrows))
        self.play(
            *it.chain(
                self.get_conditional_change_anims(1, 0.1, post_rects),
                [Animation(arrows)]
            ),
            run_time = 3
        )
        self.play(FadeOut(arrows))
        self.wait(2)
        post_surrounding_rect = SurroundingRectangle(posterior)
        self.play(ShowCreation(post_surrounding_rect))
        self.play(FadeOut(post_surrounding_rect))
        self.wait()
        self.play(
            FadeOut(risk_averse_words),
            *self.get_conditional_change_anims(1, 0.3, post_rects),
            run_time = 2
        )

    def tweak_flush_case(self):
        her = self.her
        post_rects = self.post_rects

        self.play(
            her.change_mode, "erm", Animation(her.glasses)
        )
        self.play(
            *self.get_conditional_change_anims(0, 0.47, post_rects),
            run_time = 3
        )
        self.wait(3)
        self.play(*self.get_conditional_change_anims(
            0, 0.97, post_rects
        ))
        self.wait()

    def tweak_prior(self):
        her = self.her
        post_rects = self.post_rects

        self.play(
            her.change_mode, "happy", Animation(her.glasses)
        )
        self.play(
            *self.get_prior_change_anims(0.3, post_rects),
            run_time = 2
        )
        self.wait(3)
        self.play(
            *self.get_prior_change_anims(1./22, post_rects),
            run_time = 2
        )
        self.play(*list(map(FadeOut, [her, her.glasses])))

    def compute_posterior(self):
        prior_rects = self.get_prior_rectangles()
        post_tex = self.posterior_tex
        prior_rhs_group = self.get_prior_rhs_group()

        fraction = OldTex(
            "{(0.045)", "(0.97)", "\\over", 
            "(0.995)", "(0.3)", "+", "(0.045)", "(0.97)}"
        )
        products = [
            VGroup(*[
                fraction.get_parts_by_tex(tex)[i]
                for tex in tex_list
            ])
            for i, tex_list in [
                (0, ["0.045", "0.97"]),
                (0, ["0.995", "0.3"]),
                (1, ["0.045", "0.97"]),
            ]
        ]
        for i in 0, 2:
            products[i].set_color(prior_rects[0].get_color())
        products[1].set_color(prior_rects[1].get_color())
        fraction.scale(0.65)
        fraction.to_corner(UP+RIGHT, buff = MED_SMALL_BUFF)
        arrow_kwargs = {
            "color" : WHITE,
            "tip_length" : 0.15,
        }
        rhs = OldTex("\\approx", "0.13")
        rhs.scale(0.8)
        rhs.next_to(post_tex, RIGHT)
        to_rhs_arrow = Arrow(
            fraction.get_bottom(), rhs.get_top(),
            **arrow_kwargs
        )

        pre_top_rect_products = VGroup(
            prior_rhs_group[0], self.top_conditional_rhs
        )
        pre_bottom_rect_products = VGroup(
            prior_rhs_group[1], self.bottom_conditional_rhs
        )

        self.play(Indicate(prior_rects[0], scale_factor = 1))
        self.play(*[
            ReplacementTransform(
                mob.copy(), term,
                run_time = 2,
            )
            for mob, term in zip(
                pre_top_rect_products, products[0]
            )
        ])
        self.play(Write(fraction.get_part_by_tex("over")))
        for pair in zip(pre_top_rect_products, products[0]):
            self.play(*list(map(Indicate, pair)))
            self.wait()
        self.wait()
        self.play(Indicate(prior_rects[1], scale_factor = 1))
        self.play(*[
            ReplacementTransform(
                mob.copy(), term,
                run_time = 2,
            )
            for mob, term in zip(
                pre_bottom_rect_products, products[1]
            )
        ])
        self.wait()
        for pair in zip(pre_bottom_rect_products, products[1]):
            self.play(*list(map(Indicate, pair)))
            self.wait()
        self.play(
            Write(fraction.get_part_by_tex("+")),
            ReplacementTransform(products[0].copy(), products[2])
        )
        self.wait()
        self.play(ShowCreation(to_rhs_arrow))
        self.play(Write(rhs))
        self.wait(3)


    ######

    def get_prior_labels(self, value):
        p_str = "%0.3f"%value
        q_str = "%0.3f"%(1-value)
        labels = [
            OldTex(
                "P(", s, self.double_heart_template, ")",
                "= ", num
            )
            for s, num in (("", p_str), ("\\text{not }", q_str))
        ]
        for label in labels:
            label.scale(0.7)
            self.insert_double_heart(label)

        return labels

    def get_prior_rhs_group(self):
        labels = self.sample_space.horizontal_parts.labels
        return VGroup(*[label[-1] for label in labels])

    def get_conditional_label(self, value, given_flush = True):
        label = OldTex(
            "P(", self.cash_string, "|", 
            "" if given_flush else "\\text{not }",
            self.double_heart_template, ")",
            "=", str(value)
        )
        self.insert_double_heart(label)
        label.set_color_by_tex(self.cash_string, GREEN)
        label.scale(0.7)
        return label

    def insert_double_heart(self, tex_mob):
        double_heart = SuitSymbol("hearts")
        double_heart.add(SuitSymbol("hearts"))
        double_heart.arrange(RIGHT, buff = SMALL_BUFF)
        double_heart.get_tex = lambda : self.double_heart_template
        template = tex_mob.get_part_by_tex(self.double_heart_template)
        double_heart.replace(template)
        tex_mob.submobjects[tex_mob.index_of_part(template)] = double_heart
        return tex_mob

    def get_prior_change_anims(self, value, post_rects = None):
        space = self.sample_space
        parts = space.horizontal_parts
        anims = self.get_horizontal_division_change_animations(
            value, new_label_kwargs = {
                "labels" : self.get_prior_labels(value)
            }
        )
        if post_rects is not None:
            anims += self.get_posterior_rectangle_change_anims(post_rects)
        return anims

    def get_conditional_change_anims(
        self, sub_sample_space_index, value,
        post_rects = None
        ):
        given_flush = (sub_sample_space_index == 0)
        label = self.get_conditional_label(value, given_flush)
        return SampleSpaceScene.get_conditional_change_anims(
            self, sub_sample_space_index, value, post_rects,
            new_label_kwargs = {"labels" : [label]},
        )
