# ==============================================================================
# Scene:      ManyTypesOfUpdates
# Source:     videos/_2024/transformers/attention.py (lines 3361-3500)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ManyTypesOfUpdates.py ManyTypesOfUpdates -w -m --fps 15
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



# ----- From _2024/transformers/embedding.py -----

def break_into_pieces(phrase_mob: Text, offsets: list[int]):
    phrase = phrase_mob.get_string()
    lhs = offsets
    rhs = [*offsets[1:], len(phrase)]
    result = []
    for lh, rh in zip(lhs, rhs):
        substr = phrase[lh:rh]
        start = phrase_mob.substr_to_path_count(phrase[:lh])
        end = start + phrase_mob.substr_to_path_count(substr)
        result.append(phrase_mob[start:end])
    return VGroup(*result)


def break_into_words(phrase_mob):
    offsets = [m.start() for m in re.finditer(" ", phrase_mob.get_string())]
    return break_into_pieces(phrase_mob, [0, *offsets])


def get_piece_rectangles(
    phrase_pieces,
    h_buff=0.05,
    v_buff=0.1,
    fill_opacity=0.15,
    fill_color=None,
    stroke_width=1,
    stroke_color=None,
    hue_range=(0.5, 0.6),
    leading_spaces=False,
):
    rects = VGroup()
    height = phrase_pieces.get_height() + 2 * v_buff
    last_right_x = phrase_pieces.get_x(LEFT)
    for piece in phrase_pieces:
        left_x = last_right_x if leading_spaces else piece.get_x(LEFT)
        right_x = piece.get_x(RIGHT)
        fill = random_bright_color(hue_range) if fill_color is None else fill_color
        stroke = fill if stroke_color is None else stroke_color
        rect = Rectangle(
            width=right_x - left_x + 2 * h_buff,
            height=height,
            fill_color=fill,
            fill_opacity=fill_opacity,
            stroke_color=stroke,
            stroke_width=stroke_width
        )
        if leading_spaces:
            rect.set_x(left_x, LEFT)
        else:
            rect.move_to(piece)
        rect.set_y(0)
        rects.add(rect)

        last_right_x = right_x

    rects.match_y(phrase_pieces)
    return rects



# ----- From _2024/transformers/attention.py -----

class ManyTypesOfUpdates(InteractiveScene):
    def construct(self):
        # Add matrices
        shapes = [(4, 8), (4, 8), (8, 4), (4, 8)]
        names = ["W_Q", "W_K", R"\uparrow W_V", R"\downarrow W_V"]
        colors = [YELLOW, TEAL, RED_B, RED_C]

        matrices = VGroup(
            WeightMatrix(shape=shape)
            for shape in shapes
        )
        buff_ratio = 0.35
        matrices.arrange(RIGHT, buff=matrices[0].get_width() * buff_ratio)
        matrices[-1].next_to(matrices[-2], RIGHT, buff=matrices[-2].get_width() * 0.1)
        matrices.center()
        matrices.set_width(FRAME_WIDTH - 2)
        matrices.to_edge(UP, buff=1.0)
        titles = VGroup(
            Tex(name).set_color(color).match_x(mat).to_edge(UP, buff=MED_SMALL_BUFF)
            for name, color, mat in zip(names, colors, matrices)
        )
        for title in titles[2:]:
            title[0].next_to(title[1], LEFT, buff=0.5 * SMALL_BUFF)

        self.add(matrices, titles)

        # Add phrase
        phrase = Text("John hit the brakes sharply, they screeched loudly, and he jolted forward.")
        raw_words = break_into_words(phrase)
        rects = get_piece_rectangles(raw_words)
        rects.fade(0.5)
        words = VGroup(VGroup(*pair) for pair in zip(rects, raw_words))
        words.set_width(FRAME_WIDTH - 1)
        words.center().set_y(-2)

        self.add(words)

        labels = index_labels(words)
        labels.shift(0.5 * DOWN)

        # Set up association types
        attention_types = [
            (
                "Adverb to verb",
                [
                    (1, 4, 1.0), 
                    (6, 7, 1.0), 
                ]
            ),
            (
                "Subject to verb",
                [
                    (0, 1, 1.0),
                    (3, 6, 0.5),
                    (5, 6, 0.5),
                    (0, 10, 0.5),
                    (9, 10, 0.5),
                ],
            ),
            (
                "Antecedent to pronoun",
                [
                    (0, 9, 1.0),
                    (3, 5, 1.0),
                ]
            ),
            (
                "Related to the subject",
                [
                    (0, 1, 0.25),
                    (0, 3, 0.25),
                    (0, 9, 0.2),
                    (0, 10, 0.2),
                    (0, 11, 0.2),
                ]
            ),
            (
                "Related to the object",
                [
                    (3, 4, 0.2),
                    (3, 5, 0.5),
                    (3, 6, 0.35),
                    (3, 7, 0.2),
                ]
            ),
        ]

        # Animate
        last_group = VGroup()
        for description, connections in attention_types:
            desc = Text(description)
            desc.center()
            connections = VGroup(
                Line(
                    words[i].get_top(),
                    words[j].get_top(),
                    path_arc=-PI / 2,
                    stroke_color=random_bright_color(
                        hue_range=(0.3, 0.5),
                        luminance_range=(0.5, 0.7),
                    ),
                    stroke_opacity=strength**0.5,
                )
                for (i, j, strength) in connections
            )
            connections.set_stroke(width=(0, 5, 5, 5, 0))
            connections.shuffle()
            self.play(
                FadeOut(last_group),
                # FadeIn(desc, shift=0.25 * UP),
                ShowCreation(connections, lag_ratio=0.25, run_time=0.5 * len(connections)),
                LaggedStart(
                    (self.get_matrix_update_anim(mat)
                    for mat in matrices),
                    lag_ratio=0.15,
                ),
                LaggedStart(
                    (VShowPassingFlash(
                        line.copy().insert_n_curves(100).set_stroke(width=10),
                        time_width=2.0,
                        run_time=2,
                    )
                    for line in connections),
                    lag_ratio=0.1,
                )
            )
            self.wait(2)
            # last_group = VGroup(desc, connections)
            last_group = VGroup(connections)

    def get_matrix_update_anim(self, matrix):
        rects = VGroup(
            Underline(entry, buff=0.05)
            for entry in matrix.get_entries()
        )
        rects.set_stroke(WHITE, 1)
        return AnimationGroup(
            LaggedStartMap(ShowCreationThenFadeOut, rects, lag_ratio=1e-2),
            RandomizeMatrixEntries(matrix)
        )
