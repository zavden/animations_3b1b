# ==============================================================================
# Scene:      MyseteryNovel
# Source:     videos/_2024/transformers/attention.py (lines 1453-1545)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl MyseteryNovel.py MyseteryNovel -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR now points to _lib/data (get_directories()["data"]) instead of Grant's output folder (GloVe, placeholder texts)
#   - FillArrow no longer exists: Arrow (the current filled arrow) is used with thickness 4.7 (0.07 / 0.015)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING
from pathlib import Path


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")


if TYPE_CHECKING:
    from typing import Optional
    from manimlib.typing import Vect3, ManimColor


def get_paragraph(words, line_len=40, font_size=48):
    """
    Handle word wrapping
    """
    words = list(map(str.strip, words))
    word_lens = list(map(len, words))
    lines = []
    lh, rh = 0, 0
    while rh < len(words):
        rh += 1
        if sum(word_lens[lh:rh]) > line_len:
            rh -= 1
            lines.append(words[lh:rh])
            lh = rh
    lines.append(words[lh:])
    text = "\n".join([" ".join(line).strip() for line in lines])
    return Text(text, alignment="LEFT", font_size=font_size)


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


class ContextAnimation(LaggedStart):
    def __init__(
        self,
        target,
        sources,
        direction=UP,
        hue_range=(0.1, 0.3),
        time_width=2,
        min_stroke_width=0,
        max_stroke_width=5,
        lag_ratio=None,
        strengths=None,
        run_time=3,
        fix_in_frame=False,
        path_arc=PI / 2,
        **kwargs,
    ):
        arcs = VGroup()
        if strengths is None:
            strengths = np.random.random(len(sources))**2
        for source, strength in zip(sources, strengths):
            sign = direction[1] * (-1)**int(source.get_x() < target.get_x())
            arcs.add(Line(
                source.get_edge_center(direction),
                target.get_edge_center(direction),
                path_arc=sign * path_arc,
                stroke_color=random_bright_color(hue_range=hue_range),
                stroke_width=interpolate(
                    min_stroke_width,
                    max_stroke_width,
                    strength,
                )
            ))
        if fix_in_frame:
            arcs.fix_in_frame()
        arcs.shuffle()
        lag_ratio = 0.5 / len(arcs) if lag_ratio is None else lag_ratio

        super().__init__(
            *(
                VShowPassingFlash(arc, time_width=time_width)
                for arc in arcs
            ),
            lag_ratio=lag_ratio,
            run_time=run_time,
            **kwargs,
        )


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

class MyseteryNovel(InteractiveScene):
    def construct(self):
        # Create paragraphs
        text = Path(DATA_DIR, "murder_story.txt").read_text()
        paragraphs = VGroup(
            get_paragraph(para.split(" "), line_len=40)
            for para in text.split("\n\n")
        )
        dots = Tex(R"\vdots", font_size=200)
        paragraphs.replace_submobject(4, dots)
        paragraphs.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        dots.match_x(paragraphs)
        self.add(paragraphs)

        # Mark last word
        last_word = paragraphs[-1]["Derek!\""][0]
        rect = SurroundingRectangle(last_word)
        rect.set_stroke(YELLOW, 2)
        rect.set_fill(YELLOW, 0.25)
        q_marks = Tex("???")
        q_marks.move_to(rect)
        rect.add(q_marks)
        rect.shift(0.05 * DR)

        last_word.scale(0).set_fill(BLACK)
        self.add(rect)

        # Show the first line
        frame = self.frame
        frame.set_y(15)
        paragraphs.set_fill(opacity=0.25)
        opening = paragraphs[0]["It was a dark and stormy night."][0]
        self.play(opening.animate.set_fill(opacity=1).set_anim_args(lag_ratio=0.1))
        self.wait()

        # Scroll down
        penultimate_words = paragraphs[-1]["therefore, the murderer was"][0]
        self.play(
            frame.animate.set_y(-15.4),
            paragraphs.animate.set_fill(opacity=1).set_anim_args(lag_ratio=0.01),
            run_time=5,
        )
        self.wait()
        self.add(penultimate_words.copy())
        self.play(paragraphs.animate.set_opacity(0.25))
        self.wait()

        # Show the final vector
        was = penultimate_words[-3:]
        # CHANGE: FillArrow no longer exists in manimgl; Arrow is now the filled arrow (thickness 0.07 -> 4.7, the scale is 0.015)
        arrow = Arrow(ORIGIN, DOWN, buff=0, thickness=4.7)
        arrow.next_to(was, DOWN, MED_SMALL_BUFF)
        vect = NumericEmbedding(length=12)
        vect.set_height(5)
        vect.next_to(arrow, DOWN)

        self.play(LaggedStart(
            frame.animate.set_y(-17.5).set_height(12.5),
            FadeIn(arrow, scale=3, shift=DOWN),
            FadeIn(vect, DOWN),
            run_time=2
        ))
        self.context_anim(paragraphs[-1], vect)
        self.wait()

        # Zoom out more
        vect_group = VGroup(arrow, vect)
        vect_group.target = vect_group.generate_target()
        vect_group.target.scale(2.35, about_edge=UP)
        self.play(
            paragraphs.animate.set_fill(opacity=0.8),
            frame.animate.set_height(37).set_y(-14),
            MoveToTarget(vect_group),
            run_time=2
        )
        self.context_anim(paragraphs[-4:], vect)

    def context_anim(self, source, vect):
        flat_source = VGroup(*source.family_members_with_points())
        vect_len = len(vect.get_entries())
        self.play(
            LaggedStart(
                (ContextAnimation(
                    entry, flat_source[n::vect_len],
                    path_arc=-PI / 2,
                    run_time=5,
                    lag_ratio=1e-3,
                    max_stroke_width=2
                )
                for n, entry in enumerate(vect.get_entries())),
                lag_ratio=0.1,
            ),
            RandomizeMatrixEntries(vect, run_time=5),
        )
