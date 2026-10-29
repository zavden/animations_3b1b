# ==============================================================================
# Scene:      WhyPointToError
# Source:     videos/_2020/hamming.py (lines 5442-5467)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyPointToError.py WhyPointToError -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyPointToError(Scene):
    def construct(self):
        rect = SurroundingRectangle(OldTexText("0000").scale(2))
        rect.to_edge(RIGHT)
        rect.set_stroke(RED, 3)
        words = OldTexText("Why do these\\\\point to an error?")
        arrow = Vector(0.7 * RIGHT)
        arrow.next_to(rect, LEFT)
        words.next_to(arrow, LEFT)
        words.set_color(RED)

        bit = Integer(0).scale(2)
        bit.next_to(words, UP, buff=0.45)
        bit.shift(1.11 * words.get_width() * LEFT)

        self.play(
            Write(words),
            ShowCreation(rect),
        )
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(
            rect.become, SurroundingRectangle(bit).match_style(rect),
            FadeOut(arrow)
        )
        self.wait()
