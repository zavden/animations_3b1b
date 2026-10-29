# ==============================================================================
# Scene:      HighDimensionalSpaceCompanion
# Source:     videos/_2024/transformers/embedding.py (lines 906-1016)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl HighDimensionalSpaceCompanion.py HighDimensionalSpaceCompanion -w -m --fps 15
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



# ----- From _2024/transformers/embedding.py -----

class HighDimensionalSpaceCompanion(InteractiveScene):
    def construct(self):
        # Vector example
        word = Text("bank")
        vect = WeightMatrix(shape=(8, 1))
        vect.next_to(word, RIGHT, buff=LARGE_BUFF)
        vect.set_height(3)
        arrow = Arrow(word, vect)
        group = VGroup(word, arrow, vect)
        group.move_to(RIGHT)
        group.to_edge(UP, buff=0.1)
        self.add(group)

        # Draw vague embedding space
        bubble_center = np.array([0.5, -2.25, 0])
        base_bubble: VMobject = OldThoughtBubble()[-2][-1]
        base_bubble.set_shape(8, 7)
        base_bubble.rotate(PI)
        base_bubble.set_fill(GREY_D, opacity=[0.25, 1, 0.25])
        base_bubble.move_to(bubble_center)
        bubble_label = Text("Word vector space", font_size=60)
        bubble_label.move_to(base_bubble)
        bubble_label.shift(2.0 * UP)
        # bubble_label = Text("Embedding space", font_size=72)
        q_marks = Tex("???", font_size=120)
        q_marks.next_to(bubble_label, DOWN, buff=0.5)
        base_bubble.add(bubble_label, q_marks)

        def get_bubble():
            result = base_bubble.copy()
            result.apply_complex_function(
                lambda z: z * (1 + 0.025 * np.cos(5 * np.log(z).imag + self.time))
            )
            result.move_to(bubble_center)
            return result

        bubble = always_redraw(get_bubble)
        self.add(bubble)
        self.wait(10)

        # Show dimension
        brace = Brace(vect, RIGHT)
        label = VGroup(
            # Integer(12288),
            Integer(10000),
            Text("coordinates")
        )
        label.arrange(DOWN, aligned_edge=LEFT)
        label.set_height(1)
        label.set_color(YELLOW)
        label.next_to(brace, RIGHT)

        dimension_label = VGroup(
            label[0].copy(),
            Text("-dimensional")
        )
        dimension_label.arrange(RIGHT, buff=0.05, aligned_edge=UP)
        dimension_label.match_height(bubble_label).scale(0.8)
        dimension_label.set_color(YELLOW)
        dimension_label.next_to(q_marks, DOWN, buff=0.5)

        self.play(
            GrowFromCenter(brace),
            CountInFrom(label[0], 0),
            FadeIn(label[1]),
        )
        self.wait()
        self.play(
            TransformFromCopy(label[0], dimension_label[0]),
            FadeInFromPoint(dimension_label[1], label[0].get_center()),
        )
        self.remove(dimension_label)
        bubble_label.add(*dimension_label)

        self.wait(10)

        # Show 3d slice
        axes = ThreeDAxes()
        axes.rotate(20 * DEGREES, OUT)
        axes.rotate(80 * DEGREES, LEFT)
        axes.set_height(3)
        axes.move_to(bubble)
        axes.shift(0.5 * RIGHT)
        axes_label = TexText("3d ``slice''")
        axes_label.next_to(axes, RIGHT)
        axes_label.shift(0.35 * DOWN + 1.5 * LEFT)

        self.play(
            bubble_label.animate.scale(0.5).shift(1.2 * UP + 1.5 * LEFT),
            FadeOut(q_marks),
            Write(axes, lag_ratio=0.01),
            Write(axes_label)
        )
        self.wait(2)

        # Show some vector projections
        vectors = VGroup(*(
            Arrow(
                axes.get_origin(),
                axes.c2p(*np.random.uniform(-3, 3, 3)),
                buff=0,
                stroke_color=random_bright_color(hue_range=(0.55, 0.65))
            )
            for x in range(5)
        ))
        vectors.set_flat_stroke(False)

        self.play(LaggedStartMap(FadeIn, vectors, scale=0.5, lag_ratio=0.3))
        z_direction = axes.z_axis.get_vector()
        axes.add(vectors)
        self.play(Rotate(axes, -200 * DEGREES, axis=z_direction, run_time=10))
