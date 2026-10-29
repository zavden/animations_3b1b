# ==============================================================================
# Scene:      VolumeEqualsPi
# Source:     videos/_2023/gauss_int/supplements.py (lines 556-560)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VolumeEqualsPi.py VolumeEqualsPi -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VolumeEqualsPi(InteractiveScene):
    def construct(self):
        text = TexText(R"Volume = $\pi$")
        text[R"\pi"].scale(2, about_edge=LEFT)
        self.add(text)
