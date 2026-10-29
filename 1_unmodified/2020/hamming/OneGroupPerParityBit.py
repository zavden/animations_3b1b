# ==============================================================================
# Scene:      OneGroupPerParityBit
# Source:     videos/_2020/hamming.py (lines 4211-4230)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneGroupPerParityBit.py OneGroupPerParityBit -w -m --fps 15
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


def get_grid_position_labels(boxes, height=0.25):
    labels = VGroup()
    for n, box in enumerate(boxes):
        label = Integer(n)
        label.set_height(height)
        label.move_to(box, DR)
        label.shift(SMALL_BUFF * UL)
        labels.add(label)
    return labels


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


class OneGroupPerParityBit(Scene):
    def construct(self):
        N = 4
        block = get_bit_grid(2**(N // 2), 2**(N // 2))
        block.set_height(5)
        block.to_edge(LEFT, buff=LARGE_BUFF)
        boxes = get_bit_grid_boxes(block)
        pos_labels = get_grid_position_labels(boxes)

        for bit in block:
            bit.scale(0.7)

        parity_boxes = VGroup(*[boxes[2**n] for n in range(N)])
        parity_boxes.set_fill(GREEN, 0.8)
        block.save_state()
        self.add(boxes, pos_labels, block)
        for n in range(4):
            block.restore()
            get_bit_n_subgroup(block, n, 0).set_fill(opacity=0)
            self.wait(1.5)
