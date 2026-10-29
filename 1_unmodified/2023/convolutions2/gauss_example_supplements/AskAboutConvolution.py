# ==============================================================================
# Scene:      AskAboutConvolution
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 244-253)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutConvolution.py AskAboutConvolution -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutConvolution(InteractiveScene):
    def construct(self):
        text = TexText(
            "Convolution between $e^{-x^2}$ and $e^{-y^2}$",
            t2c={"x": BLUE, "y": YELLOW},
            font_size=60
        )
        text.to_edge(UP, buff=MED_LARGE_BUFF)
        text.set_backstroke(width=2)
        self.add(text)
