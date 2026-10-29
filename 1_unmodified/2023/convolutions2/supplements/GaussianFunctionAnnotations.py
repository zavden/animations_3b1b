# ==============================================================================
# Scene:      GaussianFunctionAnnotations
# Source:     videos/_2023/convolutions2/supplements.py (lines 854-865)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GaussianFunctionAnnotations.py GaussianFunctionAnnotations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class GaussianFunctionAnnotations(InteractiveScene):
    def construct(self):
        # Test
        tex_kw = dict(font_size=36, t2c={"x": BLUE, "y": YELLOW})
        functions = VGroup(
            Tex(R"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-x^2 / 2\sigma^2}", **tex_kw),
            Tex(R"g(y) = \frac{1}{\sigma \sqrt{2\pi}} e^{-y^2 / 2\sigma^2}", **tex_kw),
        )
        functions.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        functions.to_corner(UL)

        self.add(functions)
