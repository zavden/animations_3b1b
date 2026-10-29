# ==============================================================================
# Scene:      MovingBrace
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 74-83)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MovingBrace.py MovingBrace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MovingBrace(InteractiveScene):
    def construct(self):
        squares = Square().replicate(3)
        squares.arrange(RIGHT)
        squares.set_width(FRAME_WIDTH - 1)
        brace = Brace(squares[0], UP)
        self.play(GrowFromCenter(brace))
        self.wait()
        self.play(brace.animate.match_x(squares[1]))
        self.wait()
