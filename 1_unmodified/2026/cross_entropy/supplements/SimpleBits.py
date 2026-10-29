# ==============================================================================
# Scene:      SimpleBits
# Source:     videos/_2026/cross_entropy/supplements.py (lines 1057-1066)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl SimpleBits.py SimpleBits -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


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



# ----- From _2026/cross_entropy/supplements.py -----

class SimpleBits(InteractiveScene):
    def construct(self):
        # Test
        bits = bit_string_mobject("0100100001010000")
        bits.set_width(5)
        bits.space_out_submobjects(1.2)
        bits.center()
        for bit in bits:
            bit.set_opacity(clip(inverse_interpolate(2.5, 1.75, abs(bit.get_x())), 0, 1))
        self.add(bits)
