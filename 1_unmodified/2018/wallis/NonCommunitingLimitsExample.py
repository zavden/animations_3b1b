# ==============================================================================
# Scene:      NonCommunitingLimitsExample
# Source:     videos/_2018/wallis.py (lines 4262-4390)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NonCommunitingLimitsExample.py NonCommunitingLimitsExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NonCommunitingLimitsExample(Scene):
    CONFIG = {
        "num_terms_per_row": 6,
        "num_rows": 5,
        "x_spacing": 0.75,
        "y_spacing": 1,
    }

    def construct(self):
        rows = VGroup(*[
            self.get_row(seven_index)
            for seven_index in range(self.num_rows)
        ])
        rows.add(self.get_v_dot_row())
        for n, row in enumerate(rows):
            row.move_to(n * self.y_spacing * DOWN)
        rows.center().to_edge(UP)
        rows[-1].shift(MED_SMALL_BUFF * UP)

        row_rects = VGroup(*list(map(SurroundingRectangle, rows[:-1])))
        row_rects.set_color(YELLOW)

        columns = VGroup(*[
            VGroup(*[row[0][i] for row in rows])
            for i in range(len(rows[0][0]))
        ])
        column_rects = VGroup(*list(map(SurroundingRectangle, columns)))
        column_rects.set_color(BLUE)

        row_arrows = VGroup(*[
            OldTex("\\rightarrow").next_to(row, RIGHT)
            for row in rows[:-1]
        ])
        row_products = VGroup(*[
            Integer(7).next_to(arrow)
            for arrow in row_arrows
        ])
        row_products.set_color(YELLOW)

        row_product_limit_dots = OldTex("\\vdots")
        row_product_limit_dots.next_to(row_products, DOWN)
        row_product_limit = Integer(7)
        row_product_limit.set_color(YELLOW)
        row_product_limit.next_to(row_product_limit_dots, DOWN)

        column_arrows = VGroup(*[
            OldTex("\\downarrow").next_to(part, DOWN, SMALL_BUFF)
            for part in rows[-1][0]
        ])
        column_limits = VGroup(*[
            Integer(1).next_to(arrow, DOWN)
            for arrow in column_arrows
        ])
        column_limits.set_color(BLUE)
        column_limit_dots = self.get_row_dots(column_limits)

        column_limits_arrow = OldTex("\\rightarrow").next_to(
            column_limit_dots, RIGHT
        )
        product_of_limits = Integer(1).next_to(column_limits_arrow, RIGHT)
        product_of_limits.set_color(BLUE)

        self.add(rows)
        self.wait()
        self.play(LaggedStartMap(ShowCreation, row_rects))
        self.wait(2)
        row_products_iter = iter(row_products)
        self.play(
            LaggedStartMap(Write, row_arrows),
            LaggedStartMap(
                ReplacementTransform, rows[:-1].copy(),
                lambda r: (r, next(row_products_iter))
            )
        )
        self.wait()
        self.play(Write(row_product_limit_dots))
        self.play(Write(row_product_limit))
        self.wait()

        self.play(LaggedStartMap(FadeOut, row_rects))
        self.play(LaggedStartMap(FadeIn, column_rects))
        self.wait()
        column_limit_iter = iter(column_limits)
        self.play(
            LaggedStartMap(Write, column_arrows),
            LaggedStartMap(
                ReplacementTransform, columns.copy(),
                lambda c: (c, next(column_limit_iter))
            )
        )
        self.wait()
        self.play(Write(column_limits_arrow))
        self.play(
            Write(product_of_limits),
            FadeOut(row_product_limit)
        )
        self.wait()


    def get_row(self, seven_index):
        terms = [1] * (self.num_terms_per_row)
        if seven_index < len(terms):
            terms[seven_index] = 7
        row = VGroup(*list(map(Integer, terms)))
        self.arrange_row(row)
        dots = self.get_row_dots(row)

        return VGroup(row, dots)

    def get_v_dot_row(self):
        row = VGroup(*[
            OldTex("\\vdots")
            for x in range(self.num_terms_per_row)
        ])
        self.arrange_row(row)
        dots = self.get_row_dots(row)
        dots.fade(1)
        return VGroup(row, dots)

    def arrange_row(self, row):
        for n, part in enumerate(row):
            part.move_to(n * self.x_spacing * RIGHT)

    def get_row_dots(self, row):
        dots = VGroup()
        for p1, p2 in zip(row, row[1:]):
            dots.add(OldTex("\\cdot").move_to(VGroup(p1, p2)))
        dots.add(OldTex("\\cdots").next_to(row, RIGHT))
        return dots
