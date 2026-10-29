# ==============================================================================
# Scene:      IsSellerOne100
# Source:     videos/_2020/beta/beta1.py (lines 1158-1545)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl IsSellerOne100.py IsSellerOne100 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


def get_prob_positive_experience_label(include_equals=False,
                                       include_decimal=False,
                                       include_q_mark=False):
    label = OldTex(
        "P", "(", "00000", ")",
    )

    pe = OldTexText("Positive\\\\experience")
    pe.set_color(GREEN)
    pe.replace(label[2], dim_to_match=0)
    label.replace_submobject(2, pe)
    VGroup(label[1], label[3]).match_height(
        pe, stretch=True, about_edge=DOWN,
    )
    if include_equals:
        eq = OldTex("=").next_to(label, RIGHT)
        label.add(eq)
    if include_decimal:
        decimal = DecimalNumber(0.95)
        decimal.next_to(label, RIGHT)
        decimal.set_color(YELLOW)
        label.decimal = decimal
        label.add(decimal)
    if include_q_mark:
        q_mark = OldTex("?")
        q_mark.relative_mob = label[-1]
        q_mark.add_updater(
            lambda m: m.next_to(m.relative_mob, RIGHT, SMALL_BUFF)
        )
        label.add(q_mark)

    return label



# ----- From _2020/beta/beta1.py -----

