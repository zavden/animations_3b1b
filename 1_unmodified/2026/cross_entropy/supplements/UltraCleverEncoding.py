# ==============================================================================
# Scene:      UltraCleverEncoding
# Source:     videos/_2026/cross_entropy/supplements.py (lines 729-759)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl UltraCleverEncoding.py UltraCleverEncoding -w -m --fps 15
#
# Notes:
#   arrow.svg is the faithful conversion of images/arrow.ai (PDF) to SVG with pdftocairo.
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


class InstructionArrow(SVGMobject):
    def __init__(self, direction=RIGHT, width=0.5, *args, **kwargs):
        super().__init__("arrow.svg", *args, **kwargs)
        self.set_width(width)
        self.rotate(angle_of_vector(direction))
        self.direction = direction


class ArrowGroup(VGroup):
    def __init__(self):
        super().__init__(InstructionArrow(v) for v in [UP, DOWN, LEFT, RIGHT])



# ----- From _2026/cross_entropy/supplements.py -----

class UltraCleverEncoding(InteractiveScene):
    def construct(self):
        # Test
        arrow_group = ArrowGroup()
        arrows = VGroup(
            arrow_group[i].copy()[0]
            for i in [1, 0, 2, 0, 2, 0, 1, 3, 1, 1, 0, 0, 0, 3, 2, 0]
        )
        arrows.set_fill(TEAL)
        arrows.arrange(RIGHT)

        lower_jumble = arrows.copy()
        lower_jumble.set_fill(opacity=0.5)
        for arrow in lower_jumble:
            arrow.scale(1.5)
            arrow.next_to(arrows, DOWN, MED_SMALL_BUFF)
            arrow.shift(np.random.uniform(-0.2, 0.2, 3))

        bits = int_to_bit_string(n_bits=len(arrows), font="CMU Serif")
        bits.space_out_submobjects(1.2)
        bits.next_to(arrows, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT).shift(SMALL_BUFF * LEFT)
        bits.set_color(TEAL)

        self.add(arrows)
        self.wait()
        self.play(
            TransformFromCopy(arrows, lower_jumble, path_arc=30 * DEG, lag_ratio=0.01)
        )
        self.play(VShowPassingFlash(lower_jumble.copy().set_fill(opacity=0).set_stroke(YELLOW, 3), time_width=1.5, run_time=3))
        self.play(ReplacementTransform(lower_jumble, bits, lag_ratio=0.01, path_arc=10 * DEG, run_time=2))
        self.wait()
