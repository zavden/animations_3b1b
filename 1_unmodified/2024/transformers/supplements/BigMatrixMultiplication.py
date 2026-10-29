# ==============================================================================
# Scene:      BigMatrixMultiplication
# Source:     videos/_2024/transformers/supplements.py (lines 220-236)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl BigMatrixMultiplication.py BigMatrixMultiplication -w -m --fps 15
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



# ----- From _2024/transformers/supplements.py -----

class BigMatrixMultiplication(InteractiveScene):
    mat_dims = (12, 12)
    random_seed = 9

    def construct(self):
        # Test
        matrix = WeightMatrix(shape=self.mat_dims)
        matrix.set_width(FRAME_WIDTH - 4)
        matrix.to_edge(LEFT, buff=0.5)
        vector = NumericEmbedding(length=self.mat_dims[0])
        vector.match_height(matrix)
        vector.next_to(matrix, RIGHT)

        self.add(matrix)
        self.add(vector)
        show_matrix_vector_product(self, matrix, vector)
        self.wait()
