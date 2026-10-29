# ==============================================================================
# Scene:      CountOutcomes
# Source:     videos/_2023/convolutions2/supplements.py (lines 186-190)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountOutcomes.py CountOutcomes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CountOutcomes(InteractiveScene):
    def construct(self):
        equation = Tex(R"6 \times 6 = 36 \text{ outcomes}")
        self.play(FadeIn(equation, lag_ratio=0.1))
        self.wait()
