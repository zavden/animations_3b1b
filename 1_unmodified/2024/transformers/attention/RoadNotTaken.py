# ==============================================================================
# Scene:      RoadNotTaken
# Source:     videos/_2024/transformers/attention.py (lines 1548-1712)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl RoadNotTaken.py RoadNotTaken -w -m --fps 15
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

class RoadNotTaken(InteractiveScene):
    def construct(self):
        # Add poem
        stanza_strs = [
            """
                Two roads diverged in a yellow wood,
                And sorry I could not travel both
                And be one traveler, long I stood
                And looked down one as far as I could
                To where it bent in the undergrowth;
            """,
            """
                Then took the other, as just as fair,
                And having perhaps the better claim,
                Because it was grassy and wanted wear;
                Though as for that the passing there
                Had worn them really about the same,
            """,
            """
                And both that morning equally lay
                In leaves no step had trodden black.
                Oh, I kept the first for another day!
                Yet knowing how way leads on to way,
                I doubted if I should ever come back.
            """,
            """
                I shall be telling this with a sigh
                Somewhere ages and ages hence:
                Two roads diverged in a wood, and I—
                I took the one less traveled by,
                And that has made all the difference.
            """,
        ]
        poem = Text("\n\n".join(stanza_strs), alignment="LEFT")
        stanzas = VGroup(poem[stanza_str][0] for stanza_str in stanza_strs)
        stanzas.arrange_in_grid(h_buff=1.5, v_buff=1.0, fill_rows_first=False)
        stanzas.set_width(FRAME_WIDTH - 1)
        stanzas.move_to(0.5 * UP)
        poem.refresh_bounding_box(recurse_down=True)

        self.play(FadeIn(poem, lag_ratio=0.01, run_time=4))
        self.wait()

        # Note all text until "one"
        rect = SurroundingRectangle(poem)
        less = poem["less"][-1]
        one = poem["one"][-1]
        diff_rects = VGroup(
            SurroundingRectangle(mob).scale(10, about_edge=UL)
            for mob in [less, poem["And"][-1]]
        )
        for diff_rect in diff_rects:
            rect = Difference(rect, diff_rect)
        rect.set_stroke(TEAL, 3)

        less_index = poem.submobjects.index(less[0])
        faded_portion = poem[less_index:]
        active_portion = poem[:less_index]
        less_rect = SurroundingRectangle(less)
        less_rect.set_stroke(YELLOW, 3)
        one_rect = SurroundingRectangle(one)
        one_rect.become(Difference(one_rect, less_rect))
        one_rect.match_height(less_rect, about_edge=DOWN, stretch=True)
        one_rect.set_stroke(BLUE, 3)
        arrow = Vector(0.75 * UP)
        arrow.next_to(one, DOWN, SMALL_BUFF)
        arrow.set_stroke(YELLOW)
        active_portion_copy = active_portion.copy()
        active_portion_copy.set_color(TEAL_B)

        self.play(
            FadeIn(rect),
            Write(active_portion_copy, run_time=2, stroke_color=TEAL, lag_ratio=0.01),
            faded_portion.animate.set_fill(opacity=0.5),
        )
        self.play(FadeOut(active_portion_copy))
        self.wait()
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(
            ShowCreation(less_rect),
            less.animate.set_fill(opacity=1),
            arrow.animate.match_x(less),
        )
        self.wait()
        self.remove(less_rect)
        self.play(
            arrow.animate.match_x(one),
            TransformFromCopy(less_rect, one_rect),
        )
        self.wait()

        # Highlight "two roads"
        one = one.copy()
        less = less.copy()
        two_roads = poem["Two roads"][-1].copy()
        took_the = poem["I took the"][-1].copy()

        self.play(
            FadeIn(two_roads, lag_ratio=0.1),
            FadeIn(took_the, lag_ratio=0.1),
            FadeIn(one),
            arrow.animate.rotate(-PI / 2).next_to(two_roads, LEFT, SMALL_BUFF),
            poem.animate.set_fill(opacity=0.5),
            run_time=1.5
        )
        self.wait()

        # Highlight "took the other" and "grassy and wanted wear"
        top_two_roads = poem["Two roads diverged"][0].copy()
        took_other = poem["Then took the other"][0].copy()
        wanted_wear = poem["it was grassy and wanted wear"][0].copy()
        for phrase in [top_two_roads, took_other, wanted_wear]:
            phrase.set_fill(WHITE, 1)

        self.play(
            arrow.animate.rotate(PI / 2).next_to(top_two_roads, DOWN, SMALL_BUFF),
            FadeIn(top_two_roads),
        )
        self.wait()
        self.play(
            arrow.animate.rotate(3 * PI / 4).next_to(took_other, UP, SMALL_BUFF),
            FadeIn(took_other)
        )
        self.wait()
        self.play(
            arrow.animate.rotate(-PI / 2).next_to(wanted_wear, DOWN, SMALL_BUFF),
            FadeIn(wanted_wear)
        )
        self.wait()

        # Higlight words throughout
        active_portion_copy.set_fill(YELLOW_A, 1)

        self.play(
            LaggedStart(
                (FadeIn(char, rate_func=there_and_back_with_pause)
                for char in active_portion_copy),
                lag_ratio=0.005,
                run_time=6
            )
        )
        self.wait()

        # Show less again
        self.play(
            arrow.animate.rotate(-PI / 4).next_to(less, DOWN, SMALL_BUFF),
            ShowCreation(less_rect),
            less.animate.set_fill(WHITE, 1)
        )
        self.wait()

        # Show final embedding
        frame = self.frame
        embedding = NumericEmbedding(length=10)
        embedding.set_height(3)
        embedding.next_to(one, DOWN, buff=arrow.get_length() + 2 * SMALL_BUFF)

        self.play(
            arrow.animate.rotate(PI).next_to(one, DOWN, SMALL_BUFF).set_anim_args(path_arc=PI),
            frame.animate.set_height(9).move_to(DOWN)
        )
        self.play(TransformFromCopy(one, embedding))
        self.play(RandomizeMatrixEntries(embedding))
        self.wait()
