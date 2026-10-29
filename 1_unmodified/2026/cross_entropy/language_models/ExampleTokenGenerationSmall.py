# ==============================================================================
# Scene:      ExampleTokenGenerationSmall
# Source:     videos/_2026/cross_entropy/language_models.py (lines 1820-1821)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py
#
# Run from this folder:
#     manimgl ExampleTokenGenerationSmall.py ExampleTokenGenerationSmall -w -m --fps 15
#
# Extra packages installed in the venv: tiktoken
#
# Notes:
#   tiktoken downloads the GPT-2 BPE vocabulary (not model weights) the first time and caches it; internet is needed that one time.
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import tiktoken


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



# ----- From _2026/cross_entropy/language_models.py -----

def get_token_groups(text):
    text_mob = Text(text)
    tokens = break_into_tokens(text_mob)
    rects = get_piece_rectangles(tokens, h_buff=0, leading_spaces=True)
    return VGroup(VGroup(*pair) for pair in zip(rects, tokens))


class ExampleTokenGenerationBig(InteractiveScene):
    time_per_token = 1.25

    def construct(self):
        # Test
        tokens = get_token_groups("int fibonacci(int n){if(n<=1){return n;}return fibonacci(n-1)+fibonacci(n-2);}")
        tokens.scale(0.7)
        tokens.save_state()
        for n in range(len(tokens)):
            tokens.restore()
            tokens[:n].next_to(ORIGIN, LEFT)
            self.add(tokens[:n])
            self.wait(self.time_per_token)
            self.remove(tokens)


class ExampleTokenGenerationSmall(ExampleTokenGenerationBig):
    time_per_token = 11 / 30
