# ==============================================================================
# Scene:      DisambiguateFPR
# Source:     videos/_2020/med_test.py (lines 5930-6235)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DisambiguateFPR.py DisambiguateFPR -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DisambiguateFPR(Scene):
    def construct(self):
        # Add title
        title = OldTexText(
            "1\\% False Positive Rate",
            isolate=["F", "P", "R"],
            font_size=72
        )
        title.to_edge(UP)
        title.set_color(GREY_A)
        underline = Underline(title)
        underline.match_color(title)

        morty = Mortimer()
        morty.to_corner(DR)
        morty.look_at(title)

        self.add(title)
        self.play(
            PiCreatureSays(
                morty,
                "It's a confusing term!",
                target_mode="surprised",
                run_time=1,
            )
        )
        self.play(
            Blink(morty),
            ShowCreation(underline),
        )
        self.play(morty.change, "angry")
        self.play(Blink(morty))

        # Draw out grid
        word_grid = VGroup(
            OldTexText("True positives", color=GREEN),
            OldTexText("False negatives", color=RED_E),
            OldTexText("False positives", color=GREEN_D),
            OldTexText("True negatives", color=RED),
        )
        word_box = SurroundingRectangle(word_grid)
        word_box.set_stroke(WHITE, 2)
        word_box.stretch(2, 1)

        word_grid.arrange_in_grid(
            v_buff=1.0,
            h_buff=0.5,
            fill_rows_first=False
        )
        word_grid.move_to(2 * DOWN)

        globals()['word_box'] = word_box
        word_boxes = VGroup(*(
            word_box.copy().move_to(word).match_color(word)
            for word in word_grid
        ))

        group_boxes = VGroup(
            SurroundingRectangle(word_boxes[:2], color=YELLOW),
            SurroundingRectangle(word_boxes[2:], color=GREY_B),
        )
        group_titles = VGroup(
            OldTexText("Have COVID-19", font_size=36),
            OldTexText("Don't have COVID-19", font_size=36),
        )
        for box, gt in zip(group_boxes, group_titles):
            gt.next_to(box, UP)
            gt.match_color(box)

        icon = SVGMobject("person", stroke_width=0, fill_color=GREY_B)
        globals()['icon'] = icon
        with_pop = VGroup(*(icon.copy() for x in range(1)))
        with_pop.set_color(YELLOW)
        without_pop = VGroup(*(icon.copy() for x in range(999)))

        with_pop.set_height(0.5)
        with_pop.move_to(group_boxes[0])
        without_pop.arrange_in_grid(n_rows=20)
        without_pop.replace(group_boxes[1], dim_to_match=1)
        without_pop.scale(0.9)

        self.play(
            ShowCreation(group_boxes, lag_ratio=0.3),
            DrawBorderThenFill(with_pop),
            ShowIncreasingSubsets(without_pop),
            FadeIn(group_titles, lag_ratio=0.3),
            FadeOut(morty),
            FadeOut(morty.bubble),
            FadeOut(morty.bubble.content),
        )
        self.wait()

        arrow = Vector(DOWN)
        arrow.next_to(group_titles[1], UP)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(
            LaggedStartMap(Write, word_grid[2:], lag_ratio=0.9),
            LaggedStartMap(ShowCreation, word_boxes[2:], lag_ratio=0.9),
            without_pop.set_opacity, 0.3,
            run_time=1,
        )
        self.wait()

        # Two reasonable fractions
        tp, fn, fp, tn = (
            word
            for word, box in zip(word_grid, word_boxes)
        )

        def create_fraction(m1, m2, scale_factor=0.75):
            result = VGroup(
                m1.copy(),
                OldTex("\\quad \\over \\quad"),
                m1.copy(),
                OldTex("+"),
                m2.copy()
            )
            result[0::2].scale(scale_factor)
            result[2:].arrange(RIGHT, buff=SMALL_BUFF)
            result[1].match_width(result[2:], stretch=True)
            result[1].next_to(result[2:], UP, SMALL_BUFF)
            result[0].next_to(result[1], UP, SMALL_BUFF)
            return result

        def fraction_anims(m1, m2, fraction):
            return [
                TransformFromCopy(m1, fraction[0]),
                TransformFromCopy(m1, fraction[2]),
                TransformFromCopy(m2, fraction[4]),
                GrowFromPoint(
                    fraction[1],
                    VGroup(m1, m2).get_center(),
                ),
                GrowFromPoint(
                    fraction[3],
                    VGroup(m1, m2).get_center(),
                ),
            ]

        frac1 = create_fraction(fp, tp)
        frac2 = create_fraction(fp, tn)
        fracs = VGroup(frac1, frac2)
        fracs.arrange(RIGHT, buff=3)
        fracs.to_edge(UP, buff=1.5)

        title.add(underline)
        fpr = OldTexText(
            "1\\% ", "F", "", "P", "", "R", "",
            font_size=72
        )
        fpr.add(Underline(fpr))
        fpr[-1].set_width(0)
        fpr.match_style(title)
        fpr.next_to(frac2, UP, MED_LARGE_BUFF)

        frac2.save_state()
        frac2.set_x(0)

        self.play(
            FadeOut(arrow),
            LaggedStart(*fraction_anims(fp, tn, frac2))
        )
        self.wait(2)

        self.play(
            ReplacementTransform(title, fpr),
            Restore(frac2)
        )
        self.play(
            LaggedStartMap(Write, word_grid[:2], lag_ratio=0),
            LaggedStartMap(ShowCreation, word_boxes[:2], lag_ratio=0),
            with_pop.set_opacity, 0.2,
            run_time=1,
        )
        self.play(
            LaggedStart(*fraction_anims(fp, tp, frac1)),
            fn.set_opacity, 0.5,
            tn.set_opacity, 0.5,
        )
        self.wait()

        comment = OldTexText("What we actually want")
        comment.next_to(frac1, UP, buff=0.75)

        self.play(FadeIn(comment, 0.5 * UP))
        self.wait()

        # Prep for Bayes calculation
        right_brace = Brace(word_boxes[2], RIGHT, buff=SMALL_BUFF)
        left_brace = Brace(word_boxes[1], LEFT, buff=SMALL_BUFF)
        fpr.generate_target()
        fpr.target.scale(48 / 72)
        fpr.target.next_to(right_brace, RIGHT)
        fnr = OldTexText("10\\% FNR")
        fnr.next_to(left_brace, LEFT)
        VGroup(left_brace, right_brace, fnr).set_color(GREY_A)

        self.play(
            MoveToTarget(fpr),
            GrowFromCenter(left_brace),
            GrowFromCenter(right_brace),
            FadeIn(fnr),
            FadeOut(comment),
            FadeOut(fracs),
            fn.set_opacity, 1.0,
            tn.set_opacity, 1.0,
        )

        prior_title = OldTexText("Prior: 1 in 1,000", font_size=72)
        prior_title.to_edge(UP)
        self.play(FadeIn(prior_title, UP))
        self.wait()

        # Show population counts
        full_pop = VGroup(
            OldTexText("Imagine"),
            Integer(10000),
            OldTexText("People")
        )
        full_pop.arrange(RIGHT, aligned_edge=DOWN)
        full_pop.set_color(GREY_A)
        full_pop.next_to(prior_title, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(full_pop[0::2]),
            CountInFrom(full_pop[1], 0),
            FadeOut(with_pop),
            FadeOut(without_pop),
        )
        self.wait()

        def move_number_above_word(number, word, target_count, buff=MED_SMALL_BUFF, scene=self):
            mover = number.copy()
            mover.original_bottom = mover.get_bottom()
            start_count = number.get_value()
            scene.play(
                UpdateFromAlphaFunc(
                    mover,
                    lambda m, a, word=word, sc=start_count, tc=target_count, buff=buff: m.set_color(
                        interpolate_color(GREY_A, word.get_color(), a)
                    ).set_value(
                        interpolate(sc, tc, a),
                    ).move_to(
                        interpolate(
                            m.original_bottom,
                            word.get_top() + buff * UP,
                            a
                        ),
                        DOWN,
                    )
                )
            )
            return mover

        with_count = move_number_above_word(full_pop[1], group_titles[0], 10, buff=0.3)
        self.wait()
        without_count = move_number_above_word(full_pop[1], group_titles[1], 9990)
        self.wait()

        self.play(word_grid.shift, 0.25 * DOWN)
        tp_count = move_number_above_word(with_count, word_grid[0], 9, SMALL_BUFF)
        fn_count = move_number_above_word(with_count, word_grid[1], 1, SMALL_BUFF)
        self.wait()
        fp_count = move_number_above_word(without_count, word_grid[2], 100, SMALL_BUFF)
        tn_count = move_number_above_word(without_count, word_grid[3], 9890, buff=0.05)
        self.wait()

        faders = VGroup(
            with_count, without_count,
            group_titles,
            fpr, fnr,
            fn, tn, fn_count, tn_count,
        )
        braces = VGroup(left_brace, right_brace)
        self.play(faders.set_opacity, 0.3, FadeOut(braces))
        self.wait()

        # Show posterior
        prior_group = VGroup(prior_title, full_pop)
        prior_group.generate_target()
        prior_group.target.to_edge(LEFT)
        prior_group.target.shift(0.5 * DOWN)

        arrow = Vector(0.8 * RIGHT)
        arrow.next_to(prior_group.target[0], RIGHT)

        post_word = OldTexText("Posterior:", font_size=72)
        post_word.set_color(BLUE)
        post_word.next_to(arrow, RIGHT)
        post_word.align_to(prior_group.target[0][0][0], DOWN)
        post_frac = create_fraction(tp_count, fp_count, scale_factor=1)
        post_frac.next_to(post_word, RIGHT, MED_LARGE_BUFF)

        rhs = OldTex("\\approx", "8.3\\%")
        rhs.next_to(post_frac, RIGHT)

        self.play(
            MoveToTarget(prior_group),
            GrowArrow(arrow),
            Write(post_word, run_time=1),
        )
        self.play(*fraction_anims(tp_count, fp_count, post_frac))
        self.wait()
        self.play(Write(rhs))
        self.wait()
