# ==============================================================================
# Scene:      SquarePyramid
# Source:     videos/_2026/spheres_talk/supplements.py (lines 597-624)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquarePyramid.py SquarePyramid -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquarePyramid(InteractiveScene):
    def construct(self):
        # Show pyramid
        frame = self.frame

        n_squares = 40
        max_side_length = 2
        squares = VGroup(
            Square(side_length)
            for side_length in np.linspace(max_side_length, 0.01, n_squares)
        )
        squares.arrange(OUT, buff=max_side_length / n_squares)
        squares.set_fill(RED, 0.2)
        squares.set_stroke(RED, 2, 0.5)

        frame.reorient(21, 67, 0, (-0.2, -0.12, -0.92), 4.41)
        self.play(
            LaggedStartMap(FadeIn, squares, shift=RIGHT, lag_ratio=0.35, run_time=8),
        )

        # Volume
        label =Tex(R"\text{Vol.} = \frac{1}{3} \text{B} \times \text{H}", font_size=72)
        label.fix_in_frame()
        label.to_edge(DOWN)
        label.set_backstroke(BLACK, 5)

        self.play(Write(label))
        self.wait()
