# ==============================================================================
# Scene:      RotationalSymmetryAnnotations
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 425-465)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationalSymmetryAnnotations.py RotationalSymmetryAnnotations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RotationalSymmetryAnnotations(InteractiveScene):
    def construct(self):
        # Add equation
        kw = dict(t2c={"x": BLUE, "y": YELLOW, "r": RED})
        top_eq = Tex("f(x)g(y) = e^{-x^2} e^{-y^2}", **kw)
        top_eq_lhs = top_eq["f(x)g(y)"][0]
        top_eq_rhs = top_eq["= e^{-x^2} e^{-y^2}"][0]
        top_eq.to_corner(UL)

        self.add(top_eq)

        # Expand equation
        rhs2 = Tex("= e^{-(x^2 + y^2)}", **kw)
        rhs3 = Tex("= e^{-r^2}", **kw)

        rhs2.next_to(top_eq_rhs, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        rhs3.next_to(rhs2, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        xy_rect = SurroundingRectangle(rhs2["x^2 + y^2"], buff=0.05)
        r_rect = SurroundingRectangle(rhs3["r^2"], buff=0.05)
        rects = VGroup(xy_rect, r_rect)
        rects.set_stroke(RED, 1)

        self.play(
            TransformMatchingShapes(
                top_eq_rhs.copy(), rhs2,
                path_arc=30 * DEGREES,
            )
        )
        self.wait()
        self.play(ShowCreation(xy_rect))
        self.play(
            TransformMatchingTex(
                rhs2.copy(), rhs3,
                key_map={"x^2 + y^2": "r^2"},
                run_time=1
            ),
            TransformFromCopy(xy_rect, r_rect),
        )
        self.play(FadeOut(rects))
        self.wait()
