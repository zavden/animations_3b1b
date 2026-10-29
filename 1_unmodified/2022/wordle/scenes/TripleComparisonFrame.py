# ==============================================================================
# Scene:      TripleComparisonFrame
# Source:     videos/_2022/wordle/scenes.py (lines 3841-3864)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TripleComparisonFrame.py TripleComparisonFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TripleComparisonFrame(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        squares = Square().replicate(3)
        squares.stretch(0.9, 0)
        squares.arrange(RIGHT, buff=0.1)
        squares.set_width(FRAME_WIDTH - 0.5)
        squares.set_stroke(WHITE, 2)
        squares.set_fill(BLACK, 1)
        squares.to_edge(DOWN, buff=1.5)
        self.add(squares)

        titles = VGroup(
            OldTexText("V1: Just maximize\\\\entropy"),
            OldTexText("V2: Incorporate word\\\\frequency data"),
            OldTexText("V3: Use true wordle list\\\\(plus 1 or 2 other tricks)"),
        )
        titles.scale(0.75)
        for title, square in zip(titles, squares):
            title.next_to(square, UP)

        self.add(titles)

        self.embed()
