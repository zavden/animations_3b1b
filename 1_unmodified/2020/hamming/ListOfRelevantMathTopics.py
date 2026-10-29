# ==============================================================================
# Scene:      ListOfRelevantMathTopics
# Source:     videos/_2020/hamming.py (lines 1090-1110)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ListOfRelevantMathTopics.py ListOfRelevantMathTopics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ListOfRelevantMathTopics(Scene):
    def construct(self):
        topics = VGroup(
            OldTexText("$L^1$ norm"),
            OldTexText("Sphere packing"),
            OldTexText("Finite sporadic groups (see Golay codes)"),
            OldTexText("Finite fields"),
            OldTexText("Galois extensions"),
            OldTexText("Lagrange interpolation (see Reed-Solomon)"),
            OldTexText("Discrete Fourier Transform"),
            OldTex("\\dots")
        )
        topics.arrange(RIGHT, buff=LARGE_BUFF)
        brown = interpolate_color(GREY_BROWN, WHITE, 0.25)
        for topic, color in zip(topics, it.cycle([BLUE_C, BLUE_D, BLUE_B, brown])):
            topic.set_color(color)

        topics.move_to(ORIGIN, LEFT)
        topics.to_edge(UP)
        self.play(topics.shift, (topics.get_width() - 5) * LEFT, run_time=12)
        self.wait()
