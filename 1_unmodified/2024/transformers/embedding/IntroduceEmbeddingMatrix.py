# ==============================================================================
# Scene:      IntroduceEmbeddingMatrix
# Source:     videos/_2024/transformers/embedding.py (lines 341-609)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl IntroduceEmbeddingMatrix.py IntroduceEmbeddingMatrix -w -m --fps 15
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


def data_flying_animation(
    point,
    vect=2 * DOWN + RIGHT,
    color=GREY_C,
    max_opacity=0.75,
    font_size=48,
    fix_in_frame=False
    ):
    word = Text("Data", color=color, font_size=font_size)
    if fix_in_frame:
        word.fix_in_frame()
    return UpdateFromAlphaFunc(
        word, lambda m, a: m.move_to(
            interpolate(point, point + vect, a)
        ).set_opacity(there_and_back(a) * max_opacity)
    )


def get_data_modifying_matrix_anims(
    matrix,
    word_shape=(5, 10),
    alpha_maxes=(0.7, 0.9),
    shift_vect=2 * DOWN + RIGHT,
    run_time=3,
    fix_in_frame=False,
    font_size=48,
):
    x_min, x_max = [matrix.get_x(LEFT), matrix.get_x(RIGHT)]
    y_min, y_max = [matrix.get_y(UP), matrix.get_y(DOWN)]
    z = matrix.get_z()
    points = np.array([
        [
            interpolate(x_min, x_max, a1),
            interpolate(y_min, y_max, a2),
            z,
        ]
        for a1 in np.linspace(0, alpha_maxes[1], word_shape[1])
        for a2 in np.linspace(0, alpha_maxes[0], word_shape[0])
    ])
    return [
        LaggedStart(
            (data_flying_animation(p, vect=shift_vect, fix_in_frame=fix_in_frame, font_size=font_size)
            for p in points),
            lag_ratio=1 / len(points),
            run_time=run_time
        ),
        RandomizeMatrixEntries(matrix, run_time=run_time),
    ]


def data_modifying_matrix(scene, matrix, *args, **kwargs):
    anims = get_data_modifying_matrix_anims(matrix, *args, **kwargs)
    scene.play(*anims)


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

def get_token_encoding():
    return tiktoken.encoding_for_model("davinci")


