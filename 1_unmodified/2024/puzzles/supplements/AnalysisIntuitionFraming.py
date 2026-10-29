# ==============================================================================
# Scene:      AnalysisIntuitionFraming
# Source:     videos/_2024/puzzles/supplements.py (lines 869-888)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AnalysisIntuitionFraming.py AnalysisIntuitionFraming -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AnalysisIntuitionFraming(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle())
        squares = Rectangle(4, 3).replicate(2)
        squares.set_height(4.5)
        squares.set_fill(BLACK, 1)
        squares.set_stroke(WHITE, 2)
        squares.arrange(RIGHT, buff=1.0)
        squares.move_to(0.5 * DOWN)

        titles = VGroup(Text("Analysis"), Text("Intuition"))
        titles.scale(1.5)
        for title, square in zip(titles, squares):
            title.next_to(square, UP)
        titles[0].align_to(titles[1], UP)

        self.add(squares)
        self.play(LaggedStartMap(FadeIn, titles))
        self.wait()
