# ==============================================================================
# Scene:      CountMatrixParameters
# Source:     videos/_2024/transformers/attention.py (lines 2561-3011)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl CountMatrixParameters.py CountMatrixParameters -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/transformers/helpers.py -----

if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


def show_matrix_vector_product(scene, matrix, vector, buff=0.25, x_max=999, fix_in_frame=False):
    # Show product
    eq = Tex("=")
    eq.set_width(0.5 * vector.get_width())
    shape = (matrix.shape[0], 1)
    rhs = NumericEmbedding(
        values=x_max * np.ones(shape),
        value_range=(-x_max, x_max),
        decimal_config=dict(include_sign=True, edge_to_fix=ORIGIN),
        ellipses_row=matrix.ellipses_row,
    )
    rhs.scale(vector.elements[0].get_height() / rhs.elements[0].get_height())
    eq.next_to(vector, RIGHT, buff=buff)
    rhs.next_to(eq, RIGHT, buff=buff)
    if fix_in_frame:
        eq.fix_in_frame()
        rhs.fix_in_frame()

    scene.play(FadeIn(eq), FadeIn(rhs.get_brackets()))

    last_rects = VGroup()
    n_rows = len(matrix.rows)
    for n, row, entry in zip(it.count(), matrix.get_rows(), rhs[:-2]):
        if matrix.ellipses_row is not None and n == (matrix.ellipses_row % n_rows):
            scene.add(entry)
        else:
            last_rects = matrix_row_vector_product(
                scene, row, vector, entry, last_rects,
                fix_in_frame=fix_in_frame
            )
    scene.play(FadeOut(last_rects))

    return eq, rhs


def matrix_row_vector_product(scene, row, vector, entry, to_fade, fix_in_frame=False):
    def get_rect(elem):
        return SurroundingRectangle(elem, buff=0.1, is_fixed_in_frame=fix_in_frame).set_stroke(YELLOW, 2)

    row_rects = VGroup(*map(get_rect, row))
    vect_rects = VGroup(*map(get_rect, vector[:-2]))
    partial_values = [0]
    for e1, e2 in zip(row, vector[:-2]):
        if not isinstance(e1, DecimalNumber) and isinstance(e2, DecimalNumber):
            increment = 0
        else:
            val1 = round(e1.get_value(), e1.num_decimal_places)
            val2 = round(e2.get_value(), e2.num_decimal_places)
            increment = val1 * val2
        partial_values.append(partial_values[-1] + increment)
    n_values = len(partial_values)

    scene.play(
        ShowIncreasingSubsets(row_rects),
        ShowIncreasingSubsets(vect_rects),
        UpdateFromAlphaFunc(entry, lambda m, a: m.set_value(
            partial_values[min(int(np.round(a * n_values)), n_values - 1)]
        )),
        FadeOut(to_fade),
        rate_func=linear,
    )

    return VGroup(row_rects, vect_rects)


class WeightMatrix(DecimalMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: tuple[int, int] = (6, 8),
        value_range: tuple[float, float] = (-9.9, 9.9),
        ellipses_row: Optional[int] = -2,
        ellipses_col: Optional[int] = -2,
        num_decimal_places: int = 1,
        bracket_h_buff: float = 0.1,
        decimal_config=dict(include_sign=True),
        low_positive_color: ManimColor = BLUE_E,
        high_positive_color: ManimColor = BLUE_B,
        low_negative_color: ManimColor = RED_E,
        high_negative_color: ManimColor = RED_B,
    ):
        if values is not None:
            shape = values.shape
        self.shape = shape
        self.value_range = value_range
        self.low_positive_color = low_positive_color
        self.high_positive_color = high_positive_color
        self.low_negative_color = low_negative_color
        self.high_negative_color = high_negative_color
        self.ellipses_row = ellipses_row
        self.ellipses_col = ellipses_col

        if values is None:
            values = np.random.uniform(*self.value_range, size=shape)

        super().__init__(
            values,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
        )
        self.reset_entry_colors()

    def reset_entry_colors(self):
        for entry in self.get_entries():
            entry.set_fill(color=value_to_color(
                entry.get_value(),
                self.low_positive_color,
                self.high_positive_color,
                self.low_negative_color,
                self.high_negative_color,
                0, max(self.value_range),
            ))
        return self


