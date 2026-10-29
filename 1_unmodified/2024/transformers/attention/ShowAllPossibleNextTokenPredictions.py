# ==============================================================================
# Scene:      ShowAllPossibleNextTokenPredictions
# Source:     videos/_2024/transformers/attention.py (lines 2083-2166)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py
#
# Run from this folder:
#     manimgl ShowAllPossibleNextTokenPredictions.py ShowAllPossibleNextTokenPredictions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


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

class ShowAllPossibleNextTokenPredictions(InteractiveScene):
    def construct(self):
        # Add phrase
        phrase = Text("the fluffy blue creature roamed the verdant forest despite")
        plain_words = break_into_words(phrase)
        rects = get_piece_rectangles(plain_words)
        words = VGroup(VGroup(*pair) for pair in zip(rects, plain_words))
        words = words[:-1]
        words.to_edge(LEFT, buff=MED_LARGE_BUFF)

        next_token_box = rects[-1].copy()
        next_token_box.set_color(YELLOW)
        next_token_box.set_stroke(YELLOW, 3)
        next_token_box.next_to(words, RIGHT, buff=LARGE_BUFF)
        q_marks = Tex("???")
        q_marks.move_to(next_token_box)
        next_token_box.add(q_marks)

        arrow = Arrow(words, next_token_box, buff=SMALL_BUFF)

        self.add(words)
        self.play(
            GrowArrow(arrow),
            FadeIn(next_token_box, RIGHT)
        )
        self.wait()

        # Set up subphrases
        scale_factor = 0.75
        v_buff = 0.4
        subphrases = VGroup(
            words[:n].copy().scale(scale_factor)
            for n in range(1, len(words) + 1)
        )
        subphrases.arrange(DOWN, buff=v_buff, aligned_edge=LEFT)
        subphrases.to_corner(UL)

        rhs = VGroup(arrow, next_token_box)
        alt_rhss = VGroup(
            rhs.copy().scale(scale_factor).next_to(subphrase, RIGHT, SMALL_BUFF)
            for subphrase in subphrases
        )

        self.play(
            Transform(words, subphrases[-1]),
            Transform(rhs, alt_rhss[-1]),
        )
        for n in range(len(subphrases) - 1, 0, -1):
            sp1 = subphrases[n]
            sp2 = subphrases[n - 1]
            rhs1 = alt_rhss[n]
            rhs2 = alt_rhss[n - 1]
            self.play(
                TransformFromCopy(sp1[:len(sp2)], sp2),
                TransformFromCopy(rhs1, rhs2),
                rate_func=linear,
                run_time=0.5
            )
        self.wait()

        # Highlight two examples
        for phrase, alt_rhs in zip(subphrases, alt_rhss):
            arrow = alt_rhs[0]
            alt_rhs.remove(arrow)
            phrase.add(arrow)
            phrase.save_state()
        index = 3
        self.play(LaggedStart(
            FadeOut(alt_rhss),
            FadeOut(rhs),
            words.animate.fade(0.75),
            subphrases[:index].animate.fade(0.75),
            subphrases[index + 1:].animate.fade(0.75),
            subphrases[index].animate.align_to(3 * RIGHT, RIGHT),
        ))
        self.wait()
        self.play(
            subphrases[index].animate.align_to(subphrases, LEFT).fade(0.75),
            subphrases[5].animate.restore().align_to(3 * RIGHT, RIGHT),
        )
        self.wait()

    def get_next_word_distribution():
        pass
