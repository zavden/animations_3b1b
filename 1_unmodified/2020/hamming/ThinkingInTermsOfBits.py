# ==============================================================================
# Scene:      ThinkingInTermsOfBits
# Source:     videos/_2020/hamming.py (lines 6271-6293)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl ThinkingInTermsOfBits.py ThinkingInTermsOfBits -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/chess.py -----

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]



# ----- From _2020/hamming.py -----

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


def string_to_bits(message):
    return [int(b) for b in string_to_bools(message)]


def toggle_bit_anim(bit, target_color=None, **kwargs):
    original = bit.copy()
    original[1 - get_bit_mob_value(original)].rotate(PI)
    toggle_bit(bit)
    if target_color is not None:
        bit.set_color(target_color)

    if "path_arc" not in kwargs:
        kwargs["path_arc"] = PI

    return TransformFromCopy(original, bit, **kwargs)


class ThinkingInTermsOfBits(Scene):
    def construct(self):
        word = OldTexText("Information")
        word.scale(2)
        word.next_to(ORIGIN, LEFT, buff=0.7)
        bits = get_bit_grid(11, 8, bits=string_to_bits("Information"))
        bits.set_height(6)
        bits.next_to(ORIGIN, RIGHT, buff=0.7)
        bits.set_color(GREY_A)

        for bit in bits:
            toggle_bit(bit)

        bits.shuffle()

        self.add(word)
        self.add(bits)
        self.play(LaggedStartMap(
            toggle_bit_anim, bits,
            lag_ratio=5 / len(bits),
            run_time=3,
        ))
        self.wait(2)
