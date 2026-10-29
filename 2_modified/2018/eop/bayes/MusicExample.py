# ==============================================================================
# Scene:      MusicExample
# Source:     videos/_2018/eop/bayes.py (lines 1542-2068)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MusicExample.py MusicExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - removed path_arc kwarg from LaggedStartMap(MoveAlongPath...) (Cairo ignored it, GL rejects it)
# ==============================================================================

from manim_imports_ext import *

class MusicExample(SampleSpaceScene, PiCreatureScene):
    def construct(self):
        self.introduce_musician()
        self.add_prior()
        self.record_track()
        self.add_bottom_conditionl()
        self.friend_gives_compliment()
        self.friends_dont_like()
        self.false_compliment()
        self.add_top_conditionl()
        self.get_positive_review()
        self.restrict_space()
        self.show_posterior_rectangles()
        self.show_prior_rectangle_areas()
        self.show_posterior_probability()
        self.intuition_of_positive_feedback()
        self.make_friends_honest()
        self.fade_out_post_rect()
        self.get_negative_feedback()
        self.compare_prior_to_post_given_negative()
        self.intuition_of_negative_feedback()

    def introduce_musician(self):
        randy = self.pi_creature
        randy.change_mode("soulful_musician")
        randy.arms = randy.get_arm_copies()
        guitar = randy.guitar = Guitar()
        guitar.move_to(randy)
        guitar.shift(0.31*RIGHT + 0.6*UP)

        randy.change_mode("plain")
        self.play(
            randy.change_mode, "soulful_musician",
            path_arc = np.pi/6,
        )
        self.play(
            Animation(randy),
            DrawBorderThenFill(guitar),
            Animation(randy.arms)
        )
        randy.add(guitar, randy.arms)
        self.wait()
        self.play_notes(guitar)
        self.change_pi_creature_with_guitar("concerned_musician")
        self.wait(2)
        self.play(
            randy.scale, 0.7,
            randy.to_corner, UP+LEFT,
        )
        self.play_notes(guitar)

    def add_prior(self):
        sample_space = SampleSpace()
        sample_space.shift(DOWN)
        sample_space.divide_horizontally(0.8, colors = [MAROON_D, BLUE_E])
        labels = VGroup(
            OldTex("P(S) = ", "0.8"),
            OldTex("P(\\text{not } S) = ", "0.2"),
        )
        labels.scale(0.7)
        braces, labels = sample_space.get_side_braces_and_labels(labels)
        VGroup(sample_space, braces, labels).to_edge(LEFT)
        words = list(map(TexText, [
            "Blunt honesty", "Some confidence"
        ]))
        for word, part in zip(words, sample_space.horizontal_parts):
            word.scale(0.6)
            word.move_to(part)

        self.play(LaggedStartMap(FadeIn, sample_space, run_time = 1))
        self.play(*list(map(GrowFromCenter, braces)))
        for label in labels:
            self.play(Write(label, run_time = 2))
            self.wait()
        for word, mode in zip(words, ["maybe", "soulful_musician"]):
            self.play(LaggedStartMap(FadeIn, word, run_time = 1))
            self.change_pi_creature_with_guitar(mode)
            self.wait()
        self.wait()
        self.play(*list(map(FadeOut, words)))

        self.sample_space = sample_space

    def record_track(self):
        randy = self.pi_creature
        friends = VGroup(*[
            PiCreature(mode = "happy", color = color).flip()
            for color in (BLUE_B, GREY_BROWN, MAROON_E)
        ])
        friends.scale(0.6)
        friends.arrange(RIGHT)
        friends.next_to(randy, RIGHT, LARGE_BUFF, DOWN)
        friends.to_edge(RIGHT)
        for friend in friends:
            friend.look_at(randy.eyes)

        headphones = VGroup(*list(map(Headphones, friends)))

        self.play(FadeIn(friends))
        self.pi_creatures.add(*friends)
        self.play(
            FadeIn(headphones), 
            Animation(friends)
        )
        self.play_notes(randy.guitar)
        self.play(LaggedStartMap(
            ApplyMethod, friends,
            lambda pi : (pi.change, "hooray"),
            run_time = 2,
        ))

        self.friends = friends
        self.headphones = headphones

    def add_bottom_conditionl(self):
        p = 0.99
        bottom_part = self.sample_space[1]
        bottom_part.divide_vertically(p, colors = [GREEN_E, YELLOW])
        label = self.get_conditional_label(p, False)
        braces, labels = bottom_part.get_bottom_braces_and_labels([label])
        brace = braces[0]

        self.play(FadeIn(bottom_part.vertical_parts))
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        self.wait()

    def friend_gives_compliment(self):
        friends = self.friends
        bubble = SpeechBubble(
            height = 1.25, width = 3, direction = RIGHT,
            fill_opacity = 0,
        )
        content = OldTexText("Phenomenal!")
        content.scale(0.75)
        bubble.add_content(content)
        VGroup(bubble, content).next_to(friends, LEFT, SMALL_BUFF)
        VGroup(bubble, content).to_edge(UP, SMALL_BUFF)
    
        self.play(LaggedStartMap(
            ApplyMethod, friends,
            lambda pi : (pi.change_mode, "conniving")
        ))
        self.wait()
        self.play(
            ShowCreation(bubble),
            Write(bubble.content, run_time = 1),
            ApplyMethod(friends[0].change_mode, "hooray"),
            LaggedStartMap(
                ApplyMethod, VGroup(*friends[1:]),
                lambda pi : (pi.change_mode, "happy")
            ),
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [bubble, content])))

    def friends_dont_like(self):
        friends = self.friends
        pi1, pi2, pi3 = friends
        for friend in friends:
            friend.generate_target()
        pi1.target.change("guilty", pi2.eyes)
        pi2.target.change("hesitant", pi1.eyes)
        pi3.target.change("pondering", pi2.eyes)

        self.play(LaggedStartMap(
            MoveToTarget, friends
        ))
        self.change_pi_creature_with_guitar("concerned_musician")
        self.wait()

    def false_compliment(self):
        friend = self.friends[0]
        bubble = SpeechBubble(
            height = 1.25, width = 4.5, direction = RIGHT,
            fill_opacity = 0,
        )
        content = OldTexText("The beat was consistent.")
        content.scale(0.75)
        bubble.add_content(content)
        VGroup(bubble, content).next_to(friend, LEFT, SMALL_BUFF)
        VGroup(bubble, content).to_edge(UP, SMALL_BUFF)

        self.play(
            friend.change_mode, "maybe",
            ShowCreation(bubble),
            Write(content)
        )
        self.change_pi_creature_with_guitar("happy")
        self.wait()
        self.play(*list(map(FadeOut, [bubble, content])))

        self.bubble = bubble

    def add_top_conditionl(self):
        p = 0.9
        top_part = self.sample_space[0]
        top_part.divide_vertically(p, colors = [TEAL_E, RED_E])
        label = self.get_conditional_label(p, True)
        braces, labels = top_part.get_top_braces_and_labels([label])
        brace = braces[0]

        self.play(FadeIn(top_part.vertical_parts))
        self.play(GrowFromCenter(brace))
        self.play(Write(label, run_time = 2))
        self.wait()

    def get_positive_review(self):
        friends = self.friends

        self.change_pi_creature_with_guitar(
            "soulful_musician",
            LaggedStartMap(
                ApplyMethod, friends, 
                lambda pi : (pi.change, "happy"),
                run_time = 1,
            )
        )
        self.play_notes(self.pi_creature.guitar)

    def restrict_space(self):
        positive_space, negative_space = [
            VGroup(*[
                self.sample_space[i][j]
                for i in range(2)
            ])
            for j in range(2)
        ]
        negative_space.save_state()

        self.play(negative_space.fade, 0.8)
        self.play(LaggedStartMap(
            ApplyMethod, positive_space,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back,
            run_time = 2,
            lag_ratio = 0.7,
        ))
        self.wait()

        self.negative_space = negative_space

    def show_posterior_rectangles(self):
        prior_rects = self.get_prior_rectangles()
        post_rects = self.get_posterior_rectangles()
        label = OldTex("P(S | ", "\\checkmark", ")")
        label.scale(0.7)
        label.set_color_by_tex("\\checkmark", GREEN)
        braces, labels = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [label]
        )
        brace = braces[0]

        self.play(ReplacementTransform(
            prior_rects.copy(), post_rects,
            run_time = 2
        ))
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        self.wait()

        self.post_rects = post_rects
        self.post_tex = label

    def show_prior_rectangle_areas(self):
        prior_rects = self.get_prior_rectangles()
        products = VGroup(
            OldTex("(", "0.8", ")(", "0.9", ")"),
            OldTex("(", "0.2", ")(", "0.99", ")"),
        )
        top_product, bottom_product = products
        for product, rect in zip(products, prior_rects):
            product.scale(0.7)
            product.move_to(rect)
        side_labels = self.sample_space.horizontal_parts.labels
        top_labels = self.sample_space[0].vertical_parts.labels
        bottom_labels = self.sample_space[1].vertical_parts.labels

        self.play(
            ReplacementTransform(
                side_labels[0][-1].copy(),
                top_product[1],
            ),
            ReplacementTransform(
                top_labels[0][-1].copy(),
                top_product[3],
            ),
            Write(VGroup(*top_product[::2]))
        )
        self.wait(2)
        self.play(
            ReplacementTransform(
                side_labels[1][-1].copy(),
                bottom_product[1],
            ),
            ReplacementTransform(
                bottom_labels[0][-1].copy(),
                bottom_product[3],
            ),
            Write(VGroup(*bottom_product[::2]))
        )
        self.wait(2)

        self.products = products

    def show_posterior_probability(self):
        post_tex = self.post_tex
        rhs = OldTex("\\approx", "0.78")
        rhs.scale(0.7)
        rhs.next_to(post_tex, RIGHT)
        ratio = OldTex(
            "{(0.8)(0.9)", "\\over", 
            "(0.8)(0.9)", "+", "(0.2)(0.99)}"
        )
        ratio.scale(0.6)
        ratio.next_to(VGroup(post_tex, rhs), DOWN, LARGE_BUFF)
        ratio.to_edge(RIGHT)
        arrow_kwargs = {
            "tip_length" : 0.15, 
            "color" : WHITE,
            "buff" : 2*SMALL_BUFF,
        }
        to_ratio_arrow = Arrow(
            post_tex.get_bottom(), ratio.get_top(), **arrow_kwargs
        )
        to_rhs_arrow = Arrow(
            ratio.get_top(), rhs[1].get_bottom(), **arrow_kwargs
        )

        prior_rects = self.get_prior_rectangles()

        self.play(
            ShowCreation(to_ratio_arrow),
            FadeIn(ratio)
        )
        self.wait(2)
        for mob in prior_rects, prior_rects[0]:
            self.play(
                mob.set_color, YELLOW,
                Animation(self.products),
                rate_func = there_and_back,
                run_time = 2
            )
            self.wait()
        self.wait()
        self.play(ShowCreation(to_rhs_arrow))
        self.play(Write(rhs, run_time = 1))
        self.wait(2)

        self.post_rhs = rhs
        self.ratio_group = VGroup(ratio, to_ratio_arrow, to_rhs_arrow)

    def intuition_of_positive_feedback(self):
        friends = self.friends
        prior_num = self.sample_space.horizontal_parts.labels[0][-1]
        prior_num_ghost = prior_num.copy().set_fill(opacity = 0.5)
        post_num = self.post_rhs[-1]
        prior_rect = SurroundingRectangle(prior_num)
        post_rect = SurroundingRectangle(post_num)

        self.play(ShowCreation(prior_rect))
        self.play(Transform(
            prior_num_ghost, post_num,
            remover = True,
            path_arc = -np.pi/6,
            run_time = 2,
        ))
        self.play(ShowCreation(post_rect))
        self.wait(2)
        for mode, time in ("shruggie", 2), ("hesitant", 0):
            self.play(LaggedStartMap(
                ApplyMethod, friends,
                lambda pi : (pi.change, mode),
                run_time = 2,
            ))
            self.wait(time)
        self.play(*list(map(FadeOut, [
            prior_rect, post_rect,
            self.ratio_group, self.post_rhs
        ])))

        self.prior_num_rect = prior_rect

    def make_friends_honest(self):
        post_rects = self.post_rects

        self.play(FadeOut(self.products))
        for value in 0.5, 0.1, 0.9:
            label = self.get_conditional_label(value)
            self.play(*self.get_top_conditional_change_anims(
                value, post_rects, 
                new_label_kwargs = {"labels" : [label]},
            ), run_time = 2)
            self.wait(2)

    def fade_out_post_rect(self):
        self.play(*list(map(FadeOut, [
            self.post_rects, 
            self.post_rects.braces, 
            self.post_rects.labels, 
        ])))
        self.play(self.negative_space.restore)

    def get_negative_feedback(self):
        friends = self.friends
        old_prior_rects = self.get_prior_rectangles()
        for part in self.sample_space.horizontal_parts:
            part.vertical_parts.submobjects.reverse()
        new_prior_rects = self.get_prior_rectangles()
        post_rects = self.get_posterior_rectangles()
        label = OldTex(
            "P(S | \\text{not } ", "\\checkmark", ")",
            "\\approx", "0.98"
        )
        label.scale(0.7)
        label.set_color_by_tex("\\checkmark", GREEN)
        braces, labels = self.get_posterior_rectangle_braces_and_labels(
            post_rects, [label]
        )
        brace = braces[0]

        self.play(old_prior_rects.fade, 0.8)
        self.play(LaggedStartMap(
            ApplyMethod, friends,
            lambda pi : (pi.change, "pondering", post_rects),
            run_time = 1
        ))
        self.wait()
        self.play(ReplacementTransform(
            new_prior_rects.copy(), post_rects,
            run_time = 2            
        ))
        self.play(GrowFromCenter(brace))
        self.wait(2)
        self.play(Write(label))
        self.wait(3)

        self.post_rects = post_rects

    def compare_prior_to_post_given_negative(self):
        post_num = self.post_rects.labels[0][-1]
        post_num_rect = SurroundingRectangle(post_num)

        self.play(ShowCreation(self.prior_num_rect))
        self.wait()
        self.play(ShowCreation(post_num_rect))
        self.wait()

        self.post_num_rect = post_num_rect

    def intuition_of_negative_feedback(self):
        friends = self.friends
        randy = self.pi_creature
        bubble = self.bubble

        modes = ["sassy", "pleading", "horrified"]
        for friend, mode in zip(friends, modes):
            friend.generate_target()
            friend.target.change(mode, randy.eyes)
        content = OldTexText("Horrible.  Just horrible.")
        content.scale(0.6)
        bubble.add_content(content)

        self.play(*list(map(MoveToTarget, friends)))
        self.play(
            ShowCreation(bubble),
            Write(bubble.content)
        )
        self.change_pi_creature_with_guitar("sad")
        self.wait()
        self.change_pi_creature_with_guitar("concerned_musician")
        self.wait(3)

    ######

    def create_pi_creature(self):
        randy = Randolph()
        randy.left_arm_range = [.36, .45]
        self.randy = randy
        return randy

    def get_conditional_label(self, value, given_suck = True):
        positive_str = "\\checkmark"
        label = OldTex(
            "P(", positive_str, "|", 
            "" if given_suck else "\\text{not }",
            "S", ")",
            "=", str(value)
        )
        label.set_color_by_tex(positive_str, GREEN)
        label.scale(0.7)
        return label

    def change_pi_creature_with_guitar(self, target_mode, *added_anims):
        randy = self.pi_creature
        randy.remove(randy.arms, randy.guitar)
        target = randy.copy()
        target.change_mode(target_mode)
        target.arms = target.get_arm_copies()
        target.guitar = randy.guitar.copy()
        for pi in randy, target:
            pi.add(pi.guitar, pi.arms)
        self.play(Transform(randy, target), *added_anims)

    def play_notes(self, guitar):
        note = SVGMobject(file_name = "8th_note")
        note.set_height(0.5)
        note.set_stroke(width = 0)
        note.set_fill(BLUE, 1)
        note.move_to(guitar)
        note.shift(MED_SMALL_BUFF*(DOWN+2*LEFT))
        notes = VGroup(*[note.copy() for x in range(10)])
        sine_wave = FunctionGraph(np.sin, x_min = -5, x_max = 5)
        sine_wave.scale(0.75)
        sine_wave.rotate(np.pi/6, about_point = ORIGIN)
        sine_wave.shift(
            notes.get_center() - \
            sine_wave.point_from_proportion(0)
        )
        self.play(LaggedStartMap(
            MoveAlongPath, notes, 
            lambda n : (n, sine_wave),
            # CHANGE: path_arc is ignored by MoveAlongPath in Cairo and rejected by GL; removed
            run_time = 4,
            lag_ratio = 0.5,
            rate_func = lambda t : t,
        ))
