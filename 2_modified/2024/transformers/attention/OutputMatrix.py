# ==============================================================================
# Scene:      OutputMatrix
# Source:     videos/_2024/transformers/attention.py (lines 3897-4033)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl OutputMatrix.py OutputMatrix -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - FillArrow no longer exists: Arrow (the current filled arrow) is used with thickness 1.7 (0.025 / 0.015)
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



# ----- From _2024/transformers/attention.py -----

class OutputMatrix(InteractiveScene):
    def construct(self):
        # Set up all heads
        matrix_pairs = VGroup(self.get_factored_value_map() for x in range(3))
        matrix_pairs.arrange(RIGHT, buff=LARGE_BUFF)
        matrix_pairs.to_edge(LEFT)
        matrix_pairs.set_y(1)
        dots = Tex(R"\dots", font_size=120)
        dots.next_to(matrix_pairs, RIGHT, LARGE_BUFF)

        rects = VGroup(SurroundingRectangle(pair, buff=0.25) for pair in matrix_pairs)
        rects.set_stroke(RED, 2)
        labels = VGroup()
        for n, rect in enumerate(rects, start=1):
            rect.set_height(2.5, stretch=True, about_edge=UP)
            rect.round_corners(radius=0.1)
            label = Text(f"Head {n}\nValue map", font_size=36)
            label.next_to(rect, UP)
            labels.add(label)

        up_labels = VGroup()
        down_labels = VGroup()
        for n, pair in enumerate(matrix_pairs, start=1):
            up_mat, down_mat = pair
            down_label = TexText(Rf"Value$^{{({n})}}_{{\downarrow}}$", font_size=30)
            up_label = TexText(Rf"Value$^{{({n})}}_{{\uparrow}}$", font_size=30)
            for label, mat, v in zip([up_label, down_label], pair, [ORIGIN, 0.25 * RIGHT]):
                label.next_to(pair, DOWN, buff=0.5)
                label[-1].scale(1.5, about_edge=UL)
                label.match_x(mat)
                label.shift(v)
                # CHANGE: FillArrow no longer exists in manimgl; Arrow is now the filled arrow (thickness 0.025 -> 1.7, the scale is 0.015)
                arrow = Arrow(label[2], mat, thickness=1.7)
                arrow.scale(0.6)
                label.add(arrow)

            up_labels.add(up_label)
            down_labels.add(down_label)

        up_labels.set_fill(RED_B)
        down_labels.set_fill(RED_C)

        # Animate
        for pair, rect, label, up_label, down_label in zip(matrix_pairs, rects, labels, up_labels, down_labels):
            mat_labels =VGroup(up_label, down_label)
            self.play(
                FadeIn(label, 0.25 * UP),
                LaggedStartMap(FadeIn, pair, scale=1.25, lag_ratio=0.5),
                LaggedStartMap(FadeIn, mat_labels, lag_ratio=0.5),
                ShowCreation(rect),
            )
        self.play(Write(dots))
        self.wait()

        # Aggregate into the output matrix
        up_matrices = VGroup(pair[0] for pair in matrix_pairs)
        stapled_up_matrices = up_matrices.copy()
        for mat in stapled_up_matrices:
            brackets = mat[-2:]
            brackets[0].stretch(0, 0, about_edge=RIGHT)
            brackets[1].stretch(0, 0, about_edge=LEFT)
            brackets.set_opacity(0)
        stapled_up_matrices.arrange(RIGHT, buff=SMALL_BUFF)
        stapled_up_matrices.scale(2)
        stapled_up_matrices.next_to(rects, DOWN, buff=1.5)

        up_labels.target = up_labels.generate_target()
        lines = VGroup()
        for stum, up_label in zip(stapled_up_matrices, up_labels.target):
            line = Line(UP, DOWN).match_height(stum)
            line.set_stroke(WHITE, 1)
            line.next_to(stum, RIGHT, buff=SMALL_BUFF / 2)
            lines.add(line)
            up_label[-1].set_opacity(0)
            up_label[-1].scale(0, about_edge=DOWN)
            up_label.scale(0.75)
            up_label.next_to(stum, UP, buff=SMALL_BUFF)

        out_dots = dots.copy()
        out_dots.scale(0.5)
        out_dots.next_to(lines, RIGHT)
        out_brackets = up_matrices[0].get_brackets().copy()
        out_brackets.match_height(stapled_up_matrices)
        out_brackets[0].next_to(stapled_up_matrices, LEFT, SMALL_BUFF)
        out_brackets[1].next_to(out_dots, RIGHT, SMALL_BUFF)

        out_matrix = VGroup(stapled_up_matrices, lines, out_dots, out_brackets)

        self.play(
            self.frame.animate.reorient(0, 0, 0, (-0.88, -0.87, 0.0), 8.00),
            up_matrices.animate.set_opacity(0.5),
            TransformFromCopy(up_matrices, stapled_up_matrices, lag_ratio=1e-4),
            MoveToTarget(up_labels),
            TransformFromCopy(dots, out_dots),
            FadeIn(lines, lag_ratio=0.5),
            FadeIn(out_brackets, scale=1.25),
            run_time=2
        )
        self.wait()

        # Circle and label output
        out_rect = SurroundingRectangle(VGroup(out_matrix, up_labels), buff=MED_SMALL_BUFF)
        out_rect.round_corners(radius=0.1)
        out_rect.set_stroke(PINK, 3)
        out_label = Text("Output\nmatrix")
        out_label.set_color(PINK)
        out_label.next_to(out_rect, LEFT)

        self.play(
            ShowCreation(out_rect),
            FadeIn(out_label, shift=0.25 * LEFT, scale=1.25),
        )
        self.wait()

        # Center the down matrices
        self.play(
            LaggedStart(
                (pair[1].animate.shift(0.5 * LEFT)
                for pair in matrix_pairs),
                lag_ratio=0.05,
            ),
            LaggedStart(
                (label.animate.shift(0.5 * LEFT)
                for label in down_labels),
                lag_ratio=0.05,
            ),
            LaggedStartMap(FadeOut, up_matrices)
        )
        self.wait()

    def get_factored_value_map(self, big_d=7, lil_d=4, height=1.0):
        matrices = VGroup(
            WeightMatrix(shape=(big_d, lil_d)),
            WeightMatrix(shape=(lil_d, big_d)),
        )
        matrices.arrange(RIGHT, buff=matrices[0].get_width() * 0.1)
        matrices.set_height(height)
        return matrices
