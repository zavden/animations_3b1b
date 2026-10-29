# ==============================================================================
# Scene:      SimpleExample
# Source:     videos/_2022/convolutions/discrete.py (lines 785-1089)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleExample.py SimpleExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_aligned_pairs(group1, group2, n):
    return VGroup(*(
        VGroup(m1, m2)
        for m1 in group1
        for m2 in group2
        if m1.index + m2.index == n
    ))


def get_row_shift(top_row, low_row, n):
    min_index = low_row[0].index
    max_index = top_row[-1].index
    max_sum = min_index + max_index
    if n <= max_sum:
        x_shift = top_row[n - 2 * min_index].get_x() - low_row[0].get_x()
    else:
        x_shift = top_row[-1].get_x() - low_row[n - max_sum].get_x()
    return low_row.animate.shift(x_shift * RIGHT)


class SimpleExample(InteractiveScene):
    def construct(self):
        # Question
        question = Text("What is")
        conv = Tex("(1, 2, 3) * (4, 5, 6)")
        group = VGroup(question, conv)
        group.arrange(DOWN)
        group.to_edge(UP)

        self.play(Write(question, run_time=1.5), FadeIn(conv, 0.5 * DOWN, time_span=(0.5, 1.5)))
        self.wait()

        # Blocks
        top_row = Square(side_length=0.75).get_grid(1, 3, buff=0)
        top_row.set_stroke(GREY_B, 2)
        top_row.set_fill(GREY_E, 1)
        low_row = top_row.copy()
        for row, values in (top_row, range(1, 4)), (low_row, range(4, 7)):
            for index, value, square in zip(it.count(), values, row):
                value_label = Integer(value)
                value_label.move_to(square)
                square.value_label = value_label
                square.add(value_label)
                square.value = value
                square.index = index

        VGroup(top_row, low_row).arrange(RIGHT, buff=LARGE_BUFF)

        self.play(
            TransformMatchingShapes(conv[1:6:2].copy(), top_row),
            TransformMatchingShapes(conv[9:14:2].copy(), low_row),
        )
        self.wait()

        # Labels
        self.add_block_labels(top_row, "a", BLUE)
        self.add_block_labels(low_row, "b", RED)

        # Set up position
        top_row.generate_target()
        low_row.generate_target()
        low_row.target.rotate(PI)
        for square in low_row.target:
            square.value_label.rotate(PI)
            square.label.rotate(PI)
        top_row.target.center()
        low_row.target.next_to(top_row.target, DOWN, MED_LARGE_BUFF)

        conv_result = np.convolve([1, 2, 3], [4, 5, 6])
        rhs_args = ["=", R"\big("]
        for k in conv_result:
            rhs_args.append(str(k))
            rhs_args.append(",")
        rhs_args[-1] = R"\big)"
        rhs = OldTex(*rhs_args)
        rhs[1:].set_color(YELLOW)
        conv.generate_target()
        group = VGroup(conv.target, rhs)
        group.arrange(RIGHT, buff=0.2)
        group.next_to(top_row, UP, buff=2),

        self.play(LaggedStart(
            MoveToTarget(top_row),
            MoveToTarget(low_row, path_arc=PI),
            MoveToTarget(conv),
            Write(VGroup(*rhs[:2], rhs[-1])),
            FadeOut(question, UP),
        ))
        self.wait()

        # March!
        c_labels = VGroup()
        for n in range(len(conv_result)):
            self.play(get_row_shift(top_row, low_row, n))

            pairs = get_aligned_pairs(top_row, low_row, n)
            label_pairs = VGroup(*(
                VGroup(m1.value_label, m2.value_label)
                for m1, m2 in pairs
            ))
            new_label_pairs = label_pairs.copy()
            expr = VGroup()
            symbols = VGroup()
            for label_pair in new_label_pairs:
                label_pair.arrange(RIGHT, buff=MED_SMALL_BUFF)
                label_pair.next_to(expr, RIGHT, SMALL_BUFF)
                dot = OldTex(R"\dot")
                dot.move_to(label_pair)
                plus = OldTex("+")
                plus.next_to(label_pair, RIGHT, SMALL_BUFF)
                expr.add(*label_pair, dot, plus)
                symbols.add(dot, plus)
            symbols[-1].scale(0, about_point=symbols[-2].get_right())
            expr.next_to(label_pairs, UP, LARGE_BUFF)
            c_label = OldTex(f"c_{n}", font_size=30, color=YELLOW).next_to(rhs[2 * n + 2], UP)

            rects = VGroup(*(
                SurroundingRectangle(lp, buff=0.2).set_stroke(YELLOW, 1).round_corners()
                for lp in label_pairs
            ))
            self.play(FadeIn(rects, lag_ratio=0.5))
            self.play(
                LaggedStart(*(
                    TransformFromCopy(lp, nlp)
                    for lp, nlp in zip(label_pairs, new_label_pairs)
                ), lag_ratio=0.5),
                Write(symbols),
            )
            self.wait()
            anims = [
                FadeTransform(expr.copy(), rhs[2 * n + 2]),
                c_labels.animate.set_opacity(0.35),
                FadeIn(c_label)
            ]
            if n < 4:
                anims.append(Write(rhs[2 * n + 3]))
            self.play(*anims)
            self.wait()
            self.play(FadeOut(expr), FadeOut(rects))

            c_labels.add(c_label)
        self.play(FadeOut(c_labels))

        # Grid of values
        equation = VGroup(conv, rhs)
        values1 = VGroup(*(block.value_label for block in top_row)).copy()
        values2 = VGroup(*(block.value_label for block in low_row)).copy()

        grid = Square(side_length=1.0).get_grid(3, 3, buff=0)
        grid.set_stroke(WHITE, 2)
        grid.set_fill(GREY_E, 1.0)
        grid.move_to(DL)

        self.play(
            Write(grid, time_span=(0.5, 2.0)),
            LaggedStart(
                *(
                    value.animate.next_to(square, UP, buff=0.2)
                    for value, square in zip(values1, grid[:3])
                ),
                *(
                    value.animate.next_to(square, LEFT, buff=0.2)
                    for value, square in zip(values2, grid[0::3])
                ),
                run_time=2
            ),
            *(
                MaintainPositionRelativeTo(block, value)
                for row, values in [(top_row, values1), (low_row, values2)]
                for block, value in zip(row, values)
            ),
            VFadeOut(top_row),
            VFadeOut(low_row),
            equation.animate.center().to_edge(UP)
        )

        # Products
        products = VGroup()
        diag_groups = VGroup().replicate(5)
        for n, square in enumerate(grid):
            i, j = n // 3, n % 3
            v1 = values1[j]
            v2 = values2[i]
            product = Integer(v1.get_value() * v2.get_value())
            product.match_height(v1)
            product.move_to(square)
            product.factors = (v1, v2)
            square.product = product
            products.add(product)
            diag_groups[i + j].add(product)

        products.set_color(GREEN)

        self.play(LaggedStart(*(
            ReplacementTransform(factor.copy(), product)
            for product in products
            for factor in product.factors
        ), lag_ratio=0.1))
        self.wait()

        # Circle diagonals
        products.rotate(PI / 4)
        ovals = VGroup()
        radius = 0.3
        for diag in diag_groups:
            oval = SurroundingRectangle(diag, buff=0.19)
            oval.set_width(2 * radius, stretch=True)
            oval.set_stroke(YELLOW, 2)
            oval.round_corners(radius=radius)
            ovals.add(oval)
        VGroup(products, ovals).rotate(-PI / 4)
        ovals[0].become(Circle(radius=radius).match_style(ovals[0]).move_to(products[0]))

        arrows = VGroup(*(
            Vector(0.5 * UP).next_to(part, DOWN)
            for part in rhs[2::2]
        ))
        arrows.set_color(YELLOW)

        curr_arrow = arrows[0].copy()
        curr_arrow.shift(0.5 * DOWN).set_opacity(0)
        for n, oval, arrow in zip(it.count(), ovals, arrows):
            self.play(
                ShowCreation(oval),
                ovals[:n].animate.set_stroke(opacity=0.25),
                Transform(curr_arrow, arrow)
            )
            self.wait(0.5)
        self.play(ovals.animate.set_stroke(opacity=0.25), FadeOut(curr_arrow))
        self.wait()

        grid_group = VGroup(grid, values1, values2, products, ovals)

        # Show polynomial
        polynomial_eq = Tex(
            R"\left(1 + 2x + 3x^2\right)\left(4 + 5x + 6x^2\right)"
            R"={4} + {13}x + {28}x^2 + {27}x^3 + {18}x^4",
            tex_to_color_map=dict(
                (f"{{{n}}}", YELLOW)
                for n in conv_result
            )
        )
        polynomial_eq.next_to(equation, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(polynomial_eq, DOWN),
            grid_group.animate.center().to_edge(DOWN)
        )
        self.wait()

        # Replace terms
        self.play(grid_group.animate.set_height(4.5, about_edge=DOWN))

        for i, value in zip((*range(3), *range(3)), (*values1, *values2)):
            tex = ["", "x", "x^2"][i]
            value.target = Tex(f"{value.get_value()}{tex}")
            value.target.scale(value.get_height() / value.target[0].get_height())
            value.target.move_to(value, DOWN)
        values2[1].target.align_to(values2[0].target, RIGHT)
        values2[2].target.align_to(values2[0].target, RIGHT)
        for n, diag_group in enumerate(diag_groups):
            tex = ["", "x", "x^2", "x^3", "x^4"][n]
            for product in diag_group:
                product.target = Tex(f"{product.get_value()}{tex}")
                product.target.match_style(product)
                product.target.scale(0.9)
                product.target.move_to(product)

        eq_values1 = VGroup(polynomial_eq[1], polynomial_eq[3:5], polynomial_eq[6:9])
        eq_values2 = VGroup(polynomial_eq[11], polynomial_eq[13:15], polynomial_eq[16:19])

        for values, eq_values in [(values1, eq_values1), (values2, eq_values2)]:
            self.play(
                LaggedStart(*(TransformMatchingShapes(ev.copy(), v.target) for ev, v in zip(eq_values, values))),
                LaggedStart(*(FadeTransform(v, v.target[0]) for v in values)),
            )
        self.wait()
        old_rects = VGroup()
        for n, prod in enumerate(products):
            new_rects = VGroup(
                SurroundingRectangle(values1[n % 3].target),
                SurroundingRectangle(values2[n // 3].target),
            )
            new_rects.set_stroke(GREEN, 2)
            self.play(
                FadeIn(new_rects),
                FadeOut(old_rects),
                FadeTransform(prod, prod.target[:len(prod)]),
                FadeIn(prod.target[len(prod):], scale=2),
                FlashAround(prod.target, time_width=1),
                run_time=1.0
            )
            old_rects = new_rects
        self.play(FadeOut(old_rects))

        # Show diagonals again
        arrows = VGroup(*(
            Vector(0.5 * UP).next_to(polynomial_eq.select_part(f"{{{n}}}"), DOWN, buff=SMALL_BUFF)
            for n in conv_result
        ))
        arrows.set_color(YELLOW)

        curr_arrow = arrows[0].copy().shift(DOWN).set_opacity(0)
        for n, oval, arrow in zip(it.count(), ovals, arrows):
            self.play(
                oval.animate.set_stroke(opacity=1),
                Transform(curr_arrow, arrow),
                ovals[:n].animate.set_stroke(opacity=0.25),
            )
            self.wait(0.5)
        self.play(
            FadeOut(curr_arrow),
            ovals.animate.set_stroke(opacity=0.5)
        )

    def add_block_labels(self, blocks, letter, color=BLUE, font_size=30):
        labels = VGroup()
        for n, square in enumerate(blocks):
            label = OldTex(f"{letter}_{{{n}}}", font_size=font_size)
            label.set_color(color)
            label.next_to(square, UP, SMALL_BUFF)
            square.label = label
            square.add(label)
            labels.add(label)
        return labels
