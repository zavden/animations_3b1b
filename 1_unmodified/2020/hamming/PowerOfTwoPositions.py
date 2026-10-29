# ==============================================================================
# Scene:      PowerOfTwoPositions
# Source:     videos/_2020/hamming.py (lines 4190-4208)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PowerOfTwoPositions.py PowerOfTwoPositions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_bit_grid(n_rows, n_cols, bits=None, buff=MED_SMALL_BUFF, height=4):
    bit_pair = VGroup(Integer(0), Integer(1))
    bit_mobs = VGroup(*[
        bit_pair.copy()
        for x in range(n_rows * n_cols)
    ])
    bit_mobs.arrange_in_grid(n_rows, n_cols, buff=buff)
    bit_mobs.set_height(height)
    if bits is None:
        bits = np.random.randint(0, 2, len(bit_mobs))

    for bit_mob, bit in zip(bit_mobs, bits):
        bit_mob[1 - bit].set_opacity(0)

    bit_mobs.n_rows = n_rows
    bit_mobs.n_cols = n_cols
    return bit_mobs


def get_bit_grid_boxes(bit_grid, color=GREY_B, stroke_width=2):
    width = get_norm(bit_grid[1].get_center() - bit_grid[0].get_center())
    height = get_norm(bit_grid[bit_grid.n_cols].get_center() - bit_grid[0].get_center())
    return VGroup(*[
        Rectangle(
            height=height,
            width=width,
            stroke_color=color,
            stroke_width=stroke_width,
        ).move_to(bit)
        for bit in bit_grid
    ])


class PowerOfTwoPositions(Scene):
    def construct(self):
        block = get_bit_grid(4, 4)
        block.set_height(5)
        block.to_edge(LEFT, buff=LARGE_BUFF)
        boxes = get_bit_grid_boxes(block)

        numbers = VGroup(*[
            Integer(n).move_to(box)
            for n, box in enumerate(boxes)
        ])

        self.add(numbers)
        self.wait()
        for n in range(4):
            numbers[2**n].scale(1.5)
            numbers[2**n].set_color(YELLOW)
            self.wait(0.25)
        self.wait()
