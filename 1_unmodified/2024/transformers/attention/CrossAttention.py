# ==============================================================================
# Scene:      CrossAttention
# Source:     videos/_2024/transformers/attention.py (lines 3120-3301)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/embedding.py, _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl CrossAttention.py CrossAttention -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import warnings


# ----- From _2024/transformers/helpers.py -----

def softmax(logits, temperature=1.0):
    logits = np.array(logits)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')  # Ignore all warnings within this block
        logits = logits - np.max(logits)  # For numerical stability
        exps = np.exp(np.divide(logits, temperature, where=temperature != 0))
    
    if np.isinf(exps).any() or np.isnan(exps).any() or temperature == 0:
        result = np.zeros_like(logits)
        result[np.argmax(logits)] = 1
        return result
    return exps / np.sum(exps)



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

class CrossAttention(InteractiveScene):
    def construct(self):
        # Show both
        en_tokens = self.get_words("I do not want to pet it")
        fr_tokens = self.get_words("Je ne veux pas le caresser", hue_range=(0.2, 0.3))
        phrases = VGroup(en_tokens, fr_tokens)
        phrases.arrange(DOWN, buff=2.0)
        self.play(LaggedStartMap(FadeIn, en_tokens, scale=2, lag_ratio=0.25))
        self.wait()
        self.play(LaggedStartMap(FadeIn, fr_tokens, scale=2, lag_ratio=0.25))
        self.wait()

        # Create attention pattern
        unnormalized_pattern = [
            [3, 0, 0, 0, 0, 0],
            [0, 1, 1.3, 1, 0, 0],
            [0, 3, 0, 3, 0, 0],
            [0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 3, 0],
        ]
        attention_pattern = np.array([
            softmax(col) for col in unnormalized_pattern
        ]).T

        # Show connections
        lines = VGroup()
        for n, row in enumerate(attention_pattern.T):
            for k, value in enumerate(row):
                line = Line(en_tokens[n].get_bottom(), fr_tokens[k].get_top(), buff=0)
                line.set_stroke(
                    color=[
                        en_tokens[n][0].get_color(),
                        fr_tokens[k][0].get_color(),
                    ],
                    width=3,
                    opacity=value,
                )
                lines.add(line)

        self.play(ShowCreation(lines, lag_ratio=0.01, run_time=2))
        self.wait(2)
        self.play(FadeOut(lines))

        # Create grid
        grid = Square().get_grid(len(fr_tokens), len(en_tokens), buff=0)
        grid.stretch(1.2, 0)
        grid.set_stroke(GREY_B, 1)
        grid.set_height(5.0)
        grid.to_edge(DOWN, buff=SMALL_BUFF)
        grid.set_x(1)

        # Create qk symbols
        q_sym_generator = self.get_symbol_generator(R"\vec{\textbf{Q}}_0", color=YELLOW)
        k_sym_generator = self.get_symbol_generator(R"\vec{\textbf{K}}_0", color=TEAL)
        e_sym_generator = self.get_symbol_generator(R"\vec{\textbf{E}}_0", color=GREY_B)
        f_sym_generator = self.get_symbol_generator(R"\vec{\textbf{F}}_0", color=BLUE)

        q_syms = VGroup(q_sym_generator(n + 1) for n in range(len(en_tokens)))
        k_syms = VGroup(k_sym_generator(n + 1) for n in range(len(fr_tokens)))
        e_syms = VGroup(e_sym_generator(n + 1) for n in range(len(en_tokens)))
        f_syms = VGroup(f_sym_generator(n + 1) for n in range(len(fr_tokens)))
        VGroup(q_syms, k_syms, e_syms, f_syms).scale(0.65)

        for q_sym, e_sym, square in zip(q_syms, e_syms, grid):
            q_sym.next_to(square, UP, SMALL_BUFF)
            e_sym.next_to(q_sym, UP, buff=0.65)

        for k_sym, f_sym, square in zip(k_syms, f_syms, grid[::len(en_tokens)]):
            k_sym.next_to(square, LEFT, SMALL_BUFF)
            f_sym.next_to(k_sym, LEFT, buff=0.75)

        q_arrows = VGroup(Arrow(*pair, buff=0.1) for pair in zip(e_syms, q_syms))
        k_arrows = VGroup(Arrow(*pair, buff=0.1) for pair in zip(f_syms, k_syms))
        e_arrows = VGroup(Vector(0.4 * DOWN).next_to(e_sym, UP, SMALL_BUFF) for e_sym in e_syms)
        f_arrows = VGroup(Vector(0.5 * RIGHT).next_to(f_sym, LEFT, SMALL_BUFF) for f_sym in f_syms)
        arrows = VGroup(q_arrows, k_arrows, e_arrows, f_arrows)
        arrows.set_color(GREY_B)

        wq_syms = VGroup(
            Tex("W_Q", font_size=20, fill_color=YELLOW).next_to(arrow, RIGHT, buff=0.1)
            for arrow in q_arrows
        )
        wk_syms = VGroup(
            Tex("W_K", font_size=20, fill_color=TEAL).next_to(arrow, UP, buff=0.1)
            for arrow in k_arrows
        )

        # Move tokens into place
        en_tokens.target = en_tokens.generate_target()
        fr_tokens.target = fr_tokens.generate_target()
        for token, arrow in zip(en_tokens.target, e_arrows):
            token.next_to(arrow, UP, SMALL_BUFF)
        for token, arrow in zip(fr_tokens.target, f_arrows):
            token.next_to(arrow, LEFT, SMALL_BUFF)
        self.play(
            MoveToTarget(en_tokens),
            MoveToTarget(fr_tokens),
        )
        self.play(
            LaggedStartMap(GrowArrow, e_arrows),
            LaggedStartMap(GrowArrow, f_arrows),
            LaggedStartMap(FadeIn, e_syms, shift=0.25 * DOWN),
            LaggedStartMap(FadeIn, f_syms, shift=0.25 * RIGHT),
            lag_ratio=0.25,
            run_time=1.5,
        )
        self.play(
            LaggedStartMap(GrowArrow, q_arrows),
            LaggedStartMap(GrowArrow, k_arrows),
            LaggedStartMap(FadeIn, wq_syms, shift=0.25 * DOWN),
            LaggedStartMap(FadeIn, wk_syms, shift=0.25 * RIGHT),
            LaggedStartMap(FadeIn, q_syms, shift=0.5 * DOWN),
            LaggedStartMap(FadeIn, k_syms, shift=0.5 * RIGHT),
            lag_ratio=0.25,
            run_time=1.5,
        )
        self.play(FadeIn(grid, lag_ratio=1e-2), run_time=2)
        self.wait()

        # Show dot products
        dot_prods = VGroup()
        for q_sym in q_syms:
            for k_sym in k_syms:
                dot = Tex(".")
                dot.match_x(q_sym)
                dot.match_y(k_sym)
                dot_prod = VGroup(q_sym.copy(), dot, k_sym.copy())
                dot_prod.target = dot_prod.generate_target()
                dot_prod.target.arrange(RIGHT, buff=SMALL_BUFF)
                dot_prod.target.scale(0.7)
                dot_prod.target.move_to(dot)
                dot.set_opacity(0)
                dot_prods.add(dot_prod)

        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.01),
            run_time=3
        )
        self.wait()

        # Show dots
        dots = VGroup()
        for square, value in zip(grid, attention_pattern.flatten()):
            dot = Dot(radius=value * 0.4)
            dot.set_fill(GREY_B, 1)
            dot.move_to(square)
            dots.add(dot)


        self.play(
            LaggedStartMap(GrowFromCenter, dots, lag_ratio=1e-2),
            dot_prods.animate.set_fill(opacity=0.2).set_anim_args(lag_ratio=1e-3),
            run_time=4
        )
        self.wait()




        pass

    def get_words(self, text, hue_range=(0.5, 0.6)):
        sent = Text(text)
        tokens = break_into_words(sent)
        rects = get_piece_rectangles(
            tokens, hue_range=hue_range,
            # h_buff=0, leading_spaces=True
        )
        return VGroup(VGroup(*pair) for pair in zip(rects, tokens))

    def get_symbol_generator(self, raw_tex, subsrc="0", color=WHITE):
        template = Tex(raw_tex)
        template.set_color(color)
        subscr = template.make_number_changeable(subsrc)

        def get_sym(number):
            subscr.set_value(number)
            return template.copy()

        return get_sym
