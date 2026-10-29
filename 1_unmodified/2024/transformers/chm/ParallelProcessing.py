# ==============================================================================
# Scene:      ParallelProcessing
# Source:     videos/_2024/transformers/chm.py (lines 1536-1574)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ParallelProcessing.py ParallelProcessing -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

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



# ----- From _2024/transformers/chm.py -----

class SerialProcessing(InteractiveScene):
    phrase = "It was the best of times it was the worst of times"
    phrase_center = 2 * UP

    def construct(self):
        # Set up words
        words = self.get_words()
        rects = get_piece_rectangles(words)

        self.add(rects)
        self.add(words)

        # Animate in the vectors
        vectors = VGroup(
            self.get_abstract_vector().next_to(word, DOWN, LARGE_BUFF)
            for word in words
        )
        last_vect = VGroup(VectorizedPoint(rects[0].get_bottom()))

        for word, vect in zip(words, vectors):
            self.play(
                FadeIn(vect, run_time=2),
                LaggedStart(
                    (ContextAnimation(
                        square, VGroup(*word, *last_vect),
                        direction=DOWN,
                        lag_ratio=0.01,
                        path_arc=30 * DEGREES
                    )
                    for square in vect),
                    lag_ratio=0.05,
                    run_time=2
                ),
                last_vect.animate.set_opacity(0.2)
            )
            last_vect = vect

    def get_words(self):
        result = break_into_words(Text(self.phrase))
        result.move_to(self.phrase_center)
        return result

    def get_abstract_vector(self, values=None, default_length=10, elem_size=0.2):
        if values is None:
            values = np.random.uniform(-1, 1, default_length)
        result = Square().get_grid(len(values), 1, buff=0)
        result.set_width(elem_size)
        result.set_stroke(WHITE, 1)
        for square, value in zip(result, values):
            color = value_to_color(value, min_value=0, max_value=1)
            square.set_fill(color, opacity=1)
        return result


class ParallelProcessing(SerialProcessing):
    def construct(self):
        # Set up words
        words = self.get_words()
        rects = get_piece_rectangles(words)

        self.add(rects)
        self.add(words)

        # Animate in the vectors
        vectors = VGroup(
            self.get_abstract_vector().next_to(word, DOWN, buff=1.5)
            for word in words
        )

        lines = VGroup(
            Line(
                rect.get_bottom(), vect.get_top(),
                buff=0.05,
                stroke_color=WHITE,
                stroke_width=2 * random.random()**3
            )
            for rect in rects
            for vect in vectors
        )
        lines.shuffle()

        for vect, word in zip(vectors, words):
            vect.save_state()
            for square in vect:
                square.move_to(word)
                square.set_opacity(0)

        self.play(
            LaggedStartMap(ShowCreation, lines, lag_ratio=0.01),
            LaggedStartMap(Restore, vectors, lag_ratio=0)
        )
        self.play(lines.animate.set_stroke(opacity=0.25))
        self.wait()
