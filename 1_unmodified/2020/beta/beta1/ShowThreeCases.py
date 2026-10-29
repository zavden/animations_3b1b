# ==============================================================================
# Scene:      ShowThreeCases
# Source:     videos/_2020/beta/beta1.py (lines 243-448)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl ShowThreeCases.py ShowThreeCases -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"



# ----- From _2020/beta/beta1.py -----

class ShowThreeCases(Scene):
    def construct(self):
        titles = self.get_titles()
        reviews = self.get_reviews(titles)
        for review in reviews:
            review.match_x(reviews[2])

        # Introduce everything
        self.play(LaggedStartMap(
            FadeInFrom, titles,
            lambda m: (m, DOWN),
            lag_ratio=0.2
        ))
        self.play(LaggedStart(*[
            LaggedStartMap(
                FadeInFromLarge, review,
                lag_ratio=0.1
            )
            for review in reviews
        ], lag_ratio=0.1))
        self.add(reviews)
        self.wait()

        self.play(ShowCreationThenFadeAround(reviews[2]))
        self.wait()

        # Suspicious of 100%
        randy = Randolph()
        randy.flip()
        randy.set_height(2)
        randy.next_to(
            reviews[0], RIGHT, LARGE_BUFF,
            aligned_edge=UP,
        )
        randy.look_at(reviews[0])
        self.play(FadeIn(randy))
        self.play(randy.change, "sassy")
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy))

        # Low number means it could be a fluke.
        review = reviews[0]

        review.generate_target()
        review.target.scale(2)
        review.target.arrange(RIGHT)
        review.target.move_to(review)

        self.play(MoveToTarget(review))

        alt_negs = [1, 2, 1, 0]
        alt_reviews = VGroup()
        for k in alt_negs:
            alt_reviews.add(self.get_plusses_and_minuses(titles[0], 1, 10, k))
        for ar in alt_reviews:
            for m1, m2 in zip(ar, review):
                m1.replace(m2)

        alt_percents = VGroup(*[
            OldTex(str(10 * (10 - k)) + "\\%")
            for k in alt_negs
        ])
        hundo = titles[0][0]
        for ap in alt_percents:
            fix_percent(ap.family_members_with_points()[-1])
            ap.match_style(hundo)
            ap.match_height(hundo)
            ap.move_to(hundo, RIGHT)

        last_review = review
        last_percent = hundo
        for ar, ap in zip(alt_reviews, alt_percents):
            self.play(
                FadeIn(ar, 0.5 * DOWN, lag_ratio=0.2),
                FadeOut(last_review),
                FadeIn(ap, 0.5 * DOWN),
                FadeOut(last_percent, 0.5 * UP),
                run_time=1.5
            )
            last_review = ar
            last_percent = ap
        self.remove(last_review, last_percent)
        self.add(titles, *reviews)

        # How do you think about the tradeoff?
        p1 = titles[1][0]
        p2 = titles[2][0]
        nums = VGroup(p1, p2)
        lower_reviews = reviews[1:]
        lower_reviews.generate_target()
        lower_reviews.target.arrange(LEFT, buff=1.5)
        lower_reviews.target.center()
        nums.generate_target()
        for nt, review in zip(nums.target, lower_reviews.target):
            nt.next_to(review, UP, MED_LARGE_BUFF)

        nums.target[0].match_y(nums.target[1])

        self.clear()
        self.play(
            MoveToTarget(lower_reviews),
            MoveToTarget(nums),
            FadeOut(titles[1][1:]),
            FadeOut(titles[2][1:]),
            FadeOut(titles[0]),
            FadeOut(reviews[0]),
            run_time=2,
        )

        greater_than = OldTex(">")
        greater_than.scale(2)
        greater_than.move_to(midpoint(
            reviews[2].get_right(),
            reviews[1].get_left(),
        ))
        less_than = greater_than.copy().flip()
        less_than.match_height(nums[0][0])
        less_than.match_y(nums, DOWN)

        nums.generate_target()
        nums.target[1].next_to(less_than, LEFT, MED_LARGE_BUFF)
        nums.target[0].next_to(less_than, RIGHT, MED_LARGE_BUFF)

        squares = VGroup(*[
            SurroundingRectangle(
                submob, buff=0.01,
                stroke_color=GREY_B,
                stroke_width=1,
            )
            for submob in reviews[2]
        ])
        squares.shuffle()
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeOut, squares,
                lag_ratio=0.5 / len(squares),
                run_time=3,
            ),
            Write(greater_than),
        )
        self.wait()
        self.play(
            MoveToTarget(nums),
            TransformFromCopy(
                greater_than, less_than,
            )
        )
        self.wait()

    def get_titles(self):
        titles = VGroup(
            OldTexText(
                "$100\\%$ \\\\",
                "10 reviews"
            ),
            OldTexText(
                "$96\\%$ \\\\",
                "50 reviews"
            ),
            OldTexText(
                "$93\\%$ \\\\",
                "200 reviews"
            ),
        )
        colors = [PINK, BLUE, YELLOW]
        for title, color in zip(titles, colors):
            fix_percent(title[0][-1])
            title[0].set_color(color)

        titles.scale(1.25)
        titles.arrange(DOWN, buff=1.5)
        titles.to_corner(UL)
        return titles

    def get_reviews(self, titles):
        return VGroup(
            self.get_plusses_and_minuses(
                titles[0], 5, 2, 0,
            ),
            self.get_plusses_and_minuses(
                titles[1], 5, 10, 2,
            ),
            self.get_plusses_and_minuses(
                titles[2], 8, 25, 14,
            ),
        )

    def get_plusses_and_minuses(self, title, n_rows, n_cols, n_minus):
        check = OldTex(CMARK_TEX, color=GREEN)
        cross = OldTex(XMARK_TEX, color=RED)
        checks = VGroup(*[
            check.copy() for x in range(n_rows * n_cols)
        ])
        checks.arrange_in_grid(n_rows=n_rows, n_cols=n_cols)
        checks.scale(0.5)
        # if checks.get_height() > title.get_height():
        #     checks.match_height(title)
        checks.next_to(title, RIGHT, LARGE_BUFF)

        for check in random.sample(list(checks), n_minus):
            mob = cross.copy()
            mob.replace(check, dim_to_match=0)
            check.become(mob)

        return checks
