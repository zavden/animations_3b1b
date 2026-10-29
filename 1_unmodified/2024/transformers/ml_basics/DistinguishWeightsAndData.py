# ==============================================================================
# Scene:      DistinguishWeightsAndData
# Source:     videos/_2024/transformers/ml_basics.py (lines 1666-1811)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl DistinguishWeightsAndData.py DistinguishWeightsAndData -w -m --fps 15
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



# ----- From _2024/transformers/ml_basics.py -----

class DistinguishWeightsAndData(InteractiveScene):
    def construct(self):
        # Set up titles
        weights_title, data_title = titles = VGroup(
            Text(word, font_size=60)
            for word in ["Weights", "Data"]
        )
        weights_title.set_color(BLUE)
        data_title.set_color(GREY_B)

        for title, sign in zip(titles, [-1, 1]):
            title.set_x(sign * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=0.25)
            underline = Underline(title, stretch_factor=1.5)
            underline.match_color(title)
            underline.set_y(title[0].get_y(DOWN) - 0.1)
            title.add(underline)

        v_line = Line(UP, DOWN).set_height(4.5)
        v_line.to_edge(UP, buff=0)
        v_line.set_stroke(GREY_A, 2)

        # Set up matrices
        matrices = VGroup(
            WeightMatrix(
                shape=(6, 8),
                ellipses_row=None,
                ellipses_col=None,
            )
            for n in range(4)
        )
        matrices.arrange_in_grid(v_buff=1, h_buff=1)
        vectors = VGroup(
            NumericEmbedding(length=8, ellipses_row=None)
            for n in range(8)
        )
        vectors.arrange(RIGHT)

        tensors = VGroup(matrices, vectors)
        for group, title in zip(tensors, titles):
            group.set_height(2.5)
            group.next_to(title, DOWN, buff=0.5)

        # Mix up all the numbers
        mat_nums = VGroup(
            elem
            for matrix in matrices
            for elem in matrix.get_entries()
        )
        mat_braces = VGroup(
            brace
            for matrix in matrices
            for brace in matrix.get_brackets()
        )
        vec_nums = VGroup(
            elem
            for vector in vectors
            for elem in vector.get_entries()
        )
        vec_braces = VGroup(
            brace
            for vector in vectors
            for brace in vector.get_brackets()
        )

        def random_point(x_min, x_max, y_min, y_max):
            return np.array([
                random.uniform(x_min, x_max),
                random.uniform(y_min, y_max),
                0
            ])

        all_nums = VGroup(*mat_nums, *vec_nums)
        all_nums.shuffle()
        for num in all_nums:
            states = num.replicate(4)
            for state in states[1:]:
                state.set_height(0.15)
            sign = 1 if num in vec_nums else -1
            states[1].move_to(random_point(6.5 * sign, 1 * sign, 0, 3.5))
            states[2].move_to(random_point(-8, 8, -4, 4))
            states[3].move_to(random_point(-8, 8, -4, 4))
            states[3].set_opacity(0)
            num.states = states
            num.become(states[3])

        self.add(all_nums)

        # Animations
        lag_ratio = 1 / len(all_nums)
        self.play(
            LaggedStart(
                (Transform(num, num.states[2], path_arc=PI)
                for num in all_nums),
                lag_ratio=lag_ratio,
                run_time=3
            ),
        )
        self.wait()
        self.play(
            LaggedStart(
                (LaggedStart(
                    (Transform(num, num.states[1])
                    for num in group),
                    lag_ratio=lag_ratio,
                    run_time=2
                )
                for group in [mat_nums, vec_nums]),
                lag_ratio=0.5
            ),
            ShowCreation(v_line),
        )
        self.play(
            Write(weights_title),
            LaggedStart(
                (Transform(num, num.states[0])
                for num in mat_nums),
                lag_ratio=lag_ratio,
                run_time=2
            ),
            FadeIn(mat_braces, lag_ratio=0.1, time_span=(1, 2)),
        )
        self.play(
            Write(data_title),
            LaggedStart(
                (Transform(num, num.states[0])
                for num in vec_nums),
                lag_ratio=lag_ratio,
                run_time=2
            ),
            FadeIn(vec_braces, lag_ratio=0.1, time_span=(1, 2)),
        )
        self.wait()

        # Add subtitles
        subtitles = VGroup(
            Text("What defines the model", font_size=40),
            Text("What the model processes", font_size=40),
        )
        for subtitle, title, group in zip(subtitles, titles, tensors):
            subtitle.next_to(title, DOWN)
            self.play(
                FadeIn(subtitle, lag_ratio=0.1),
                group.animate.next_to(subtitle, DOWN, buff=0.5),
            )
            self.wait()
