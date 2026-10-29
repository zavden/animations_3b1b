# ==============================================================================
# Scene:      CarFactoryNumbers
# Source:     videos/_2020/beta/beta1.py (lines 2012-2056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CarFactoryNumbers.py CarFactoryNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CarFactoryNumbers(Scene):
    def construct(self):
        # Test words
        denom_words = OldTexText(
            "in a test of 100 cars",
            tex_to_color_map={"100": BLUE},
        )
        denom_words.to_corner(UR)

        numer_words = OldTexText(
            "2 defects found",
            tex_to_color_map={"2": RED}
        )
        numer_words.move_to(denom_words, LEFT)

        self.play(Write(denom_words, run_time=1))
        self.wait()
        self.play(
            denom_words.next_to, numer_words, DOWN, {"aligned_edge": LEFT},
            FadeIn(numer_words),
        )
        self.wait()

        # Question words
        question = VGroup(
            OldTexText("How do you plan"),
            OldTexText("for"),
            Integer(int(1e6), color=BLUE),
            OldTexText("cars?")
        )
        question[1:].arrange(RIGHT, aligned_edge=DOWN)
        question[2].shift(
            (question[2][1].get_bottom()[1] - question[2][0].get_bottom()[1]) * UP
        )
        question[1:].next_to(question[0], DOWN, aligned_edge=LEFT)
        question.next_to(denom_words, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        self.play(
            UpdateFromAlphaFunc(
                question,
                lambda m, a: m.set_opacity(a),
            ),
            CountInFrom(question[2], 0, run_time=1.5)
        )
        self.wait()
