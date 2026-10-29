# ==============================================================================
# Scene:      UnitCircleAndSquare
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1387-1400)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnitCircleAndSquare.py UnitCircleAndSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnitCircleAndSquare(InteractiveScene):
    def construct(self):
        radius = 2
        circle = Circle(radius=radius)
        circle.set_fill(BLUE, 0.2)
        circle.set_stroke(BLUE, 3)
        square = Square(side_length=radius)
        square.set_stroke(RED, 3)
        square.set_fill(RED, 0.25)
        square.move_to(circle.get_center(), DL)
        one_label = Integer(1)
        one_label.next_to(square.get_bottom(), UP, SMALL_BUFF)

        self.add(circle, square, one_label)