class IntroduceEmbeddingMatrix(InteractiveScene):
    def construct(self):
        # Load words
        words = [
            'aah',
            'aardvark',
            'aardwolf',
            'aargh',
            'ab',
            'aback',
            'abacterial',
            'abacus',
            'abalone',
            'abandon',
            'zygoid',
            'zygomatic',
            'zygomorphic',
            'zygosis',
            'zygote',
            'zygotic',
            'zyme',
            'zymogen',
            'zymosis',
            'zzz'
        ]

        # Get all words
        dots = Tex(R"\vdots")
        shown_words = VGroup(
            *map(Text, words[:10]),
            dots,
            *map(Text, words[-10:]),
        )
        shown_words.arrange(DOWN, aligned_edge=LEFT)
        dots.match_x(shown_words[:5])
        shown_words.set_height(FRAME_HEIGHT - 1)
        shown_words.move_to(LEFT)
        shown_words.set_fill(border_width=0)

        brace = Brace(shown_words, RIGHT)
        brace_text = brace.get_tex(R"\text{All words, } \sim 50\text{k}")

        self.play(
            LaggedStartMap(FadeIn, shown_words, shift=0.5 * LEFT, lag_ratio=0.1, run_time=2),
            GrowFromCenter(brace, time_span=(0.5, 2.0)),
            FadeIn(brace_text, time_span=(0.5, 1.5)),
        )
        self.wait()

        # Show embedding matrix
        dots_index = shown_words.submobjects.index(dots)
        matrix = WeightMatrix(
            shape=(10, len(shown_words)),
            ellipses_col=dots_index
        )
        matrix.set_width(13.5)
        matrix.center()
        columns = matrix.get_columns()

        matrix_name = Text("Embedding matrix", font_size=90)
        matrix_name.next_to(matrix, DOWN, buff=0.5)

        shown_words.target = shown_words.generate_target()
        shown_words.target.rotate(PI / 2)
        shown_words.target.next_to(matrix, UP)
        for word, column in zip(shown_words.target, columns):
            word.match_x(column)
            word.rotate(-45 * DEGREES, about_edge=DOWN)
        shown_words.target[dots_index].rotate(45 * DEGREES).move_to(
            shown_words.target[dots_index - 1:dots_index + 2]
        )
        new_brace = Brace(shown_words.target, UP, buff=0.0)
        column_rects = VGroup(*(
            SurroundingRectangle(column, buff=0.05)
            for column in columns
        ))
        column_rects.set_stroke(WHITE, 1)

        self.play(
            MoveToTarget(shown_words),
            brace.animate.become(new_brace),
            brace_text.animate.next_to(new_brace, UP, buff=0.1),
            LaggedStart(*(
                Write(column, lag_ratio=0.01, stroke_width=1)
                for column in columns
            ), lag_ratio=0.2, run_time=2),
            LaggedStartMap(FadeIn, matrix.get_brackets(), scale=0.5, lag_ratio=0)
        )
        self.play(Write(matrix_name, run_time=1))
        self.wait()

        # Show a few columns
        last_rect = VMobject()
        # for index in [9, -7, 7, -5, -6]:
        for index in range(len(columns)):
            for group in shown_words, columns:
                group.target = group.generate_target()
                group.target.set_opacity(0.2)
                group.target[index].set_opacity(1)
            rect = column_rects[index]
            self.play(
                *map(MoveToTarget, [shown_words, columns]),
                FadeIn(rect),
                FadeOut(last_rect),
            )
            last_rect = rect
            self.wait(0.5)
        self.play(
            FadeOut(last_rect),
            shown_words.animate.set_opacity(1),
            columns.animate.set_opacity(1),
        )

        # Label as W_E
        frame = self.frame
        lhs = Tex("W_E = ", font_size=90)
        lhs.next_to(matrix, LEFT)

        self.play(
            frame.animate.set_width(FRAME_WIDTH + 3, about_edge=RIGHT),
            Write(lhs)
        )
        self.wait()

        # Randomize entries
        rects = VGroup(*(
            SurroundingRectangle(entry).insert_n_curves(20)
            for entry in matrix.get_entries()
            if entry not in matrix.ellipses
        ))
        rects.set_stroke(WHITE, 1)
        for x in range(1):
            self.play(
                RandomizeMatrixEntries(matrix, lag_ratio=0.01),
                LaggedStartMap(VShowPassingFlash, rects, lag_ratio=0.01, time_width=1.5),
                run_time=2,
            )
        data_modifying_matrix(self, matrix)
        self.wait()

        # Highlight just one word
        matrix_group = VGroup(lhs, matrix, shown_words, matrix_name)
        index = words.index("aardvark")
        vector = VGroup(
            matrix.get_brackets()[0],
            matrix.get_columns()[index],
            matrix.get_brackets()[1],
        ).copy()
        vector.target = vector.generate_target()
        vector.target.arrange(RIGHT, buff=0.1)
        vector.target.set_height(4.5)
        vector.target.move_to(frame, DOWN).shift(0.5 * UP)
        vector.target.set_x(-3)

        word = shown_words[index].copy()
        word.target = word.generate_target()
        word.target.rotate(-45 * DEGREES)
        word.target.scale(3)
        word.target.next_to(vector.target, LEFT, buff=1.5)
        arrow = Arrow(word.target, vector.target)

        self.play(LaggedStart(
            matrix_group.animate.scale(0.5).next_to(frame.get_top(), DOWN, 0.5),
            FadeOut(brace, UP),
            FadeOut(brace_text, 0.5 * UP),
            MoveToTarget(word),
            MoveToTarget(vector),
            GrowFromPoint(arrow, word.get_center()),
        ), lag_ratio=0.15)
        self.wait()

        word_group = VGroup(word, arrow, vector)

        # Pull the matrix back up
        self.play(
            FadeOut(word_group, DOWN),
            matrix_group.animate.scale(2.0).move_to(frame)
        )

        # Have data fly across
        data_modifying_matrix(self, matrix, word_shape=(3, 10), alpha_maxes=(0.5, 0.9))
        self.wait()

        # Prep tokens
        encoding = get_token_encoding()
        n_vocab = encoding.n_vocab
        kw = dict(font_size=24)
        shown_tokens = VGroup(
            *(Text(encoding.decode([i]), **kw) for i in range(10)),
            shown_words[dots_index].copy().rotate(-45 * DEGREES),
            *(Text(encoding.decode([i]), **kw) for i in range(n_vocab - 10, n_vocab)),
        )
        for token, word in zip(shown_tokens, shown_words):
            token.rotate(45 * DEGREES)
            token.move_to(word, DL)
        shown_tokens[dots_index].move_to(
            shown_tokens[dots_index-1:dots_index + 2:2]
        )

        # Show dimensions
        top_brace = Brace(shown_words, UP)
        left_brace = Brace(matrix, LEFT, buff=SMALL_BUFF)
        vocab_count = Integer(50257)
        vocab_label = VGroup(vocab_count, Text("words"))
        vocab_label.arrange(RIGHT, aligned_edge=UP)
        vocab_label.next_to(top_brace, UP, SMALL_BUFF)
        token_label = Text("tokens", fill_color=YELLOW)
        token_label.move_to(vocab_label[1], LEFT)

        dim_count = Integer(12288)
        dim_count.next_to(left_brace, LEFT, SMALL_BUFF)

        self.play(
            GrowFromCenter(top_brace),
            CountInFrom(vocab_count, 0),
            FadeIn(vocab_label[1]),
        )
        self.wait()
        self.play(
            FadeOut(vocab_label[1], 0.5 * UP),
            FadeIn(token_label, 0.5 * UP),
            LaggedStartMap(FadeOut, shown_words, shift=0.25 * UP, lag_ratio=0.1),
            LaggedStartMap(FadeIn, shown_tokens, shift=0.25 * UP, lag_ratio=0.1),
        )
        self.wait()

        matrix_name.target = matrix_name.generate_target()
        matrix_name.target.shift(RIGHT)
        self.play(
            MoveToTarget(matrix_name),
            lhs.animate.next_to(matrix_name.target, LEFT),
            GrowFromCenter(left_brace),
            CountInFrom(dim_count, 0),
        )
        self.play(FlashAround(dim_count))
        self.wait()

        # Count total parameters
        matrix_group = VGroup(
            top_brace, vocab_count,
            left_brace, dim_count,
            matrix, shown_words, matrix_name, lhs
        )

        top_equation = VGroup(
            Text("Total parameters = "),
            dim_count.copy(),
            Tex(R"\times"),
            vocab_count.copy(),
            Tex("="),
            Integer(vocab_count.get_value() * dim_count.get_value()).set_color(YELLOW),
        )
        top_equation.arrange(RIGHT)
        top_equation.set_height(0.5)
        top_equation.next_to(matrix_group, UP, buff=1.0)
        result_rect = SurroundingRectangle(top_equation[-1])
        result_rect.set_stroke(YELLOW, 2)

        self.play(
            LaggedStartMap(FadeIn, top_equation[::2], shift=0.25 * UP, lag_ratio=0.5),
            TransformFromCopy(dim_count, top_equation[1]),
            TransformFromCopy(vocab_count, top_equation[3]),
            frame.animate.set_height(11).move_to(matrix_group, DOWN).shift(DOWN),
        )
        self.play(FadeTransform(
            top_equation[1:5:2].copy(), top_equation[-1]
        ))
        self.play(ShowCreation(result_rect))
        self.wait()