class IsSellerOne100(Scene):
    def construct(self):
        self.add_review()
        self.show_probability()
        self.show_simulated_reviews()

    def add_review(self):
        reviews = VGroup(*[Tex(CMARK_TEX) for x in range(10)])
        reviews.arrange(RIGHT)
        reviews.scale(2)
        reviews.set_color(GREEN)
        reviews.next_to(ORIGIN, UP)

        blanks = VGroup(*[
            Line(LEFT, RIGHT).match_width(rev).next_to(rev, DOWN, SMALL_BUFF)
            for rev in reviews
        ])
        blanks.shift(0.25 * reviews[0].get_width() * LEFT)

        label = OldTexText(
            " out of ",
        )
        tens = VGroup(*[Integer(10) for x in range(2)])
        tens[0].next_to(label, LEFT)
        tens[1].next_to(label, RIGHT)
        tens.set_color(GREEN)
        label.add(tens)
        label.scale(2)
        label.next_to(reviews, DOWN, LARGE_BUFF)

        self.add(label)
        self.add(blanks)
        tens[0].to_count = reviews
        self.play(
            ShowIncreasingSubsets(reviews, int_func=np.ceil),
            UpdateFromAlphaFunc(
                tens[0],
                lambda m, a: m.set_color(
                    interpolate_color(RED, GREEN, a)
                ).set_value(len(m.to_count))
            ),
            run_time=2,
            rate_func=bezier([0, 0, 1, 1]),
        )
        self.wait()

        self.review_group = VGroup(reviews, blanks, label)

    def show_probability(self):
        review_group = self.review_group

        prob_label = get_prob_positive_experience_label()
        prob_label.add(OldTex("=").next_to(prob_label, RIGHT))
        rhs = DecimalNumber(1)
        rhs.next_to(prob_label, RIGHT)
        rhs.set_color(YELLOW)
        prob_label.add(rhs)
        prob_label.scale(2)
        prob_label.to_corner(UL)

        q_mark = OldTex("?")
        q_mark.set_color(YELLOW)
        q_mark.match_height(rhs)
        q_mark.reference = rhs
        q_mark.add_updater(lambda m: m.next_to(m.reference, RIGHT))

        rhs_rect = SurroundingRectangle(rhs, buff=0.2)
        rhs_rect.set_color(RED)

        not_necessarily = OldTexText("Not necessarily!")
        not_necessarily.set_color(RED)
        not_necessarily.scale(1.5)
        not_necessarily.next_to(prob_label, DOWN, 1.5)
        arrow = Arrow(
            not_necessarily.get_top(),
            rhs_rect.get_corner(DL),
            buff=MED_SMALL_BUFF,
        )
        arrow.set_color(RED)

        rhs.set_value(0)
        self.play(
            ChangeDecimalToValue(rhs, 1),
            UpdateFromAlphaFunc(
                prob_label,
                lambda m, a: m.set_opacity(a),
            ),
            FadeIn(q_mark),
        )
        self.wait()
        self.play(
            ShowCreation(rhs_rect),
            Write(not_necessarily),
            ShowCreation(arrow),
            review_group.to_edge, DOWN,
            run_time=1,
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(rhs, 0.95),
            FadeOut(rhs_rect),
            FadeOut(arrow),
            FadeOut(not_necessarily),
        )
        self.wait()

        self.prob_label_group = VGroup(
            prob_label, rhs, q_mark,
        )

    def show_simulated_reviews(self):
        prob_label_group = self.prob_label_group
        review_group = self.review_group

        # Set up decimals
        random.seed(2)
        decimals = VGroup()
        for x in range(10):
            dec = DecimalNumber()
            decimals.add(dec)

        def randomize_decimals(decimals):
            for dec in decimals:
                value = random.random()
                dec.set_value(value)
                if value > 0.95:
                    dec.set_color(RED)
                else:
                    dec.set_color(WHITE)

        randomize_decimals(decimals)

        decimals.set_height(0.3)
        decimals.arrange(RIGHT, buff=MED_LARGE_BUFF)
        decimals.next_to(ORIGIN, DOWN)
        decimals[0].set_value(0.42)
        decimals[0].set_color(WHITE)
        decimals[1].set_value(0.97)
        decimals[1].set_color(RED)

        random_label = OldTexText("Random number\\\\in [0, 1]")
        random_label.scale(0.7)
        random_label.next_to(decimals[0], DOWN)
        random_label.set_color(GREY_B)

        arrows = VGroup()
        for dec in decimals:
            arrow = Vector(0.4 * UP)
            arrow.next_to(dec, UP)
            arrows.add(arrow)

        # Set up marks
        def get_marks(decs, arrows):
            marks = VGroup()
            for dec, arrow in zip(decs, arrows):
                if dec.get_value() < 0.95:
                    mark = OldTex(CMARK_TEX)
                    mark.set_color(GREEN)
                else:
                    mark = OldTex(XMARK_TEX)
                    mark.set_color(RED)
                mark.set_height(0.5)
                mark.next_to(arrow, UP)
                marks.add(mark)
            return marks

        marks = get_marks(decimals, arrows)

        lt_p95 = OldTex("< 0.95")
        gte_p95 = OldTex("\\ge 0.95")
        for label in lt_p95, gte_p95:
            label.match_height(decimals[0])

        lt_p95.next_to(decimals[0], RIGHT, MED_SMALL_BUFF)
        gte_p95.next_to(decimals[1], RIGHT, MED_SMALL_BUFF)
        lt_p95.set_color(GREEN)
        gte_p95.set_color(RED)

        # Introduce simulation
        review_group.save_state()
        self.play(
            review_group.scale, 0.25,
            review_group.to_corner, UR,
            Write(random_label),
            CountInFrom(decimals[0], 0),
        )
        self.wait()
        self.play(FadeIn(lt_p95, LEFT))
        self.play(
            GrowArrow(arrows[0]),
            FadeIn(marks[0], DOWN)
        )
        self.wait()
        self.play(
            FadeOut(lt_p95, 0.5 * RIGHT),
            FadeIn(gte_p95, 0.5 * LEFT),
        )
        self.play(
            random_label.match_x, decimals[1],
            CountInFrom(decimals[1], 0),
            UpdateFromAlphaFunc(
                decimals[1],
                lambda m, a: m.set_opacity(a),
            ),
        )
        self.play(
            GrowArrow(arrows[1]),
            FadeIn(marks[1], DOWN),
        )
        self.wait()
        self.play(
            LaggedStartMap(
                CountInFrom, decimals[2:],
            ),
            UpdateFromAlphaFunc(
                decimals[2:],
                lambda m, a: m.set_opacity(a),
            ),
            FadeOut(gte_p95),
            run_time=1,
        )
        self.add(decimals)
        self.play(
            LaggedStartMap(GrowArrow, arrows[2:]),
            LaggedStartMap(FadeInFromDown, marks[2:]),
            run_time=1
        )
        self.add(arrows, marks)
        self.wait()

        # Add new rows
        decimals.arrows = arrows
        decimals.add_updater(lambda d: d.next_to(d.arrows, DOWN))
        added_anims = [FadeOut(random_label)]
        rows = VGroup(marks)
        for x in range(3):
            self.play(
                arrows.shift, DOWN,
                UpdateFromFunc(decimals, randomize_decimals),
                *added_anims,
            )
            added_anims = []
            new_marks = get_marks(decimals, arrows)
            self.play(LaggedStartMap(FadeInFromDown, new_marks))
            self.wait()
            rows.add(new_marks)

        # Create a stockpile of new rows
        added_rows = VGroup()
        decimals.clear_updaters()
        decimals.save_state()
        for x in range(100):
            randomize_decimals(decimals)
            added_rows.add(get_marks(decimals, arrows))
        decimals.restore()

        # Compress rows
        rows.generate_target()
        for group in rows.target, added_rows:
            group.scale(0.3)
            for row in group:
                row.arrange(RIGHT, buff=SMALL_BUFF)
            group.arrange(DOWN, buff=0.2)
        rows.target.next_to(prob_label_group, DOWN, MED_LARGE_BUFF)
        rows.target.set_x(-3.5)

        nr = 15
        added_rows[:nr].move_to(rows.target, UP)
        added_rows[nr:2 * nr].move_to(rows.target, UP)
        added_rows[nr:2 * nr].shift(3.5 * RIGHT)
        added_rows[2 * nr:3 * nr].move_to(rows.target, UP)
        added_rows[2 * nr:3 * nr].shift(7 * RIGHT)
        added_rows = added_rows[4:3 * nr]

        self.play(
            MoveToTarget(rows),
            FadeOut(decimals),
            FadeOut(arrows),
        )
        self.play(ShowIncreasingSubsets(added_rows), run_time=3)

        # Show scores
        all_rows = VGroup(*rows, *added_rows)
        scores = VGroup()
        ten_rects = VGroup()
        for row in all_rows:
            score = Integer(sum([
                mark.get_color() == Color(GREEN)
                for mark in row
            ]))
            score.match_height(row)
            score.next_to(row, RIGHT)
            if score.get_value() == 10:
                score.set_color(TEAL)
                ten_rects.add(SurroundingRectangle(score))
            scores.add(score)

        ten_rects.set_stroke(YELLOW, 2)

        self.play(FadeIn(scores))
        self.wait()
        self.play(LaggedStartMap(ShowCreation, ten_rects))
        self.play(LaggedStartMap(FadeOut, ten_rects))
        self.wait(2)

        # Show alternate possibilities
        prob = DecimalNumber(0.95)
        prob.set_color(YELLOW)
        template = prob_label_group[0][-1]
        prob.match_height(template)
        prob.move_to(template, LEFT)
        rect = BackgroundRectangle(template, buff=SMALL_BUFF)
        rect.set_fill(BLACK, 1)
        self.add(rect)
        self.add(prob)
        self.play(
            LaggedStartMap(FadeOutAndShift, all_rows, lag_ratio=0.01),
            LaggedStartMap(FadeOutAndShift, scores, lag_ratio=0.01),
            Restore(review_group),
        )
        for value in [0.9, 0.99, 0.8, 0.95]:
            self.play(ChangeDecimalToValue(prob, value))
            self.wait()

    # No longer used
    def show_random_numbers(self):
        prob_label_group = self.prob_label_group

        random.seed(2)
        rows = VGroup(*[
            VGroup(*[
                Integer(
                    random.randint(0, 99)
                ).move_to(0.85 * x * RIGHT)
                for x in range(10)
            ])
            for y in range(10 * 2)
        ])
        rows.arrange_in_grid(n_cols=2, buff=MED_LARGE_BUFF)
        rows[:10].shift(LEFT)
        rows.set_height(5.5)
        rows.center().to_edge(DOWN)

        lt_95 = VGroup(*[
            mob
            for row in rows
            for mob in row
            if mob.get_value() < 95
        ])

        square = Square()
        square.set_stroke(width=0)
        square.set_fill(YELLOW, 0.5)
        square.set_width(1.5 * rows[0][0].get_height())
        # highlights = VGroup(*[
        #     square.copy().move_to(mob)
        #     for row in rows
        #     for mob in row
        #     if mob.get_value() < 95
        # ])

        row_rects = VGroup(*[
            SurroundingRectangle(row)
            for row in rows
            if all([m.get_value() < 95 for m in row])
        ])
        row_rects.set_stroke(GREEN, 2)

        self.play(
            LaggedStartMap(
                ShowIncreasingSubsets, rows,
                run_time=3,
                lag_ratio=0.25,
            ),
            FadeOut(self.review_group, DOWN),
            prob_label_group.set_height, 0.75,
            prob_label_group.to_corner, UL,
        )
        self.wait()
        # self.add(highlights, rows)
        self.play(
            # FadeIn(highlights)
            lt_95.set_fill, BLUE,
            lt_95.set_stroke, BLUE, 2, {"background": True},
        )
        self.wait()
        self.play(LaggedStartMap(ShowCreation, row_rects))
        self.wait()
