# ==============================================================================
# Scene:      StreamOfBits
# Source:     videos/_2026/cross_entropy/supplements.py (lines 567-586)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl StreamOfBits.py StreamOfBits -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


# ----- From _2026/cross_entropy/entropy.py -----

def bit_string_mobject(
    bit_string: str,
    font: str = "Consolas",
    font_size: int = 48,
    colors: List[Colors] = [GREY_C, GREY_B]
):
    result = Text(bit_string, font=font, font_size=font_size)
    result["0"].set_color(colors[0])
    result["1"].set_color(colors[1])
    return result


def int_to_bit_string(n_bits, value=None, **kwargs):
    if value is None:
        value = np.random.randint(0, 2**n_bits)
    return bit_string_mobject(f"{value:0{n_bits}b}", **kwargs)



# ----- From _2026/cross_entropy/supplements.py -----

class StreamOfBits(InteractiveScene):
    def construct(self):
        # Test
        radius = 5
        bits = int_to_bit_string(n_bits=50)

        def update_bit(bit):
            r = get_norm(bit.get_center())
            op = inverse_interpolate(radius, 0.8 * radius, r)
            bit.set_fill(opacity=op)

        for bit in bits:
            bit.move_to(radius * RIGHT)
            bit.add_updater(update_bit)

        self.play(
            bits.animate.shift(2 * radius * LEFT).set_anim_args(lag_ratio=0.05, rate_func=bezier([0, 0, 1, 1])),
            run_time=20
        )
        self.wait()
