# ==============================================================================
# Scene:      HowBasisVectorMultiplicationPullsOutColumns
# Source:     videos/_2021/matrix_exp.py (lines 4061-4147)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowBasisVectorMultiplicationPullsOutColumns.py HowBasisVectorMultiplicationPullsOutColumns -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowBasisVectorMultiplicationPullsOutColumns(Scene):
    def construct(self):
        # Setup
        plane = NumberPlane()
        plane.scale(2.5)
        plane.shift(1.5 * DOWN)
        b_plane = plane.copy()
        b_plane.set_color(GREY_B)
        plane.add_coordinate_labels()
        self.add(b_plane, plane)

        matrix = Matrix(
            [["a", "b"], ["c", "d"]],
            h_buff=0.8,
        )
        matrix.to_corner(UL)
        matrix.to_edge(LEFT, buff=MED_SMALL_BUFF)
        matrix.add_to_back(BackgroundRectangle(matrix))
        self.add(matrix)

        basis_vectors = VGroup(
            Arrow(plane.get_origin(), plane.c2p(1, 0), buff=0, fill_color=GREEN),
            Arrow(plane.get_origin(), plane.c2p(0, 1), buff=0, fill_color=RED),
        )
        bhb = 0.2
        basis_labels = VGroup(
            Matrix([["1"], ["0"]], bracket_h_buff=bhb),
            Matrix([["0"], ["1"]], bracket_h_buff=bhb),
        )
        for vector, label, direction in zip(basis_vectors, basis_labels, [UR, RIGHT]):
            label.scale(0.7)
            label.match_color(vector)
            label.add_to_back(BackgroundRectangle(label))
            label.next_to(vector.get_end(), direction)

        # Show products
        basis_label_copies = basis_labels.deepcopy()
        rhss = VGroup(
            Matrix([["a"], ["c"]], bracket_h_buff=bhb),
            Matrix([["b"], ["d"]], bracket_h_buff=bhb),
        )
        colors = [GREEN, RED]

        def show_basis_product(index, matrix):
            basis_label_copies[index].match_height(matrix)
            basis_label_copies[index].next_to(matrix, RIGHT, SMALL_BUFF),
            equals = OldTex("=")
            equals.next_to(basis_label_copies[index], RIGHT, SMALL_BUFF)
            rhss[index].next_to(equals, RIGHT, SMALL_BUFF)
            rhss[index].set_color(colors[index])
            rhs_br = BackgroundRectangle(rhss[index])

            self.play(
                FadeIn(basis_labels[index], RIGHT),
                GrowArrow(basis_vectors[index]),
                FadeIn(basis_label_copies[index]),
                FadeIn(equals),
                FadeIn(rhs_br),
                FadeIn(rhss[index].get_brackets()),
            )
            rect_kw = {"stroke_width": 2, "buff": 0.1}
            row_rects = [
                SurroundingRectangle(row, **rect_kw)
                for row in matrix.get_rows()
            ]
            col_rect = SurroundingRectangle(basis_label_copies[index].get_entries(), **rect_kw)
            col_rect.set_stroke(opacity=0)
            last_row_rect = VMobject()
            for e1, e2, row_rect in zip(matrix.get_columns()[index], rhss[index].get_entries(), row_rects):
                self.play(
                    col_rect.animate.set_stroke(opacity=1),
                    FadeIn(row_rect),
                    FadeOut(last_row_rect),
                    e1.animate.set_color(colors[index]),
                    FadeIn(e2),
                )
                last_row_rect = row_rect
            self.play(FadeOut(last_row_rect), FadeOut(col_rect))
            rhss[index].add_to_back(rhs_br)
            rhss[index].add(equals)

        low_matrix = matrix.deepcopy()
        show_basis_product(0, matrix)
        self.wait()
        self.play(low_matrix.animate.shift(2.5 * DOWN))
        show_basis_product(1, low_matrix)
        self.wait()
