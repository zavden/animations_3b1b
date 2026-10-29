# ==============================================================================
# Scene:      LastSideBySide
# Source:     videos/_2022/visual_proofs/lies.py (lines 2332-2355)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastSideBySide.py LastSideBySide -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastSideBySide(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        squares = Square().replicate(2)
        squares.set_stroke(WHITE, 2)
        squares.set_fill(BLACK, 2)
        squares.set_height(5)
        squares.set_width(6, stretch=True)
        for square, vect in zip(squares, [LEFT, RIGHT]):
            square.move_to(FRAME_WIDTH * vect / 4)
        squares.to_edge(DOWN, buff=0.7)
        self.add(squares)

        titles = VGroup(
            OldTexText("Given examples\\\\like this..."),
            OldTexText("What's needed to\\\\make this rigorous?"),
        )
        for title, square in zip(titles, squares):
            title.next_to(square, UP, buff=MED_LARGE_BUFF)

        self.play(Write(titles[0]))
        self.wait()
        self.play(Write(titles[1]))
        self.wait()
