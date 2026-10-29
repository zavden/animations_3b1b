# ==============================================================================
# Scene:      RotationIn2D
# Source:     videos/_2026/hairy_ball/supplements.py (lines 883-905)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationIn2D.py RotationIn2D -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotationIn2D(InteractiveScene):
    def construct(self):
        # Test
        grid = NumberPlane()
        back_grid = grid.copy()
        back_grid.background_lines.set_stroke(GREY, 1)
        back_grid.axes.set_stroke(GREY, 1, 1)
        back_grid.faded_lines.set_stroke(GREY, 0.5, 0.5)

        basis_vectors = VGroup(
            Vector(RIGHT).set_color(GREEN),
            Vector(UP).set_color(RED),
        )

        self.frame.set_height(4)
        self.add(back_grid, grid, basis_vectors)
        self.wait()
        self.play(
            Rotate(basis_vectors, PI, about_point=ORIGIN),
            Rotate(grid, PI, about_point=ORIGIN),
            run_time=5
        )
        self.wait()
