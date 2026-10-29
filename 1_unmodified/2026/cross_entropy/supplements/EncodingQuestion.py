# ==============================================================================
# Scene:      EncodingQuestion
# Source:     videos/_2026/cross_entropy/supplements.py (lines 589-669)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl EncodingQuestion.py EncodingQuestion -w -m --fps 15
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

class EncodingQuestion(InteractiveScene):
    def construct(self):
        # Question
        question = Text("Most Efficient Encoding?", font_size=90)
        question.to_edge(UP, buff=0.75)

        arrow_group = ArrowGroup()
        arrow_group.set_fill(YELLOW)
        n_instructions = 24
        indices = random.choices(list(range(4)), weights=[0.5, 0.25, 0.125, 0.125], k=n_instructions)
        arrows = VGroup(
            arrow_group[idx].copy().move_to(0.75 * n * RIGHT)
            for n, idx in enumerate(indices)
        )
        arrows.set_max_width(FRAME_WIDTH - 1)
        arrows.next_to(question, DOWN, MED_LARGE_BUFF)

        self.play(
            FadeIn(arrows, shift=2 * LEFT, path_arc=30 * DEG, lag_ratio=0.05),
            run_time=2
        )

        # Encode
        naive_codewords = ["00", "01", "10", "11"]
        optimal_codewords = ["0", "10", "110", "111"]

        encoding = VGroup(
            bit_string_mobject(naive_codewords[idx])
            for idx in indices
        )
        buff = get_norm(encoding[0][0].get_right() - encoding[0][1].get_left())
        encoding.arrange(RIGHT, buff=buff)
        encoding.match_width(arrows)
        encoding.next_to(arrows, DOWN, MED_LARGE_BUFF)

        self.play(
            Write(question),
            LaggedStart(
                (TransformFromCopy(arrow, bits)
                for arrow, bits in zip(arrows, encoding)),
                lag_ratio=0.1,
            ),
            run_time=2
        )
        self.wait()

        # Squish
        rect = SurroundingRectangle(encoding, buff=0)
        rect.set_opacity(0)
        full_width = rect.get_width()
        n_bits = 2 * n_instructions

        outer_arrows = VGroup(
            Vector(v, thickness=8)
            for v in [RIGHT, LEFT]
        )
        outer_arrows.set_fill(RED)
        outer_arrows[0].add_updater(lambda m: m.next_to(rect, LEFT, SMALL_BUFF))
        outer_arrows[1].add_updater(lambda m: m.next_to(rect, RIGHT, SMALL_BUFF))

        def get_new_bit_string():
            new_n_bits = int((rect.get_width() / full_width) * n_bits)
            np.random.seed(new_n_bits)
            new_bits = int_to_bit_string(new_n_bits)
            new_bits.match_height(encoding)
            new_bits.move_to(rect)
            return new_bits

        new_bits = always_redraw(get_new_bit_string)

        self.remove(encoding)
        self.add(new_bits)
        rect.shift(RIGHT)
        self.play(FadeIn(outer_arrows, run_time=0.5))
        self.play(
            rect.animate.stretch(0.6, 0, about_edge=LEFT),
            run_time=5
        )
        self.wait()
        self.play(FadeOut(outer_arrows))
        self.wait()
