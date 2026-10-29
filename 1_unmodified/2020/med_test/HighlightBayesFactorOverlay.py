# ==============================================================================
# Scene:      HighlightBayesFactorOverlay
# Source:     videos/_2020/med_test.py (lines 5748-5770)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighlightBayesFactorOverlay.py HighlightBayesFactorOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HighlightBayesFactorOverlay(Scene):
    def construct(self):
        rect = Rectangle(height=2, width=3)
        rect.set_stroke(BLUE, 3)
        words = OldTexText("How to\\\\use this")
        words.next_to(rect, DOWN, buff=1.5)
        words.shift(2 * RIGHT)
        words.match_color(rect)
        arrow = Arrow(
            words.get_left(),
            rect.get_bottom(),
            path_arc=-60 * DEGREES
        )
        arrow.match_color(words)

        self.play(
            FadeIn(words, scale=1.1),
            DrawBorderThenFill(arrow),
        )
        self.play(
            ShowCreation(rect),
        )
        self.wait()