class NumericEmbedding(WeightMatrix):
    def __init__(
        self,
        values: Optional[np.ndarray] = None,
        shape: Optional[Tuple[int, int]] = None,
        length: int = 7,
        num_decimal_places: int = 1,
        ellipses_row: int = -2,
        ellipses_col: int = -2,
        value_range: tuple[float, float] = (-9.9, 9.9),
        bracket_h_buff: float = 0.1,
        decimal_config=dict(include_sign=True),
        dark_color: ManimColor = GREY_C,
        light_color: ManimColor = WHITE,
        **kwargs,
    ):
        if values is not None:
            if len(values.shape) == 1:
                values = values.reshape((values.shape[0], 1))
            shape = values.shape
        if shape is None:
            shape = (length, 1)
        super().__init__(
            values,
            shape=shape,
            value_range=value_range,
            num_decimal_places=num_decimal_places,
            bracket_h_buff=bracket_h_buff,
            decimal_config=decimal_config,
            low_positive_color=dark_color,
            high_positive_color=light_color,
            low_negative_color=dark_color,
            high_negative_color=light_color,
            ellipses_row=ellipses_row,
            ellipses_col=ellipses_col,
            **kwargs,
        )

        # No sign on zeros
        for entry in self.get_entries():
            if entry.get_value() == 0:
                entry[0].set_opacity(0)


