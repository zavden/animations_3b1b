# ==============================================================================
# Scene:      Introduction
# Source:     videos/_2018/eop/bayes_footnote.py (lines 18-231)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/eop/bayes.py
#
# Run from this folder:
#     manimgl Introduction.py Introduction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - SuitSymbol.CONFIG["red"] replaced by the Cairo default red #D02028 (GL SuitSymbol has no CONFIG)
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/eop/bayes.py -----

class IntroducePokerHand(PiCreatureScene, SampleSpaceScene):
    CONFIG = {
        "community_cards_center" : 1.5*DOWN,
        "community_card_values" : ["10S", "QH", "AH", "2C", "5H"],
        "your_hand_values" : ["JS", "KC"],
    }
    def construct(self):
        self.add_cards()
        self.indicate_straight()
        self.show_flush_potential()
        self.compute_flush_probability()
        self.show_flush_sample_space()
        self.talk_through_sample_space()
        self.place_high_bet()
        self.change_belief()
        self.move_community_cards_out_of_the_way()
        self.name_bayes_rule()

    def add_cards(self):
        you, her = self.you, self.her
        community_cards = VGroup(*list(map(
            PlayingCard, self.community_card_values
        )))
        community_cards.arrange(RIGHT)
        community_cards.move_to(self.community_cards_center)
        deck = VGroup(*[
            PlayingCard(turned_over = True)
            for x in range(5)
        ])
        for i, card in enumerate(deck):
            card.shift(i*(0.03*RIGHT + 0.015*DOWN))
        deck.next_to(community_cards, LEFT)

        you.hand = self.get_hand(you, self.your_hand_values)
        her.hand = self.get_hand(her, None)
        hand_cards = VGroup(*it.chain(*list(zip(you.hand, her.hand))))

        self.add(deck)
        for group in hand_cards, community_cards:
            for card in group:
                card.generate_target()
                card.scale(0.01)
                card.move_to(deck[-1], UP+RIGHT)
            self.play(LaggedStartMap(MoveToTarget, group, lag_ratio = 0.8))
            self.wait()
        self.wait()

        self.community_cards = community_cards
        self.deck = deck

    def indicate_straight(self):
        you = self.you
        community_cards = self.community_cards
        you.hand.save_state()
        you.hand.generate_target()
        for card in you.hand.target:
            card.set_height(community_cards.get_height())

        selected_community_cards = VGroup(*[card for card in community_cards if card.numerical_value >= 10])
        selected_community_cards.submobjects.sort(
            key=lambda c: c.numerical_value
        )

        selected_community_cards.save_state()
        for card in selected_community_cards:
            card.generate_target()

        straight_cards = VGroup(*it.chain(
            you.hand.target, 
            [c.target for c in selected_community_cards]
        ))
        straight_cards.submobjects.sort(
            key=lambda c: c.numerical_value
        )
        straight_cards.arrange(RIGHT, buff = SMALL_BUFF)
        straight_cards.next_to(community_cards, UP, aligned_edge = LEFT)
        you.hand.target.shift(MED_SMALL_BUFF*UP)

        self.play(LaggedStartMap(
            MoveToTarget,
            selected_community_cards,
            run_time = 1.5
        ))
        self.play(MoveToTarget(you.hand))
        self.play(LaggedStartMap(
            ApplyMethod,
            straight_cards,
            lambda m : (m.set_color, YELLOW),
            rate_func = there_and_back,
            run_time = 1.5,
            lag_ratio = 0.5,
            remover = True,
        ))
        self.play(you.change, "hooray", straight_cards)
        self.wait(2)
        self.play(
            selected_community_cards.restore,
            you.hand.restore,
            you.change_mode, "happy"
        )
        self.wait()

    def show_flush_potential(self):
        you, her = self.you, self.her
        heart_cards = VGroup(*[c for c in self.community_cards if c.suit == "hearts"])
        heart_cards.save_state()

        her.hand.save_state()
        her.hand.generate_target()
        her.hand.target.arrange(RIGHT)
        her.hand.target.next_to(heart_cards, UP)
        her.hand.target.to_edge(UP)

        her.glasses.save_state()
        her.glasses.move_to(her.hand.target)
        her.glasses.set_fill(opacity = 0)

        heart_qs = VGroup()
        hearts = VGroup()
        q_marks = VGroup()
        for target in her.hand.target:
            heart = SuitSymbol("hearts")
            q_mark = OldTex("?")
            heart_q = VGroup(heart, q_mark)
            for mob in heart_q:
                mob.set_height(0.5)
            heart_q.arrange(RIGHT, buff = SMALL_BUFF)
            heart_q.move_to(target)
            heart_qs.add(heart, q_mark)
            hearts.add(heart)
            q_marks.add(q_mark)

        self.play(heart_cards.shift, heart_cards.get_height()*UP)
        self.play(you.change_mode, "hesitant")
        self.play(MoveToTarget(her.hand))
        self.play(LaggedStartMap(DrawBorderThenFill, heart_qs))
        self.play(
            her.change, "happy",
            her.glasses.restore,
        )
        self.pi_creatures.remove(her)
        new_suit_pairs = [
            ("clubs", "diamonds"),
            ("diamonds", "spades"),
            ("spades", "clubs"),
            ("hearts", "hearts"),
        ]
        for new_suit_pair in new_suit_pairs:
            new_symbols = VGroup(*list(map(SuitSymbol, new_suit_pair)))
            for new_symbol, heart in zip(new_symbols, hearts):
                new_symbol.replace(heart, dim_to_match = 1)
            self.play(Transform(
                hearts, new_symbols,
                lag_ratio = 0.5
            ))
            self.wait()
        self.play(FadeOut(heart_qs))
        self.play(
            heart_cards.restore,
            her.hand.restore,
            you.change_mode, "pondering",
        )

        self.q_marks = q_marks

    def compute_flush_probability(self):
        you, her = self.you, self.her
        equation = OldTex(
            "{ {10 \\choose 2}", "\\over", "{45 \\choose 2} }", 
            "=", "{45 \\over 990}", "\\approx", "4.5\\%"
        )
        equation.next_to(self.community_cards, UP, buff = LARGE_BUFF)
        percentage = equation.get_part_by_tex("4.5")

        ten = VGroup(*equation[0][1:3])
        num_hearts = OldTexText("\\# Remaining hearts")
        num_hearts.scale(0.75)
        num_hearts.next_to(
            ten, UP, aligned_edge = LEFT
        )
        num_hearts.to_edge(UP)
        num_hearts.set_color(RED)
        num_hearts_arrow = Arrow(
            num_hearts.get_bottom(), ten.get_right(),
            color = RED, buff = SMALL_BUFF
        )

        fourty_five = VGroup(*equation[2][1:3])
        num_cards = OldTexText("\\# Remaining cards")
        num_cards.scale(0.75)
        num_cards.next_to(fourty_five, LEFT)
        num_cards.to_edge(LEFT)
        num_cards.set_color(BLUE)
        num_cards_arrow = Arrow(
            num_cards, fourty_five,
            color = BLUE, buff = SMALL_BUFF
        )

        self.play(LaggedStartMap(FadeIn, equation))
        self.wait(2)
        self.play(
            FadeIn(num_hearts), 
            ShowCreation(num_hearts_arrow),
            ten.set_color, RED,
        )
        self.play(
            FadeIn(num_cards), 
            ShowCreation(num_cards_arrow),
            fourty_five.set_color, BLUE
        )
        self.wait(3)
        equation.remove(percentage)
        self.play(*list(map(FadeOut, [
            equation, 
            num_hearts, num_hearts_arrow,
            num_cards, num_cards_arrow,
        ])))


        self.percentage = percentage

    def show_flush_sample_space(self):
        you, her = self.you, self.her
        percentage = self.percentage

        sample_space = self.get_sample_space()
        sample_space.add_title("Your belief")
        sample_space.move_to(VGroup(you.hand, her.hand))
        sample_space.to_edge(UP, buff = MED_SMALL_BUFF)
        p = 1./22
        sample_space.divide_horizontally(
            # CHANGE: GL SuitSymbol has no CONFIG dict; use the Cairo default red value (#D02028)
            p, colors = ["#D02028", BLUE_E]
        )
        braces, labels = sample_space.get_side_braces_and_labels([
            percentage.get_tex(), "95.5\\%"
        ])
        top_label, bottom_label = labels

        self.play(
            FadeIn(sample_space),
            ReplacementTransform(percentage, top_label)
        )
        self.play(*list(map(GrowFromCenter, [
            brace for brace in braces
        ])))
        self.wait(2)
        self.play(Write(bottom_label))
        self.wait(2)

        self.sample_space = sample_space

    def talk_through_sample_space(self):
        her = self.her
        sample_space = self.sample_space
        top_part, bottom_part = self.sample_space.horizontal_parts

        flush_hands, non_flush_hands = hand_lists = [
            [self.get_hand(her, keys) for keys in key_list]
            for key_list in [
                [("3H", "8H"), ("4H", "5H"), ("JH", "KH")],
                [("AC", "6D"), ("3D", "6S"), ("JH", "4C")],
            ]
        ]   
        for hand_list, part in zip(hand_lists, [top_part, bottom_part]):
            self.play(Indicate(part, scale_factor = 1))
            for hand in hand_list:
                hand.save_state()
                hand.scale(0.01)
                hand.move_to(part.get_right())
                self.play(hand.restore)
            self.wait()
        self.wait()
        self.play(*list(map(FadeOut, it.chain(*hand_lists))))

    def place_high_bet(self):
        you, her = self.you, self.her
        pre_money = VGroup(*[
            VGroup(*[
                OldTex("\\$")
                for x in range(10)
            ]).arrange(RIGHT, buff = SMALL_BUFF)
            for y in range(4)
        ]).arrange(UP, buff = SMALL_BUFF)
        money = VGroup(*it.chain(*pre_money))
        money.set_color(GREEN)
        money.scale(0.8)
        money.next_to(her.hand, DOWN)
        for dollar in money:
            dollar.save_state()
            dollar.scale(0.01)
            dollar.move_to(her.get_boundary_point(RIGHT))
            dollar.set_fill(opacity = 0)

        self.play(LaggedStartMap(
            ApplyMethod,
            money,
            lambda m : (m.restore,),
            run_time = 5,
        ))
        self.play(you.change_mode, "confused")
        self.wait()

        self.money = money

    def change_belief(self):
        numbers = self.sample_space.horizontal_parts.labels
        rect = Rectangle(stroke_width = 0)
        rect.set_fill(BLACK, 1)
        rect.stretch_to_fit_width(numbers.get_width())
        rect.stretch_to_fit_height(self.sample_space.get_height())
        rect.move_to(numbers, UP)

        self.play(FadeIn(rect))
        anims = self.get_horizontal_division_change_animations(0.2)
        anims.append(Animation(rect))
        self.play(
            *anims,
            run_time = 3,
            rate_func = there_and_back
        )
        self.play(FadeOut(rect))

    def move_community_cards_out_of_the_way(self):
        cards = self.community_cards
        cards.generate_target()
        cards.target.arrange(
            RIGHT, buff = -cards[0].get_width() + MED_SMALL_BUFF,
        )
        cards.target.move_to(self.deck)
        cards.target.to_edge(LEFT)

        self.sample_space.add_braces_and_labels()

        self.play(
            self.deck.scale, 0.7,
            self.deck.next_to, cards.target, UP,
            self.deck.to_edge, LEFT,
            self.sample_space.shift, 3*DOWN,
            MoveToTarget(cards)
        )

    def name_bayes_rule(self):
        title = OldTexText("Bayes' rule")
        title.set_color(BLUE)
        title.to_edge(UP)
        subtitle = OldTexText("Update ", "prior ", "beliefs")
        subtitle.scale(0.8)
        subtitle.next_to(title, DOWN)
        prior_word = subtitle.get_part_by_tex("prior")
        numbers = self.sample_space.horizontal_parts.labels
        rect = SurroundingRectangle(numbers, color = GREEN)
        arrow = Arrow(prior_word.get_bottom(), rect.get_top())
        arrow.set_color(GREEN)

        words = OldTexText(
            "Maybe she really \\\\ does have a flush $\\dots$",
            alignment = ""
        )
        words.scale(0.7)
        words.next_to(self.money, DOWN, aligned_edge = LEFT)

        self.play(
            Write(title, run_time = 2),
            self.you.change_mode, "pondering"
        )
        self.wait()
        self.play(FadeIn(subtitle))
        self.play(prior_word.set_color, GREEN)
        self.play(
            ShowCreation(rect),
            ShowCreation(arrow)
        )
        self.wait(3)
        self.play(Write(words))
        self.wait(3)


    ######

    def create_pi_creatures(self):
        shift_val = 3
        you = PiCreature(color = BLUE_D)
        her = PiCreature(color = BLUE_B).flip()
        for pi in you, her:
            pi.scale(0.5)
        you.to_corner(UP+LEFT)
        her.to_corner(UP+RIGHT)
        you.make_eye_contact(her)

        glasses = SunGlasses(her)
        her.glasses = glasses

        self.you = you
        self.her = her
        return VGroup(you, her)

    def get_hand(self, pi_creature, keys = None):
        if keys is not None:
            hand = VGroup(*list(map(PlayingCard, keys)))
        else:
            hand = VGroup(*[
                PlayingCard(turned_over = True)
                for x in range(2)
            ])
        hand.scale(0.7)
        card1, card2 = hand
        vect = np.sign(pi_creature.get_center()[0])*LEFT
        card2.move_to(card1)
        card2.shift(MED_SMALL_BUFF*RIGHT + SMALL_BUFF*DOWN)
        hand.next_to(
            pi_creature, vect, 
            buff = MED_LARGE_BUFF,
            aligned_edge = UP
        )
        return hand



