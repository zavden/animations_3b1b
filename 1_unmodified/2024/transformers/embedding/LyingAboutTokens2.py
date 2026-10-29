# ==============================================================================
# Scene:      LyingAboutTokens2
# Source:     videos/_2024/transformers/embedding.py (lines 119-257)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl LyingAboutTokens2.py LyingAboutTokens2 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import tiktoken
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



# ----- From _2024/transformers/embedding.py -----

def get_token_encoding():
    return tiktoken.encoding_for_model("davinci")


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


def break_into_tokens(phrase_mob):
    tokenizer = get_token_encoding()
    tokens = tokenizer.encode(phrase_mob.get_string())
    _, offsets = tokenizer.decode_with_offsets(tokens)
    return break_into_pieces(phrase_mob, offsets)


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


class LyingAboutTokens2(InteractiveScene):
    def construct(self):
        # Mention next word prediction task
        phrase = Text("The goal of our model is to predict the next word")

        words = break_into_tokens(phrase)
        rects = get_piece_rectangles(words, leading_spaces=True, h_buff=0)

        words.remove(words[-1])
        q_marks = Text("???")
        rects[-1].set_color(YELLOW)
        q_marks.next_to(rects[-1], DOWN)

        big_rect = Rectangle()
        big_rect.replace(rects[:-1], stretch=True)
        big_rect.set_stroke(GREY_B, 2)
        arrow = Arrow(big_rect.get_top(), rects[-1].get_top(), path_arc=-120 * DEGREES)
        arrow.scale(0.5, about_edge=DR)

        self.play(ShowIncreasingSubsets(words, run_time=1))
        self.add(rects[-1])
        self.play(LaggedStart(
            FadeIn(big_rect),
            ShowCreation(arrow),
            Write(q_marks),
            lag_ratio=0.3,
        ))
        self.wait()
        self.play(
            FadeOut(big_rect),
            LaggedStart(*(
                DrawBorderThenFill(rect)
                for rect in rects[:-1]
            ), lag_ratio=0.02),
            LaggedStart(*(
                word.animate.match_color(rect)
                for word, rect in zip(words, rects)
            )),
            FadeOut(arrow)
        )
        self.wait()

        # Show words into vectors
        vectors = VGroup(*(
            NumericEmbedding(length=8)
            for word in words
        ))
        vectors.arrange(RIGHT, buff=1.0 * vectors[0].get_width())
        vectors.set_width(12)
        vectors.to_edge(DOWN, buff=1.0)
        vectors.to_edge(LEFT, buff=0.5)
        for vector, word in zip(vectors, words):
            vector.get_brackets().match_color(word[0])

        blocks = VGroup(*(VGroup(rect, word) for rect, word in zip(rects, words)))
        q_group = VGroup(rects[-1], q_marks)
        blocks.target = blocks.generate_target()
        for block, vector in zip(blocks.target, vectors):
            block.next_to(vector, UP, buff=1.5)

        arrows = VGroup(*(
            Arrow(block, vect, stroke_width=3)
            for block, vect in zip(blocks.target, vectors)
        ))

        self.play(
            MoveToTarget(blocks),
            q_group.animate.next_to(blocks.target, RIGHT, aligned_edge=UP),
            LaggedStartMap(FadeIn, vectors, shift=0.5 * DOWN),
            LaggedStartMap(GrowFromCenter, arrows),
        )
        self.wait()

        # Setup titles
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        title1, title2 = titles = VGroup(
            Text("The Truth", font_size=72).to_edge(UP),
            Text("A Convenient Lie", font_size=72).next_to(h_line, DOWN),
        )
        h_line.set_stroke(WHITE, 2)
        h_line.next_to(titles[1], UP)
        for title in titles:
            title.add(Underline(title))

        # Show the lie
        phrase1, phrase2 = phrases = VGroup(
            Text("This process (known fancifully as tokenization) frequently subdivides words"),
            # Text("It's nice to sometimes pretend tokens are words"),
            Text("Let's pretend that tokens are always simply words"),
        )
        for phrase, title in zip(phrases, titles):
            phrase.set_width(FRAME_WIDTH - 1)
            phrase.next_to(title, DOWN, buff=1.0)

        tokens = break_into_tokens(phrase1)
        words = break_into_words(phrase2)
        token_rects = get_piece_rectangles(tokens, hue_range=(0.1, 0.2), leading_spaces=True, h_buff=0.0)
        word_rects = get_piece_rectangles(words, hue_range=(0.5, 0.6))

        self.play(
            FadeOut(blocks),
            FadeOut(q_group),
            FadeOut(arrows),
            FadeOut(vectors),
            ShowCreation(h_line),
            FadeIn(title1, lag_ratio=0.1),
            FadeIn(tokens),
        )
        self.add(token_rects, tokens)
        self.play(
            LaggedStartMap(FadeIn, token_rects),
            LaggedStart(*(
                token.animate.set_color(rect.get_color())
                for token, rect in zip(tokens, token_rects)
            ))
        )
        self.wait()
        self.play(
            FadeIn(title2, lag_ratio=0.1),
            FadeIn(words),
        )
        self.add(word_rects, words)
        self.play(
            LaggedStartMap(FadeIn, word_rects),
            LaggedStart(*(
                token.animate.set_color(rect.get_color())
                for token, rect in zip(words, word_rects)
            ))
        )
        self.wait()

        # Analyze tokenization
        brace = Brace(token_rects[8], buff=0.05)

        self.play(GrowFromCenter(brace))
        self.wait()
        for index in [2, 4, 5, 7, 8, 9, 11, 12]:
            self.play(brace.animate.become(Brace(token_rects[index], buff=0.05)))
            self.wait()