class RandomizeMatrixEntries(Animation):
    def __init__(self, matrix, **kwargs):
        self.matrix = matrix
        self.entries = matrix.get_entries()
        self.start_values = [entry.get_value() for entry in self.entries]
        self.target_values = np.random.uniform(
            matrix.value_range[0],
            matrix.value_range[1],
            len(self.entries)
        )
        super().__init__(matrix, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        for index, entry in enumerate(self.entries):
            start = self.start_values[index]
            target = self.target_values[index]
            sub_alpha = self.get_sub_alpha(alpha, index, len(self.entries))
            entry.set_value(interpolate(start, target, sub_alpha))
        self.matrix.reset_entry_colors()



# ----- From _2024/transformers/attention.py -----

class CountMatrixParameters(InteractiveScene):
    count_font_size = 36

    def construct(self):
        # Add three matrices
        d_embed = 12_288
        d_key = 128
        key_mat_shape = (5, 10)

        que_mat = WeightMatrix(shape=key_mat_shape)
        key_mat = WeightMatrix(shape=key_mat_shape)
        val_mat = WeightMatrix(shape=(key_mat_shape[1], key_mat_shape[1]))
        matrices = VGroup(que_mat, key_mat, val_mat)
        for matrix in matrices:
            matrix.set_max_width(4)

        matrices.arrange(DOWN, buff=0.75)

        colors = [YELLOW, TEAL, RED]

        titles = VGroup(Text("Query"), Text("Key"), Text("Value"))
        que_title, key_title, val_title = titles
        titles.arrange(DOWN, aligned_edge=LEFT)
        titles.next_to(matrices, LEFT, LARGE_BUFF)
        for title, matrix, color in zip(titles, matrices, colors):
            title.match_y(matrix)
            title.set_color(color)

        self.play(
            LaggedStartMap(FadeIn, titles, shift=0.25 * LEFT, lag_ratio=0.5),
            LaggedStart(
                (FadeIn(matrix, lag_ratio=1e-2)
                for matrix in matrices),
                lag_ratio=0.5,
            )
        )
        self.wait()

        # Data animations
        change_anims = [RandomizeMatrixEntries(mat) for mat in matrices]
        highlight_anims = [
            LaggedStartMap(FlashUnder, mat.get_entries(), lag_ratio=5e-3, stroke_width=1)
            for mat in matrices
        ]

        self.play(
            LaggedStart(highlight_anims, lag_ratio=0.2),
            LaggedStart(change_anims, lag_ratio=0.2),
            run_time=3
        )

        # Ask about total number of parameters
        rects = VGroup(
            SurroundingRectangle(entry, buff=0.025)
            for matrix in matrices
            for entry in matrix.get_entries()
        )
        rects.set_stroke(WHITE, 1)
        question = Text("How many\nparameters?")
        question.next_to(matrices, RIGHT, LARGE_BUFF)

        self.play(
            ShowCreation(rects, lag_ratio=5e-3, run_time=2),
            Write(question)
        )
        self.play(FadeOut(rects))
        self.wait()

        # Make room to count query/key
        value_group = VGroup(val_title, val_mat)
        value_group.save_state()
        qk_mats = matrices[:2]
        qk_mats.target = qk_mats.generate_target()
        qk_mats.target.arrange(RIGHT, buff=3.0)
        qk_mats.target.move_to(DR)

        self.play(
            FadeOut(question, DR),
            value_group.animate.scale(0.25).to_corner(DR).fade(0.25),
            MoveToTarget(qk_mats),
            que_title.animate.next_to(qk_mats.target[0], UP, buff=2.0),
            key_title.animate.next_to(qk_mats.target[1], UP, buff=2.0),
        )

        # Count up query and key
        que_col_count = self.show_column_count(que_mat, d_embed)
        key_col_count = self.show_column_count(key_mat, d_embed)
        self.wait()
        que_row_count = self.show_row_count(que_mat, d_key)
        key_row_count = self.show_row_count(key_mat, d_key)
        self.wait()

        que_product = self.show_product(
            que_col_count, que_row_count,
            added_anims=[que_title.animate.shift(UP)]
        )
        key_product = self.show_product(
            key_col_count, key_row_count,
            added_anims=[key_title.animate.shift(UP)]
        )
        self.wait()

        # Pull up the value matrix
        qk_titles = titles[:2]
        qk_titles.target = qk_titles.generate_target()
        qk_titles.target.arrange(DOWN, buff=2.0, aligned_edge=LEFT)
        qk_titles.target.to_corner(UL)
        qk_titles.target.scale(0.5, about_edge=UL)

        qk_mats.target = qk_mats.generate_target()

        qk_rhss = VGroup(que_product[-1], key_product[-1]).copy()
        qk_rhss.target = qk_rhss.generate_target()

        for mat, title, rhs in zip(qk_mats.target, qk_titles.target, qk_rhss.target):
            rhs.scale(0.5)
            mat.scale(0.5)
            rhs.next_to(title, DOWN, SMALL_BUFF, aligned_edge=LEFT)
            mat.next_to(VGroup(title, rhs), RIGHT, buff=MED_LARGE_BUFF)

        self.play(
            MoveToTarget(qk_titles),
            MoveToTarget(qk_mats),
            MoveToTarget(qk_rhss),
            FadeOut(VGroup(
                que_product, key_product,
                que_col_count, que_row_count,
                key_col_count, key_row_count,
            ), shift=0.5 * UL, lag_ratio=1e-3, time_span=(0, 1.0)),
            value_group.animate.restore().arrange(DOWN, buff=1.0).move_to(2.0 * RIGHT + 0.5 * DOWN),
            run_time=2,
        )
        self.wait()

        # Count up current value
        in_vect = NumericEmbedding(length=key_mat_shape[1])
        in_vect.match_height(val_mat)
        in_vect.next_to(val_mat, RIGHT, SMALL_BUFF)

        val_col_count = self.show_column_count(
            val_mat, d_embed,
            added_anims=[val_title.animate.shift(UP)]
        )
        self.play(FadeIn(in_vect))
        eq, rhs = show_matrix_vector_product(self, val_mat, in_vect)
        val_row_count = self.show_row_count(val_mat, d_embed)
        self.wait()
        val_product = self.show_product(
            val_col_count, val_row_count,
            added_anims=[val_title.animate.shift(UP)]
        )
        self.wait()

        # Compare the two
        frame = self.frame
        q_group, k_group = qk_groups = VGroup(
            VGroup(*trip)
            for trip in zip(qk_mats, qk_titles, qk_rhss)
        )
        for group, y in zip(qk_groups, [+1.25, -1.25]):
            group.save_state()
            group.target = group.generate_target()
            group.target.scale(2)
            group.target.next_to(val_mat, LEFT, buff=2.5)
            group.target.set_y(y)

        self.play(
            frame.animate.reorient(0, 0, 0, (-1.58, 0.02, 0.0), 9.22),
            LaggedStartMap(MoveToTarget, qk_groups),
        )
        self.wait()

        # Circle both
        val_rhs_rect = SurroundingRectangle(val_product[-1])
        val_rhs_rect.set_stroke(RED_B, 3)
        qk_rhs_rects = VGroup(
            SurroundingRectangle(rhs) for rhs in qk_rhss
        )
        qk_rhs_rects[0].set_stroke(YELLOW, 3)
        qk_rhs_rects[1].set_stroke(TEAL, 3)

        big_rect = FullScreenFadeRectangle()
        big_rect.scale(2)
        big_rect.set_fill(opacity=0.5)
        val_rhs_copy = val_product[-1].copy()
        qk_rhs_copies = qk_rhss.copy()

        self.add(big_rect, val_rhs_copy)
        self.play(
            FadeIn(big_rect),
            ShowCreation(val_rhs_rect)
        )
        self.wait()
        self.play(
            TransformFromCopy(VGroup(val_rhs_rect), qk_rhs_rects),
            FadeIn(qk_rhs_copies)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                big_rect, qk_rhs_copies, val_rhs_copy,
                qk_rhs_rects, val_rhs_rect
            ))
        )

        # Cross out
        cross = Cross(val_product, stroke_width=[0, 12, 0]).scale(1.1)
        self.play(LaggedStart(
            FadeOut(qk_groups, 2 * UR, scale=0.5),
            ShowCreation(cross),
            frame.animate.set_height(FRAME_HEIGHT).move_to(RIGHT),
            run_time=2,
            lag_ratio=0.1
        ))
        self.wait()
        self.play(FadeOut(val_product), FadeOut(cross))

        # Factor out
        val_down_mat = WeightMatrix(shape=key_mat_shape)
        val_up_mat = WeightMatrix(shape=(key_mat_shape[1], 4))
        val_down_mat.match_width(val_mat)
        val_up_mat.match_height(in_vect)

        val_down_mat.move_to(val_mat, RIGHT)
        val_up_mat.next_to(val_down_mat, LEFT, SMALL_BUFF)

        self.remove(val_mat)
        self.play(
            TransformFromCopy(val_mat.get_brackets(), val_down_mat.get_brackets()),
            TransformFromCopy(val_mat.get_columns(), val_down_mat.get_columns()),
            TransformFromCopy(val_mat.get_brackets(), val_up_mat.get_brackets()),
            TransformFromCopy(val_mat.get_rows(), val_up_mat.get_rows()),
            val_col_count.animate.next_to(val_down_mat, UP, SMALL_BUFF),
            val_row_count.animate.next_to(val_up_mat, LEFT, SMALL_BUFF),
        )
        self.add(val_down_mat)
        self.wait()

        # Circle the full linear map
        big_rect = SurroundingRectangle(VGroup(val_row_count, val_col_count))
        big_rect.round_corners(radius=0.25)
        big_rect.set_stroke(RED_B, 2)
        linear_map_words = Text("Linear map")
        linear_map_words.next_to(big_rect, UP)
        linear_map_words.set_color(RED_B)

        in_label, out_label = [
            VGroup(Text(text), Integer(d_embed))
            for text in ["d_input", "d_output"]
        ]
        for label, array, shift in [(in_label, in_vect, LEFT), (out_label, rhs, RIGHT)]:
            label.arrange(DOWN)
            label.scale(0.65)
            label.next_to(array, UP, buff=LARGE_BUFF)
            label.shift(0.25 * shift)
            arrow = Arrow(label, array)
            label.add(arrow)

        self.play(
            FadeIn(big_rect),
            FadeTransform(val_title, linear_map_words),
        )
        self.wait()
        self.play(FadeIn(in_label, lag_ratio=0.1))
        self.play(FadeIn(out_label, lag_ratio=0.1))
        self.wait(2)

        # Show the value_down map
        val_down_group = VGroup(val_down_mat, val_col_count)
        val_up_group = VGroup(val_up_mat, val_row_count)
        val_down_group.save_state()
        val_up_group.save_state()

        small_row_count = self.show_row_count(
            val_down_mat, d_key,
            added_anims=[val_up_group.animate.scale(0.5).to_edge(LEFT, buff=1.25).fade(0.5)]
        )
        self.wait()
        self.play(frame.animate.set_y(0.5))
        self.wait()

        value_down_rect = SurroundingRectangle(
            VGroup(small_row_count, val_down_mat, val_col_count)
        )
        value_down_rect.round_corners(radius=0.25)
        value_down_rect.set_stroke(RED_B, 2)
        value_down_title = TexText(R"Value$_\downarrow$")
        value_down_title.set_fill(RED_B)
        value_down_title.next_to(val_down_mat, DOWN)

        self.remove(big_rect)
        self.play(
            TransformFromCopy(big_rect, value_down_rect),
            FadeOut(linear_map_words),
            FadeIn(value_down_title, DOWN)
        )
        self.wait()

        # Show value_up map
        small_row_count.target = small_row_count.generate_target()
        small_row_count.target.rotate(-PI / 2)
        small_row_count.target[1].rotate(PI / 2)
        small_row_count.target[0].stretch_to_fit_width(val_up_group.saved_state[0].get_width())
        small_row_count.target[1].next_to(small_row_count.target[0], UP, SMALL_BUFF)
        small_row_count.target.next_to(val_up_group.saved_state[0], UP, SMALL_BUFF)
        big_rect.set_height(3.9, stretch=True)
        big_rect.align_to(VGroup(val_down_mat, val_up_group.saved_state), DR)
        big_rect.shift(0.8 * DOWN + 0.05 * RIGHT)
        linear_map_words.next_to(big_rect, UP)

        value_up_title = TexText(R"Value$_\uparrow$")
        value_up_title.set_fill(RED_B)
        value_up_title.next_to(val_up_group.saved_state[0], DOWN)

        self.play(LaggedStart(
            val_down_group.animate.fade(0.5),
            value_down_title.animate.fade(0.5),
            ReplacementTransform(value_down_rect, big_rect),
            Restore(val_up_group),
            MoveToTarget(small_row_count),
            FadeIn(linear_map_words, shift=0.5 * UP),
            run_time=2,
        ))
        val_up_group.add(small_row_count)
        self.wait()
        self.play(TransformFromCopy(value_down_title, value_up_title))
        self.wait()

        # Low rank label
        low_rank_words = TexText("``Low rank'' transformation")
        low_rank_words.next_to(big_rect, UP)
        low_rank_words.shift(0.5 * LEFT)
        self.play(
            val_down_group.animate.set_fill(opacity=1),
            value_down_title.animate.set_fill(opacity=1),
            FadeTransform(linear_map_words, low_rank_words)
        )
        self.wait()

    def scrap(self):
        # Label the value matrix
        tiny_buff = 0.025
        value_rect = SurroundingRectangle(val_down_group, buff=tiny_buff)
        value_rect.stretch(1.2, 1)
        value_rect.round_corners(0.1)
        value_rect.set_stroke(RED, 3)
        value_arrow = Vector(DOWN)
        value_arrow.match_color(value_rect)
        value_arrow.next_to(value_rect, UP, SMALL_BUFF)

        val_up_group.save_state()
        out_rect = SurroundingRectangle(val_up_group, buff=tiny_buff)
        out_rect.set_height(big_rect.get_height() - SMALL_BUFF, stretch=True)
        out_rect.match_y(big_rect)
        out_rect.round_corners(0.1)
        out_rect.set_stroke(PINK, 3)
        out_arrow = Vector(0.5 * DOWN)
        out_arrow.next_to(out_rect, UP, SMALL_BUFF)
        out_arrow.match_color(out_rect)
        output_title = TexText("Output$^{*}$")
        output_title.match_color(out_rect)
        output_title.next_to(out_arrow, UP, SMALL_BUFF)


        self.play(LaggedStart(
            Restore(val_down_group),
            LaggedStartMap(FadeOut, VGroup(in_label, out_label)),
            TransformFromCopy(big_rect, value_rect),
            FadeOut(linear_map_words),
            val_title.animate.next_to(value_arrow, UP, SMALL_BUFF),
            FadeIn(value_arrow, shift=DOWN),
            val_up_group.animate.fade(0.5),
        ))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(big_rect, out_rect),
            TransformFromCopy(value_arrow, out_arrow),
            FadeTransform(val_title.copy(), output_title),
            Restore(val_up_group),
        ))
        self.wait()

    def show_column_count(self, matrix, count, added_anims=[]):
        cols = matrix.get_columns()
        col_rects = VGroup(SurroundingRectangle(cols[0], buff=0).match_x(col) for col in cols)
        col_rects.set_stroke(WHITE, 1, 0.5)
        col_rects.set_fill(GREY_D, 0.5)
        top_brace = Brace(col_rects, UP, buff=SMALL_BUFF)
        count_mob = Integer(count, font_size=self.count_font_size)
        count_mob.next_to(top_brace, UP)

        self.play(
            GrowFromCenter(top_brace),
            CountInFrom(count_mob, 0),
            FadeIn(col_rects, lag_ratio=0.25),
            *added_anims,
        )
        self.play(FadeOut(col_rects))
        return VGroup(top_brace, count_mob)

    def show_row_count(self, matrix, count, added_anims=[]):
        rows = matrix.get_rows()
        row_rects = VGroup(SurroundingRectangle(rows[0], buff=0).match_y(row) for row in rows)
        row_rects.set_stroke(WHITE, 1, 0.5)
        row_rects.set_fill(GREY_D, 0.5)
        left_brace = Brace(matrix, LEFT, buff=SMALL_BUFF)
        count_mob = Integer(count, font_size=self.count_font_size)
        count_mob.next_to(left_brace, LEFT)

        self.play(
            GrowFromCenter(left_brace),
            CountInFrom(count_mob, 0),
            FadeIn(row_rects, lag_ratio=0.25),
            *added_anims,
        )
        self.play(FadeOut(row_rects))
        return VGroup(left_brace, count_mob)

    def show_product(self, col_count, row_count, added_anims=[]):
        col_dec = col_count[1]
        row_dec = row_count[1]
        prod_dec = Integer(
            col_dec.get_value() * row_dec.get_value(),
            font_size=self.count_font_size
        )

        equation = VGroup(
            row_dec.copy(),
            Tex(R"\times", font_size=self.count_font_size),
            col_dec.copy(),
            Tex(R"=", font_size=self.count_font_size),
            prod_dec
        )
        equation.arrange(RIGHT,buff=SMALL_BUFF)
        for index in [0, 2]:
            equation[index].align_to(equation[4], UP)
        equation.next_to(col_dec, UP, buff=1.0)

        self.play(
            TransformFromCopy(row_dec, equation[0]),
            FadeIn(equation[1]),
            TransformFromCopy(col_dec, equation[2]),
            FadeIn(equation[3]),
            *added_anims
        )
        self.play(
            FadeTransform(equation[0].copy(), equation[4]),
            FadeTransform(equation[2].copy(), equation[4]),
        )
        self.add(equation)
        return equation