# ----- From _2018/eop/bayes_footnote.py -----

SICKLY_GREEN = "#9BBD37"


class Introduction(TeacherStudentsScene):
    def construct(self):
        self.hold_up_example()
        self.write_counter_intuitive()
        self.comment_on_crazy_results()
        self.put_it_first()
        self.swap_example_order()
        self.other_culprit()

    def hold_up_example(self):
        everyone = self.get_pi_creatures()
        self.teacher.change_mode("raise_right_hand")
        rect = ScreenRectangle()
        rect.set_stroke(YELLOW, 2)
        rect.to_edge(UP)
        randy = Randolph()
        randy.scale(0.7)
        name = OldTexText(r"""
            Bayes' theorem \\
            disease example
        """)
        name.next_to(rect.get_top(), DOWN, SMALL_BUFF)
        randy.next_to(name, DOWN)
        example = VGroup(rect, name, randy)

        self.remove(everyone)
        self.add(name, randy)
        self.play(
            randy.change_mode, "sick",
            randy.set_color, SICKLY_GREEN
        )
        self.play(ShowCreation(rect))
        self.play(
            FadeIn(everyone),
            example.scale, 0.5,
            example.next_to, self.teacher.get_corner(UP+LEFT), UP,
        )
        self.wait(2)

        self.example = example

    def write_counter_intuitive(self):
        bayes = OldTexText("Bayes")
        arrow = OldTex("\\leftrightarrow")
        intuition = OldTexText("Intuition")

        group = VGroup(bayes, arrow, intuition)
        group.arrange(RIGHT, buff = SMALL_BUFF)
        group.scale(0.8)
        group.next_to(self.example, UP, buff = SMALL_BUFF)
        group.shift_onto_screen()
        cross = VGroup(
            Line(UP+LEFT, DOWN+RIGHT),
            Line(UP+RIGHT, DOWN+LEFT),
        )
        cross.replace(arrow, stretch = True)
        cross.set_stroke(RED, 6)
        group.add(cross)

        self.play(*list(map(FadeIn, [bayes, intuition])))
        self.play(Write(arrow))
        self.play(ShowCreation(cross))
        self.play_student_changes(*["confused"]*3)
        self.wait(2)

        self.bayes_to_intuition = group

    def comment_on_crazy_results(self):
        disease_group = VGroup(self.example, self.bayes_to_intuition)
        disease_group.save_state()

        self.teacher_says(
            "Who doesn't love \\\\ crazy results?",
            target_mode = "hooray",
            added_anims = [disease_group.to_corner, UP+LEFT]
        )
        self.wait(2)

        self.disease_group = disease_group

    def put_it_first(self):
        poker_example = self.get_poker_example()
        music_example = self.get_music_example()
        disease_group = self.disease_group

        self.play(
            disease_group.restore,
            disease_group.to_edge, LEFT,
            RemovePiCreatureBubble(
                self.teacher,
                target_mode = "hesitant"
            )
        )
        self.play_student_changes(
            *["pondering"]*3, 
            look_at = disease_group
        )

        poker_example.next_to(self.example, RIGHT)
        music_example.next_to(poker_example, RIGHT)
        examples = VGroup(poker_example, music_example)
        brace = Brace(examples, UP)
        bayes_to_intuition = VGroup(*list(map(TexText, [
            "Bayes", "$\\leftrightarrow$", "Intuition"
        ])))
        bayes_to_intuition.arrange(RIGHT, buff = SMALL_BUFF)
        bayes_to_intuition.next_to(brace, UP, SMALL_BUFF)
        check = OldTex("\\checkmark")
        check.set_color(GREEN)
        check.next_to(bayes_to_intuition[1], UP, SMALL_BUFF)

        for example in examples:
            self.play(FadeIn(example))
            self.wait()
        self.play(GrowFromCenter(brace))
        self.play(FadeIn(bayes_to_intuition))
        self.play(Write(check))
        self.wait(2)

        self.intuitive_examples = VGroup(
            examples, brace, bayes_to_intuition, check
        )

    def swap_example_order(self):
        intuitive_examples = self.intuitive_examples
        disease_group = VGroup(
            self.example, self.bayes_to_intuition
        )

        self.play(
            disease_group.next_to, 
                self.teacher.get_corner(UP+LEFT), UP,
            disease_group.shift, LEFT,
            intuitive_examples.scale, 0.7,
            intuitive_examples.to_corner, UP+LEFT,
            self.teacher.change_mode, "sassy"
        )

    def other_culprit(self):
        bayes = self.bayes_to_intuition[0]
        something_else = OldTexText("Something else")
        something_else.set_color(YELLOW)
        something_else.set_height(bayes.get_height())
        something_else.move_to(bayes, RIGHT)
        new_group = VGroup(
            something_else, 
            *self.bayes_to_intuition[1:]
        )

        self.play(bayes.to_edge, UP)
        self.play(Write(something_else))
        self.play(new_group.next_to, self.example, UP, SMALL_BUFF)
        self.play_student_changes(
            "erm", "confused", "hesitant",
            added_anims = [self.teacher.change_mode, "happy"]
        )
        self.wait(3)


    #####

    def get_poker_example(self):
        rect = self.get_example_rect()
        values = IntroducePokerHand.CONFIG["community_card_values"]
        community_cards = VGroup(*list(map(PlayingCard, values)))
        community_cards.arrange(RIGHT)
        deck = VGroup(*[
            PlayingCard(turned_over = True)
            for x in range(5)
        ])
        for i, card in enumerate(deck):
            card.shift(i*(0.03*RIGHT + 0.015*DOWN))
        deck.next_to(community_cards, LEFT)
        cards = VGroup(deck, community_cards)
        cards.set_width(rect.get_width() - 2*SMALL_BUFF)
        cards.next_to(rect.get_bottom(), UP, MED_SMALL_BUFF)

        probability = OldTex(
            "P(", "\\text{Flush}", "|", "\\text{High bet}", ")"
        )
        probability.set_color_by_tex("Flush", RED)
        probability.set_color_by_tex("High bet", GREEN)
        probability.scale(0.5)
        probability.next_to(rect.get_top(), DOWN)

        return VGroup(rect, probability, cards)

    def get_music_example(self):
        rect = self.get_example_rect()

        musician = Randolph(mode = "soulful_musician")
        musician.left_arm_range = [.36, .45]
        musician.arms = musician.get_arm_copies()
        guitar = musician.guitar = Guitar()
        guitar.move_to(musician)
        guitar.shift(0.31*RIGHT + 0.6*UP)
        musician.add(guitar, musician.arms)
        musician.set_height(0.7*rect.get_height())
        musician.next_to(rect.get_bottom(), UP, SMALL_BUFF)

        probability = OldTex(
            "P(", "\\text{Suck }", "|", "\\text{ Good review}", ")"
        )
        probability.set_color_by_tex("Suck", RED)
        probability.set_color_by_tex("Good", GREEN)
        probability.scale(0.5)
        probability.next_to(rect.get_top(), DOWN)

        return VGroup(rect, musician, probability)

    def get_example_rect(self):
        rect = self.example[0].copy()
        rect.set_color(WHITE)
        return rect
