# ==============================================================================
# Scene:      ThreeDExpression
# Source:     videos/_2023/gauss_int/supplements.py (lines 934-943)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDExpression.py ThreeDExpression -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeDExpression(InteractiveScene):
    def construct(self):
        expr = Tex(
            R"{1 \over \sigma^3 (2\pi)^{3/2}} e^{-(x^2 + y^2 + z^2) / 2 \sigma^2}",
            t2c={R"\sigma": RED},
            font_size=48
        )
        expr[R"1 \over \sigma^3 (2\pi)^{3/2}}"].scale(0.7, about_edge=RIGHT)
        expr.to_corner(UL)
        self.add(expr)
