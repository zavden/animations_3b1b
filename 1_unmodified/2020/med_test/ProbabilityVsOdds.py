# ==============================================================================
# Scene:      ProbabilityVsOdds
# Source:     videos/_2020/med_test.py (lines 3444-3752)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProbabilityVsOdds.py ProbabilityVsOdds -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProbabilityVsOdds(Scene):
    def construct(self):
        # Show titles and division
        titles = VGroup(
            OldTexText("Probability"),
            OldTexText("Odds"),
        )
        for title, u in zip(titles, [-1, 1]):
            title.scale(1.5)
            title.to_edge(UP)
            title.set_x(FRAME_WIDTH * u / 4)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(FRAME_WIDTH)
        h_line.next_to(titles, DOWN, SMALL_BUFF)
        h_line.set_x(0)

        v_line = Line(UP, DOWN)
        v_line.set_height(FRAME_HEIGHT)
        v_line.center()

        VGroup(h_line, v_line).set_stroke(GREY, 2)

        titles.save_state()
        for title in titles:
            title.set_x(0)
        titles[1].set_opacity(0)

        self.add(titles)
        self.wait()
        self.play(
            Restore(titles),
            ShowCreation(v_line),
        )
        self.play(ShowCreation(h_line))
        self.wait()

        # Function definitions
        def get_people_row(n_all, n_pos=1):
            icon = SVGMobject("person")
            icon.set_fill(GREY)
            icon.set_stroke(WHITE, 1)
            icon.set_height(1)

            people = VGroup(*(icon.copy() for x in range(n_all)))
            people.arrange(RIGHT, buff=SMALL_BUFF)
            people[:n_pos].set_fill(YELLOW)
            return people

        def get_prob_counts(people, n_pos, n_all):
            pos_brace = Brace(people[:n_pos], UP, buff=SMALL_BUFF)
            all_brace = Brace(people, DOWN, buff=SMALL_BUFF)

            pos_label = Integer(n_pos, color=YELLOW)
            all_label = Integer(n_all)

            pos_label.next_to(pos_brace, UP)
            all_label.next_to(all_brace, DOWN)

            return VGroup(
                VGroup(pos_brace, pos_label),
                VGroup(all_brace, all_label),
            )

        def get_odds_counts(people, n_pos, n_neg):
            pos_brace = Brace(people[:n_pos], UP, buff=SMALL_BUFF)
            neg_brace = Brace(people[n_pos:], UP, buff=SMALL_BUFF)

            pos_label = Integer(n_pos, color=YELLOW)
            neg_label = Integer(n_neg, color=GREY_B)

            pos_label.next_to(pos_brace, UP)
            neg_label.next_to(neg_brace, UP)

            return VGroup(
                VGroup(pos_brace, pos_label),
                VGroup(neg_brace, neg_label),
            )

        def get_prob_label(n_pos, n_all):
            result = VGroup(
                Integer(n_pos, color=YELLOW),
                OldTex("/"),
                Integer(n_all),
            )
            result.scale(1.5)
            result.arrange(RIGHT, buff=0.1)
            return result

        def get_odds_label(n_pos, n_neg):
            result = VGroup(
                Integer(n_pos, color=YELLOW),
                OldTex(":"),
                Integer(n_neg, color=GREY_B),
            )
            result.scale(1.5)
            result.arrange(RIGHT, buff=0.2)
            return result

        # Show probability
        people = get_people_row(5)
        people.match_x(titles[0])
        people.shift(DOWN)
        prob_counts = get_prob_counts(people, 1, 5)

        prob = get_prob_label(1, 5)
        prob.next_to(people, UP, MED_LARGE_BUFF)

        self.play(
            FadeIn(people, lag_ratio=0.3),
            Write(prob)
        )
        self.wait()

        self.play(
            prob.shift, 1.5 * UP,
            TransformFromCopy(prob[0], prob_counts[0][1]),
            GrowFromCenter(prob_counts[0][0]),
        )
        self.play(
            TransformFromCopy(prob[2], prob_counts[1][1]),
            GrowFromCenter(prob_counts[1][0]),
        )
        self.wait()

        # Transition to odds
        right_people = people.copy()
        right_people.match_x(titles[1])

        odds = get_odds_label(1, 4)
        odds.match_x(right_people)
        odds.match_y(prob)

        arrow = Arrow(prob.get_right(), odds.get_left(), buff=1)
        arrow.set_thickness(0.1)

        odds_count = get_odds_counts(right_people, 1, 4)

        self.play(
            TransformFromCopy(people, right_people),
            TransformFromCopy(
                odds.copy().replace(prob).set_opacity(0),
                odds
            ),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(
            TransformFromCopy(odds[0], odds_count[0][1]),
            GrowFromCenter(odds_count[0][0]),
        )
        self.play(
            TransformFromCopy(odds[2], odds_count[1][1]),
            GrowFromCenter(odds_count[1][0]),
        )
        self.wait()
        self.play(ShowCreationThenFadeAround(odds[1]))
        self.wait()

        # Other examples
        people.add(prob_counts)
        right_people.add(odds_count)

        def get_example(n_pos, n_all):
            new_prob = OldTex(
                f"{int(100 * n_pos / n_all)}\\%",
                font_size=72
            )
            new_odds = get_odds_label(n_pos, n_all - n_pos)
            new_odds.next_to(new_prob, RIGHT, buff=1.5)
            arrow = Arrow(
                new_prob.get_right(),
                new_odds.get_left(),
                thickness=0.05
            )
            arrow.set_fill(GREY_A)
            example = VGroup(new_prob, arrow, new_odds)
            example.scale(0.5)
            return example

        def generate_example_movement(prob, arrow, odds, example):
            mover = VGroup(prob, arrow.copy(), odds)
            return ReplacementTransform(mover, example)

        def transition_to_new_example(n_pos, n_all, example,
                                      scene=self,
                                      people=people,
                                      right_people=right_people,
                                      prob=prob,
                                      odds=odds,
                                      arrow=arrow
                                      ):

            new_people = get_people_row(n_all, n_pos)
            new_people.set_x(-FRAME_WIDTH / 4)
            new_right_people = new_people.copy()
            new_right_people.set_x(FRAME_WIDTH / 4)

            new_prob = OldTex(
                f"{int(100 * n_pos / n_all)}\\%",
                font_size=72
            )
            new_odds = get_odds_label(n_pos, n_all - n_pos)
            new_prob.move_to(prob)
            new_odds.move_to(odds)

            scene.play(
                generate_example_movement(prob, arrow, odds, example),
                FadeOut(people),
                FadeOut(right_people),
                FadeIn(new_prob),
                FadeIn(new_odds),
                FadeIn(new_people),
                FadeIn(new_right_people),
            )
            return {
                "people": new_people,
                "right_people": new_right_people,
                "prob": new_prob,
                "odds": new_odds,
            }

        examples = VGroup(*(
            get_example(n, k)
            for n, k in [(1, 10), (1, 5), (1, 2), (4, 5), (9, 10)]
        ))
        examples.arrange(UP)
        examples.to_edge(DOWN)

        kw = {}
        for n, k, ei in (1, 2, 1), (1, 10, 2), (4, 5, 0), (9, 10, 3):
            kw = transition_to_new_example(
                n, k, examples[ei], **kw
            )
            self.wait(2)

        self.remove(arrow)
        self.play(
            generate_example_movement(
                kw["prob"], arrow, kw["odds"], examples[4],
            ),
            FadeOut(kw["people"]),
            FadeOut(kw["right_people"]),
        )

        # Show ranges
        left_range = UnitInterval((0, 1, 0.1), width=5)
        left_range.set_y(1.5)
        left_range.match_x(titles[0])

        right_range = NumberLine((0, 5), width=5, include_tip=True)
        right_range.match_y(left_range)
        right_range.match_x(titles[1])
        dots = OldTex("\\dots")
        dots.next_to(right_range, RIGHT)
        right_range.add(dots)
        right_range.add(*(
            right_range.get_tick(
                1 / n,
                right_range.tick_size * (1 / n)**0.5,
            ).set_opacity((1 / n)**0.5)
            for n in range(2, 100)
        ))

        left_range.add_numbers([0, 0.2, 0.5, 0.8, 1])
        right_range.add_numbers()

        left_ticker = ArrowTip(angle=-90 * DEGREES)
        left_ticker.set_fill(BLUE)
        left_ticker.move_to(left_range.n2p(0.5), DOWN)
        right_ticker = left_ticker.copy()
        right_ticker.set_color(RED)
        right_ticker.move_to(right_range.n2p(1), DOWN)

        self.play(
            Write(left_range),
            Write(right_range),
            run_time=1
        )
        self.play(
            FadeIn(left_ticker, shift=DOWN),
            FadeIn(right_ticker, shift=DOWN),
        )

        rect = SurroundingRectangle(examples[0])
        rect.set_opacity(0)

        prob = ValueTracker(0.5)
        left_ticker.add_updater(
            lambda m: m.move_to(left_range.n2p(prob.get_value()), DOWN)
        )
        right_ticker.add_updater(
            lambda m: m.move_to(right_range.n2p(
                prob.get_value() / (1 - prob.get_value())
            ), DOWN)
        )

        for i, p in enumerate([0.1, 0.2, 0.5, 0.8, 0.9]):
            self.play(
                prob.set_value, p,
                rect.become,
                SurroundingRectangle(examples[i]),
            )
            self.wait()
        self.play(
            FadeOut(rect),
            ApplyMethod(prob.set_value, 0.5, run_time=4),
        )
        self.wait()
