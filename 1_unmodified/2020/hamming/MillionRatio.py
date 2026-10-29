# ==============================================================================
# Scene:      MillionRatio
# Source:     videos/_2020/hamming.py (lines 4990-5048)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MillionRatio.py MillionRatio -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_string(number, n_bits=None):
    result = "{:b}".format(number)
    if n_bits is not None:
        result = (n_bits - len(result)) * "0" + result
    return result


def get_bit_n_sublist(input_list, n, bit_value=1):
    return [
        elem
        for i, elem in enumerate(input_list)
        if bool(i & (1 << n)) ^ bool(1 - bit_value)
    ]


def get_bit_n_subgroup(mob, n, bit_value=1):
    """
    If we enumerate mob, this returns a subgroup of all elements
    whose index has a binary representation with the n'th bit
    equal to bit_value
    """
    return VGroup(*get_bit_n_sublist(mob, n, bit_value))


class MillionRatio(Scene):
    def construct(self):
        # Largely copied from above
        N = 20
        words = OldTex(
            """
            {21 \\text{ parity bits}
            \\over
            1{,}048{,}576 \\text{ bits per block} }
            \\approx 0.00002
            """,
            tex_to_color_map={
                "21": GREEN,
                "1{,}048{,}576": WHITE,
                "0.00002": YELLOW,
            },
            fill_color=GREY_A
        )
        words.to_corner(UL, buff=MED_SMALL_BUFF)

        self.add(words)

        st = Square()
        st.set_stroke(GREY, 0.5)
        grid = VGroup(*[st.copy() for x in range(2**(16))])
        grid.arrange_in_grid(buff=0)
        grid.set_height(6)
        grid.next_to(words, DOWN, aligned_edge=LEFT)

        self.add(grid)

        k = 17
        positions = VGroup(*[
            OldTex(int_to_bit_string(n, n_bits=20))
            for n in [*range(k), *range(2**N - k // 2, 2**N)]
        ])
        positions.replace_submobject(-k // 2, OldTex("\\vdots"))
        positions.arrange(DOWN)
        positions.set_height(7)
        positions.to_edge(RIGHT)
        for n in [0, 1, 2, 4, 8, 16]:
            positions[n].set_color(GREEN_B)

        brace = Brace(positions, LEFT, buff=SMALL_BUFF)
        p_label = OldTexText("$2^{20}$\\\\positions")
        p_label.next_to(brace, LEFT, SMALL_BUFF)

        self.play(
            ShowIncreasingSubsets(positions, run_time=3),
            GrowFromPoint(brace, brace.get_top(), run_time=3, rate_func=squish_rate_func(smooth, 0.5, 1)),
            FadeIn(p_label, 0.5 * RIGHT, run_time=3, rate_func=squish_rate_func(smooth, 0.5, 1)),
        )
        self.wait()

        grid.set_stroke(background=True)
        for n in range(16):
            grid.set_fill(BLACK, 0)
            get_bit_n_subgroup(grid, n).set_fill(BLUE, 0.8)
            self.wait(0.5)
