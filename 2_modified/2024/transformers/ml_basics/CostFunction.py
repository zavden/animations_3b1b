# ==============================================================================
# Scene:      CostFunction
# Source:     videos/_2024/transformers/ml_basics.py (lines 2368-2430)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/generation.py
#
# Run from this folder:
#     manimgl CostFunction.py CostFunction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - gpt3_predict_next_token (openai.Completion, no key or network) returns a fixed table of plausible predictions; " smarter" comes first (they are not GPT-3's)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import tiktoken
import openai


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



# ----- From _2024/transformers/generation.py -----

# CHANGE: openai.Completion (old OpenAI API, needs a key and network) is replaced by a fixed table of
# plausible predictions (they are not GPT-3's); the expected word, " smarter", comes first
_SYNTHETIC_NEXT_TOKEN_TABLE = {
    "Watching 3Blue1Brown makes you": [
        (" smarter", 0.231), (" think", 0.118), (" feel", 0.093), (" want", 0.062), (" laugh", 0.047),
        (" happy", 0.041), (" realize", 0.035), (" learn", 0.031), (" more", 0.026), (" curious", 0.021),
    ],
}
_SYNTHETIC_GENERIC_NEXT_TOKENS = [
    (" the", 0.119), (" a", 0.071), (" to", 0.058), (" and", 0.049), (" of", 0.044),
    (" in", 0.037), (" is", 0.033), (" that", 0.029), (" it", 0.026), (" for", 0.022),
]


def gpt3_predict_next_token(text, n_shown=10, random_seed=0):
    table = _SYNTHETIC_NEXT_TOKEN_TABLE.get(text.strip(), _SYNTHETIC_GENERIC_NEXT_TOKENS)
    tokens, probs = zip(*table[:n_shown])
    return list(tokens), np.array(probs)


def next_token_bar_chart(
    words, probs,
    reference_point=ORIGIN,
    font_size=24,
    width_100p=1.0,
    prob_exp=0.75,
    bar_height=0.25,
    bar_space_factor=0.5,
    buff=1.2,
    show_ellipses=True,
    use_percent=True,
):
    labels = VGroup(Text(word, font_size=font_size) for word in words)
    bars = VGroup(
        Rectangle(prob**(prob_exp) * width_100p, bar_height)
        for prob, label in zip(probs, labels)
    )
    bars.arrange(DOWN, aligned_edge=LEFT, buff=bar_space_factor * bar_height)
    bars.set_fill(opacity=1)
    bars.set_submobject_colors_by_gradient(TEAL, YELLOW)
    bars.set_stroke(WHITE, 1)

    bar_groups = VGroup()
    for label, bar, prob in zip(labels, bars, probs):
        if use_percent:
            prob_label = Integer(int(100 * prob), unit="%", font_size=0.75 * font_size)
        else:
            prob_label = DecimalNumber(prob, font_size=0.75 * font_size)
        prob_label.next_to(bar, RIGHT, buff=SMALL_BUFF)
        label.next_to(bar, LEFT)
        bar_groups.add(VGroup(label, bar, prob_label))

    if show_ellipses:
        ellipses = Tex(R"\vdots", font_size=font_size)
        ellipses.next_to(bar_groups[-1][0], DOWN)
        bar_groups.add(ellipses)

    bar_groups.shift(reference_point - bars.get_left() + buff * RIGHT)

    return bar_groups



# ----- From _2024/transformers/ml_basics.py -----

class CostFunction(InteractiveScene):
    def construct(self):
        # Add graph
        axes = Axes((0, 1, 0.1), (0, 5, 1), width=10, height=6)
        axes.center().to_edge(LEFT)
        axes.x_axis.add_numbers(num_decimal_places=1)
        axes.y_axis.add_numbers(num_decimal_places=0, direction=LEFT)
        x_label = Tex("p")
        x_label.next_to(axes.x_axis.get_right(), UR)
        axes.add(x_label)

        graph = axes.get_graph(lambda x: -np.log(x), x_range=(0.001, 10, 0.01))
        graph.set_color(RED)

        expr = Tex(R"\text{Cost} = -\log(p)", font_size=60)
        expr.next_to(axes.i2gp(0.1, graph), UR, buff=0.1)

        self.add(axes, graph, expr)

        # Add sample phrase
        phrase = Text("Watching 3Blue1Brown makes you smarter")
        phrase.scale(0.75)
        phrase.to_edge(UP)
        phrase.align_to(axes.c2p(0.1, 0), LEFT)
        pieces = break_into_tokens(phrase)
        pieces[-1].set_opacity(0.0)
        rects = get_piece_rectangles(pieces, leading_spaces=True, h_buff=0)

        self.add(rects, pieces)

        # Add predictions
        arrow = Vector(0.5 * DOWN)
        arrow.next_to(rects[-1], DOWN, SMALL_BUFF)
        index = 0

        tokens, probs = gpt3_predict_next_token(phrase.get_text()[:-len(" smarter")])
        bar_chart = next_token_bar_chart(
            tokens[:8], probs[:8],
            width_100p=7.0,
            bar_space_factor=1.0,
            use_percent=False,
        )
        bar_chart.next_to(arrow, DOWN)
        bar_chart.shift(1.25 * RIGHT)
        bar_chart.set_opacity(0.5)
        bar_chart[index].set_opacity(1.0)
        rect = SurroundingRectangle(bar_chart[index])

        self.add(arrow, bar_chart, rect)

        # Animate in graph
        self.play(
            ShowCreation(graph, run_time=3),
            Write(expr, run_time=2),
        )
        self.wait()

        # Show point on the graph
        line = axes.get_line_from_axis_to_point(0, axes.i2gp(probs[index], graph), line_func=Line)
        line.set_stroke(YELLOW)

        self.play(FadeTransform(rect.copy(), line))
        self.wait()
