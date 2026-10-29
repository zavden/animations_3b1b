# ==============================================================================
# Scene:      DifferenceLine
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 522-534)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DifferenceLine.py DifferenceLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DifferenceLine(InteractiveScene):
    def construct(self):
        # Test
        line = Line(UP, DOWN).set_height(1).set_stroke(RED, 6)
        diff_word = Text("Difference")
        diff_word.next_to(line, RIGHT, SMALL_BUFF).shift(0.1 * DOWN)
        diff_word.set_color(RED)

        self.play(
            ShowCreation(line),
            FadeIn(diff_word, lag_ratio=0.1)
        )
        self.wait()
