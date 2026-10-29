# ==============================================================================
# Scene:      WhyGaussian
# Source:     videos/_2023/clt_proof/main.py (lines 55-57)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyGaussian.py WhyGaussian -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyGaussian(InteractiveScene):
    def construct(self):
        self.add(TexText("Why $e^{-x^2}$?", font_size=72))
