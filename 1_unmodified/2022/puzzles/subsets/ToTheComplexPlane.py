# ==============================================================================
# Scene:      ToTheComplexPlane
# Source:     videos/_2022/puzzles/subsets.py (lines 4999-5019)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ToTheComplexPlane.py ToTheComplexPlane -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ToTheComplexPlane(InteractiveScene):
    def construct(self):
        plane = ComplexPlane()
        plane.add_coordinate_labels()
        label = Text("Complex plane")
        label.to_corner(UL, buff=MED_SMALL_BUFF)
        label.set_backstroke(width=10)
        poly = Tex(
            "f(x) = (1 + x)(1 + x^2)\\cdots\\left(1+x^{2{,}000}\\right)",
            tex_to_color_map={"x": YELLOW}
        )
        poly.scale(0.75)
        poly.next_to(label, DOWN, MED_LARGE_BUFF, LEFT)
        poly.set_backstroke(width=8)

        self.play(
            Write(plane),
            Write(label),
        )
        self.play(FadeIn(poly, DOWN))
        self.wait()
