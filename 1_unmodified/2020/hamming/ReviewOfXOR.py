# ==============================================================================
# Scene:      ReviewOfXOR
# Source:     videos/_2020/hamming.py (lines 5210-5426)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReviewOfXOR.py ReviewOfXOR -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_string(number, n_bits=None):
    result = "{:b}".format(number)
    if n_bits is not None:
        result = (n_bits - len(result)) * "0" + result
    return result


def get_xor(height=0.35, color=BLUE_B, stroke_width=4):
    xor = VGroup(
        Line(UP, DOWN),
        Line(LEFT, RIGHT),
        Circle(),
    )
    xor.set_stroke(color, stroke_width)
    xor.set_height(height)
    return xor


class ReviewOfXOR(Scene):
    CONFIG = {
        "random_seed": 2,
    }

    def construct(self):
        # Setup equations
        xor = get_xor()

        equations = VGroup()
        for n in range(4):
            bits = list(map(int, int_to_bit_string(n, n_bits=2)))
            equation = VGroup(
                Integer(bits[0]),
                xor.copy(),
                Integer(bits[1]),
                OldTex("="),
                Integer(op.xor(*bits)),
            )
            equation.set_height(0.6)
            equation.arrange(RIGHT)
            equations.add(equation)

        equations.arrange(DOWN, buff=LARGE_BUFF)

        # Intro xor
        equation = equations[1]
        equation.save_state()
        equation.center()
        equation[3:].set_opacity(0)

        arrow = Vector(0.7 * DOWN)
        arrow.next_to(equation[1], UP, SMALL_BUFF)
        xor_word = OldTexText("xor")
        xor_word_long = OldTexText("``exclusive or''")
        xor_words = VGroup(xor_word, xor_word_long)
        xor_words.scale(1.5)
        xor_words.match_color(xor)
        xor_words.next_to(arrow, UP)

        self.add(equation)
        self.play(
            FadeIn(equation[1], 0.5 * UP),
            GrowArrow(arrow),
            Write(xor_word),
        )
        self.wait()
        self.play(
            xor_word.next_to, xor_word_long, UP, MED_SMALL_BUFF,
            FadeIn(xor_word_long, DOWN),
        )
        self.wait()
        self.play(
            FadeOut(arrow),
            xor_words.to_corner, UL,
            Restore(equation),
            FadeIn(equations[2], UP),
        )
        self.wait()
        self.play(
            FadeIn(equations[0], DOWN),
            FadeIn(equations[3], UP),
        )
        self.wait()

        # Parity of two bits
        parity_words = OldTexText("Parity of\\\\two bits")
        parity_words.set_color(YELLOW)
        parity_words.scale(1.5)
        parity_words.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        arrows = VGroup()
        for equation in equations:
            globals()['equation'] = equation
            new_arrows = VGroup(*[
                Arrow(equation[i].get_top(), equation[4].get_top(), path_arc=-60 * DEGREES)
                for i in [0, 2]
            ])
            new_arrows.set_color(YELLOW)
            arrows.add(new_arrows)

        self.play(
            LaggedStartMap(DrawBorderThenFill, arrows),
            FadeIn(parity_words)
        )
        self.wait()

        # Addition mod 2
        mod2_words = OldTexText("Addition\\\\mod 2")
        mod2_words.scale(1.5)
        mod2_words.move_to(parity_words, RIGHT)
        mod2_words.set_color(BLUE)

        self.play(
            FadeIn(mod2_words, DOWN),
            FadeOut(parity_words, UP),
            FadeOut(arrows)
        )
        self.wait()

        # xor of two bit strings
        row_len = 8
        bit_strings = VGroup(*[
            Integer(random.choice([0, 1]), edge_to_fix=ORIGIN)
            for x in range(row_len * 3)
        ])
        bit_strings.arrange_in_grid(
            3, row_len,
            h_buff=SMALL_BUFF,
            v_buff=MED_LARGE_BUFF,
            fill_rows_first=False
        )
        bit_strings.scale(equation[0][0].get_height() / bit_strings[0].get_height())
        rows = VGroup(*[bit_strings[i::3] for i in range(3)])
        rows[0].next_to(rows[1], UP, buff=0.25)

        line = Line(LEFT, RIGHT)
        line.set_width(bit_strings.get_width() + 1)
        line.move_to(bit_strings[-2:], RIGHT)
        line.set_stroke(GREY_B, 3)
        line_xor = xor.copy()
        line_xor.set_height(0.5)
        line_xor.next_to(line, UP, aligned_edge=LEFT)

        for b1, b2, b3 in zip(*[row for row in rows]):
            b3.set_value(b1.get_value() ^ b2.get_value())
            b2.match_x(b1)
            b3.match_x(b1)

        equations.generate_target()
        for n, eq in enumerate(equations.target):
            for k, b1 in enumerate(eq[0::2]):
                target_bit = bit_strings[3 * n + k]
                target_bit.set_value(b1.get_value())
                b1.become(target_bit)
            eq[1].become(line_xor)
            eq[3].fade(1)

        self.play(
            MoveToTarget(equations, run_time=2),
            FadeOut(mod2_words),
            FadeIn(bit_strings[12:], run_time=2, rate_func=squish_rate_func(smooth, 0.5, 1), lag_ratio=0.1),
            ShowCreation(line, run_time=2, rate_func=squish_rate_func(smooth, 0.5, 1))
        )
        self.remove(equations)
        self.add(bit_strings, line_xor)
        self.wait()

        # Highlight columns
        last_rect = VMobject()
        for b1, b2, b3 in zip(*[row for row in rows]):
            rect = SurroundingRectangle(VGroup(b1, b2, b3), buff=SMALL_BUFF)
            rect.set_stroke(BLUE, 2)
            self.play(FadeIn(rect), FadeOut(last_rect))
            last_rect = rect
        self.play(FadeOut(last_rect))

        # Add more rows
        new_rows = VGroup(*[rows[0].copy() for x in range(3)])
        new_rows.arrange(DOWN, buff=0.2)
        new_rows.next_to(rows, UP, buff=0.2)
        for row in new_rows:
            for bit in row:
                bit.set_value(random.choice([0, 1]))

        self.play(
            LaggedStartMap(FadeIn, new_rows, lambda m: (m, DOWN)),
            FadeOut(xor_words),
            FadeOut(rows[2])
        )

        # Compute parities
        parity_words = OldTexText("Computes\\\\parity\\\\of each\\\\column", alignment="")
        parity_words.set_color(YELLOW)
        parity_words.to_corner(UL)
        self.add(parity_words)

        for tup in zip(*[*new_rows, *rows]):
            rects = VGroup()
            for bit in tup[:-1]:
                if bit.get_value() == 1:
                    rect = SurroundingRectangle(bit)
                    rect.set_stroke(YELLOW, 2)
                    rect.set_fill(YELLOW, 0.5)
                    rects.add(rect)
            tup[-1].set_value(len(rects) % 2)
            tup[-1].set_color(YELLOW)
            self.add(rects, *tup)
            self.wait()
            self.remove(rects)
        self.wait()

        # Simpler sum
        self.play(FadeOut(
            VGroup(new_rows, rows[0][4:], rows[1][4:], rows[2][4:]),
            lag_ratio=0.1,
        ))
        for b1, b2, b3 in zip(*[row[:4] for row in rows]):
            b3.set_value(b1.get_value() ^ b2.get_value())
            self.wait(0.25)

        arrows = VGroup()
        integers = VGroup()
        for row, n in zip(rows, [3, 5, 6]):
            arrow = Vector(0.75 * RIGHT)
            arrow.next_to(row[:4], RIGHT, buff=0.2)
            integer = Integer(n)
            integer.match_height(row[0])
            integer.match_color(row[0])
            integer.next_to(arrow, RIGHT, buff=0.2)
            self.play(
                GrowArrow(arrow),
                FadeIn(integer, LEFT)
            )

            arrows.add(arrow)
            integers.add(integer)
