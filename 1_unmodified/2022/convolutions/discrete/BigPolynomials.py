# ==============================================================================
# Scene:      BigPolynomials
# Source:     videos/_2022/convolutions/discrete.py (lines 1862-1995)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigPolynomials.py BigPolynomials -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class BigPolynomials(InteractiveScene):
    def construct(self):
        # Initialize grid
        N = 8
        height = 6.5
        grid = Square().get_grid(N, N, height=height, buff=0, group_by_rows=True)
        grid.set_stroke(WHITE, 1)
        grid.to_edge(DOWN, buff=MED_SMALL_BUFF)
        grid.shift(2 * LEFT)
        for i, row in enumerate(grid):
            if i == N - 2:
                for j, square in enumerate(row):
                    if j == N - 2:
                        self.replace_square(square, OldTex(R"\ddots"))
                    else:
                        self.replace_square(square, OldTex(R"\vdots"))
            else:
                self.replace_square(row[N - 2], OldTex(R"\cdots"))

        self.add(grid)

        # Polynomial terms
        a_terms, b_terms = all_terms = [
            VGroup(*(
                Tex(RF"{letter}_{{{n}}} x^{{{n}}}", font_size=24)
                for n in (*range(N - 1), 99)
            ))
            for letter in ["a", "b"]
        ]
        for terms in all_terms:
            terms[0].remove(*terms[0][-2:])
            terms[1].remove(*terms[1][-1:])

        for terms, group, vect in [(a_terms, grid[0], UP), (b_terms, grid, LEFT)]:
            for term, square in zip(terms, group):
                term.next_to(square, vect, SMALL_BUFF)

        a_terms[-2].become(OldTex(R"\cdots", font_size=24).move_to(a_terms[-2]).shift(0.02 * DOWN))
        b_terms[-2].become(OldTex(R"\vdots", font_size=24).move_to(b_terms[-2]))

        a_terms.set_color(BLUE_C)
        b_terms.set_color(TEAL_C)

        self.add(a_terms)
        self.add(b_terms)

        # Plusses
        for terms, vect in (a_terms, RIGHT), (b_terms, DOWN):
            terms.plusses = VGroup()
            for t1, t2 in zip(terms, terms[1:]):
                plus = OldTex("+", font_size=24).match_color(terms)
                plus.move_to(midpoint(t1.get_corner(vect), t2.get_corner(-vect)))
                terms.plusses.add(plus)
            self.add(terms.plusses)

        # Product terms
        prod_terms = VGroup()
        diags = VGroup(*(VGroup() for n in range(11)))

        for i, row in enumerate(grid):
            pre_b = b_terms[i][:2]
            if i == N - 2:
                continue
            if i == N - 1:
                i = 99
            for j, square in enumerate(row):
                pre_a = a_terms[j][:2]
                if j == N - 2:
                    continue
                if j == N - 1:
                    j = 99
                term = OldTex(f"a_{{{j}}}", f"b_{{{i}}}", f"x^{{{i + j}}}", font_size=20)
                if i + j == 0:
                    term[2].remove(*term[2][:-2])
                elif i + j == 1:
                    term[2].remove(term[2][:-2])
                term[0].match_color(a_terms)
                term[1].match_color(b_terms)
                term.set_max_width(0.9 * square.get_width())
                term.pre_a = pre_a
                term.pre_b = pre_b
                term.move_to(square)
                prod_terms.add(term)

                if i + j < len(diags):
                    diags[i + j].add(term)

        # Animate
        a_label = Text("100 terms", font_size=30)
        a_label.next_to(a_terms, UP)
        b_label = Text("100 terms", font_size=30)
        b_label.next_to(b_terms, UP, MED_LARGE_BUFF, aligned_edge=RIGHT)
        product_count = OldTexText(R"$100 \times 100 = 10{,}000$ \\ products", font_size=60)
        product_count.move_to(midpoint(grid.get_right(), RIGHT_SIDE))

        self.play(
            FlashAround(a_terms, run_time=2, time_width=2),
            FadeIn(a_label)
        )
        self.play(
            FlashAround(b_terms, run_time=2, time_width=2),
            FadeIn(b_label),
            FadeOut(a_label)
        )
        self.play(FadeOut(b_label))
        self.wait()
        self.play(
            LaggedStart(*(
                AnimationGroup(
                    TransformFromCopy(term.pre_a, term[0]),
                    TransformFromCopy(term.pre_b, term[1]),
                    FadeIn(term[2], rate_func=squish_rate_func(smooth, 0.5, 1)),
                )
                for term in prod_terms
            ), lag_ratio=0.1, run_time=5),
            Write(product_count),
        )
        self.add(prod_terms)

        # Group along diagonals
        self.play(prod_terms.animate.set_opacity(0.2))
        for n in range(len(diags)):
            diags.generate_target()
            diags.target.set_opacity(0.2)
            diags.target[n].set_opacity(1.0)
            self.play(MoveToTarget(diags))
        self.wait()

    def replace_square(self, square, mob):
        mob.move_to(square)
        mob.set_max_width(square.get_width() / 2)
        mob.set_max_height(square.get_width() / 2)
        square.set_opacity(0)
        square.add(mob)
