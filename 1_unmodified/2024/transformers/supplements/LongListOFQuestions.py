# ==============================================================================
# Scene:      LongListOFQuestions
# Source:     videos/_2024/transformers/supplements.py (lines 239-303)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl LongListOFQuestions.py LongListOFQuestions -w -m --fps 15
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



# ----- From _2024/transformers/supplements.py -----

class LongListOFQuestions(InteractiveScene):
    def construct(self):
        # Add word and vector
        word = Text("Queen")
        arrow = Vector(0.75 * RIGHT)
        vector = NumericEmbedding(length=12)
        vector.set_height(5)
        word_group = VGroup(word, arrow, vector)
        word_group.arrange(RIGHT, buff=0.15)
        word_group.to_edge(LEFT, buff=2.0)

        self.add(word_group)

        # Add neurons and questions
        questions = VGroup(map(Text, [
            "Is it English?",
            "Is it a noun?",
            "Does it refer to a person?",
            "Is it an amount?",
            "Is A tone assertive",
            "Is it a piece of a bigger word?",
            "Is it part of a quote?",
            "Is it part of a lie?",
        ]))
        questions.scale(0.75)
        n_questions = len(questions)
        neurons = VGroup(Circle(radius=0.2) for n in range(n_questions))
        neurons.add(Tex(R"\vdots", font_size=72))
        neurons.arrange_in_grid(n_questions, 1, buff_ratio=0.5)
        neurons.set_height(6)
        neurons.set_stroke(WHITE, 1)
        neurons.next_to(vector, RIGHT, buff=3.0)
        values = [0.9, 0.8, 0.85, 0.1, 0.5, 0.05, 0.2, 0.02]
        for neuron, question, value in zip(neurons, questions, values):
            neuron.set_fill(WHITE, value)
            question.next_to(neuron, RIGHT)

        # Add connections
        connections = VGroup(
            VGroup(
                Line(
                    elem.get_right(), neuron.get_center(),
                    buff=neuron.get_width() / 2
                ).set_stroke(
                    color=value_to_color(random.uniform(-10, 10)),
                    width=2 * random.random()
                )
                for elem in vector.get_entries()
            )
            for neuron in neurons[:-1]
        )

        # Animate
        lag_ratio = 0.3
        self.play(
            LaggedStart(
                (ShowCreation(line_group, lag_ratio=0)
                for line_group in connections),
                lag_ratio=lag_ratio,
            ),
            LaggedStartMap(FadeIn, neurons, lag_ratio=lag_ratio),
            LaggedStartMap(FadeIn, questions, lag_ratio=lag_ratio),
            run_time=4
        )
        self.wait()
