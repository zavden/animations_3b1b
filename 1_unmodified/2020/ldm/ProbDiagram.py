# ==============================================================================
# Scene:      ProbDiagram
# Source:     videos/_2020/ldm.py (lines 1214-1242)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProbDiagram.py ProbDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProbDiagram(Scene):
    def construct(self):
        square = Square(side_length=1)
        square.move_to(ORIGIN, DL)
        square.set_stroke(width=0)
        square.set_fill(BLUE_E, 1)

        frame = self.camera.frame
        frame.set_height(1.5)
        frame.move_to(square)

        tri = Polygon(ORIGIN, UP, UR)
        tri.set_fill(BLUE_E, 1)
        tri.set_stroke(width=0)

        tris = VGroup(tri)
        N = 1000
        for n in range(1, N):
            tri = Polygon(
                ORIGIN,
                RIGHT + UP / n,
                RIGHT + UP / (n + 1),
            )
            tri.set_stroke(width=0)
            color = BLUE_E if (n % 2 == 0) else RED_D
            tri.set_fill(color, 1)
            tris.add(tri)

        self.add(tris)
