# ==============================================================================
# Scene:      InaccurateComputation
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2948-3023)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InaccurateComputation.py InaccurateComputation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InaccurateComputation(Scene):
    def construct(self):
        h_line = DashedLine(LEFT_SIDE, RIGHT_SIDE)
        h_line.to_edge(UP, buff=1.5)
        words = VGroup(
            OldTexText("Real number"),
            OldTexText("IEEE 754\\\\representation"),
            OldTexText("Error"),
        )
        for i, word in zip([-1, 0, 1], words):
            word.next_to(h_line, UP)
            word.shift(i * FRAME_WIDTH * RIGHT / 3)

        lines = VGroup(*[
            DashedLine(TOP, BOTTOM)
            for x in range(4)
        ])
        lines.arrange(RIGHT)
        lines.stretch_to_fit_width(FRAME_WIDTH)

        self.add(h_line, lines[1:-1], words)

        numbers = VGroup(
            OldTex("\\pi").scale(2),
            OldTex("e^{\\sqrt{163}\\pi}").scale(1.5),
        )
        numbers.set_color(YELLOW)
        numbers.set_stroke(width=0, background=True)

        bit_strings = VGroup(
            OldTex(
                "01000000",
                "01001001",
                "00001111",
                "11011011",
            ),
            OldTex(
                "01011100",
                "01101001",
                "00101110",
                "00011001",
            )
        )
        for mob in bit_strings:
            mob.arrange(DOWN, buff=SMALL_BUFF)
            for word in mob:
                for submob, bit in zip(word, word.get_tex()):
                    if bit == "0":
                        submob.set_color(GREY_B)
        errors = VGroup(
            OldTex(
                "\\approx 8.7422 \\times 10^{-8}"
            ),
            OldTex(
                "\\approx 5{,}289{,}803{,}032.00",
            ),
        )
        errors.set_color(RED)

        content = VGroup(numbers, bit_strings, errors)

        for group, word in zip(content, words):
            group[1].shift(3 * DOWN)
            group.move_to(DOWN)
            group.match_x(word)

        self.play(*map(Write, numbers))
        self.wait()
        self.play(
            TransformFromCopy(numbers, bit_strings),
            lag_ratio=0.01,
            run_time=2,
        )
        self.wait()
        self.play(FadeIn(errors, 3 * LEFT))
        self.wait()
