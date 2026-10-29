# ==============================================================================
# Scene:      WhyGaussian
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 236-241)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyGaussian.py WhyGaussian -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhyGaussian(InteractiveScene):
    def construct(self):
        question = TexText("What makes $e^{-x^2}$ special?", font_size=60)
        question.to_edge(UP, buff=LARGE_BUFF)
        self.play(Write(question))
        self.wait()
