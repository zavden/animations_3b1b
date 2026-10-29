# ==============================================================================
# Scene:      ChangeAnywhereToOneBit
# Source:     videos/_2020/hamming.py (lines 2356-2403)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChangeAnywhereToOneBit.py ChangeAnywhereToOneBit -w -m --fps 15
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


def get_bit_mob_value(bit_mob):
    return int(bit_mob[1].get_fill_opacity() > bit_mob[0].get_fill_opacity())


def toggle_bit(bit):
    for sm in bit:
        sm.set_fill(opacity=1 - sm.get_fill_opacity())
    return bit


def get_ones(block):
    result = VGroup()
    for bit in block:
        if isinstance(bit, Integer):
            value = bit.get_value()
        else:
            value = get_bit_mob_value(bit)
        if value == 1:
            result.add(bit)
    return result


def get_one_rects(block, buff=SMALL_BUFF):
    rects = VGroup()
    for bit in get_ones(block):
        rect = SurroundingRectangle(bit, buff=buff)
        rect.set_stroke(YELLOW, 3)
        rect.set_fill(YELLOW, 0.2)
        rects.add(rect)
    return rects


def toggle_bit_anim(bit, target_color=None, **kwargs):
    original = bit.copy()
    original[1 - get_bit_mob_value(original)].rotate(PI)
    toggle_bit(bit)
    if target_color is not None:
        bit.set_color(target_color)

    if "path_arc" not in kwargs:
        kwargs["path_arc"] = PI

    return TransformFromCopy(original, bit, **kwargs)


class ChangeAnywhereToOneBit(Scene):
    CONFIG = {
        "random_seed": 3,
    }

    def construct(self):
        title = VGroup(
            OldTexText("Change anywhere"),
            Vector(RIGHT),
            OldTexText("One bit of information"),
        )
        title.arrange(RIGHT)
        title.set_width(FRAME_WIDTH - 1)
        title.to_edge(UP)
        self.add(title)

        grid = get_bit_grid(4, 4)
        grid.set_height(4)
        grid.match_x(title[0])
        grid.set_y(-1)
        self.add(grid)

        one_rects = get_one_rects(grid)
        self.add(one_rects)

        parity_words = VGroup(
            OldTexText("Even \\# of 1s", color=BLUE_B),
            OldTexText("Odd \\# of 1s", color=TEAL_D),
        )
        parity_words.scale(1.5)
        parity_words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        parity_words.match_x(title[2])
        parity_words.match_y(grid)
        self.add(parity_words)

        def get_parity_rect(n, words=parity_words):
            return SurroundingRectangle(words[n % 2])

        p_rect = get_parity_rect(len(one_rects))
        self.add(p_rect)

        # Random changes
        for x in range(10):
            bit = random.choice(grid)
            self.play(toggle_bit_anim(bit))
            one_rects.set_submobjects(get_one_rects(grid))
            p_rect.become(get_parity_rect(len(one_rects)))
            self.wait()
