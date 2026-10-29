# ==============================================================================
# Scene:      ScaleUp
# Source:     videos/_2020/hamming.py (lines 4902-4987)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ScaleUp.py ScaleUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class ScaleUp(Scene):
    def construct(self):
        square_template = Square()
        square_template.set_stroke(GREY_B, 2)
        square_template.set_height(1)
        zero = Integer(0)
        one = Integer(1)

        last_grid = None
        last_parity_groups = None
        last_words = None

        for N in range(4, 13):
            grid = VGroup(*[square_template.copy() for x in range(2**N)])
            grid.arrange_in_grid(
                2**int(math.floor(N / 2)),
                2**int(math.ceil(N / 2)),
                buff=0
            )
            grid.set_width(5.5)
            if N > 8:
                grid.set_stroke(width=1)
            elif N > 10:
                grid.set_stroke(width=0.25)
            grid.set_stroke(background=True)

            grid[0].set_fill(YELLOW, 0.6)
            for n in range(N):
                grid[2**n].set_fill(GREEN, 0.7)

            parity_groups = VGroup()
            for n in range(N):
                group = grid.copy()
                group.set_fill(BLACK, 0)
                get_bit_n_subgroup(group, n).set_fill(BLUE, 0.8)
                parity_groups.add(group)
            parity_groups.arrange_in_grid(n_cols=2, buff=1.5)
            parity_groups.set_width(5)
            max_height = 7
            if parity_groups.get_height() > max_height:
                parity_groups.set_height(max_height)
            parity_groups.to_edge(RIGHT, buff=0.5)

            random.seed(0)
            for square in grid:
                bit = random.choice([zero, one]).copy()
                bit.replace(square, dim_to_match=1)
                bit.scale(0.5)
                square.add(bit)

            redun = "{:.3}".format((N + 1) / (2**N))
            words = OldTex(
                f"""
                {{ {{{N + 1}}} \\text{{ parity bits}}
                \\over
                {2**N} \\text{{ bits per block}} }}
                \\approx {redun}
                """,
                tex_to_color_map={
                    f"{{{N + 1}}}": GREEN,
                    f"{2**N}": WHITE,
                    f"{redun}": YELLOW,
                },
                fill_color=GREY_A
            )
            words.to_corner(UL, buff=MED_SMALL_BUFF)
            grid.next_to(words, DOWN, aligned_edge=LEFT)

            if last_grid is None:
                self.add(grid)
                self.add(parity_groups)
                self.add(words)
            else:
                self.play(
                    ReplacementTransform(last_grid, grid[:2**(N - 1)]),
                    FadeIn(grid[2**(N - 1):], lag_ratio=0.1, run_time=2),
                    FadeOut(last_parity_groups),
                    LaggedStartMap(FadeIn, parity_groups, lag_ratio=0.2, run_time=2),
                    FadeOut(last_words, UP),
                    FadeIn(words, DOWN),
                )
            self.wait()

            last_grid = grid
            last_parity_groups = parity_groups
            last_words = words
