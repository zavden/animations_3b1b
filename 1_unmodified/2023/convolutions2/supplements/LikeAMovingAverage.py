# ==============================================================================
# Scene:      LikeAMovingAverage
# Source:     videos/_2023/convolutions2/supplements.py (lines 453-462)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LikeAMovingAverage.py LikeAMovingAverage -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LikeAMovingAverage(InteractiveScene):
    def construct(self):
        words = Text("Kind of like\na moving average")
        top_words = words["Kind of like"]
        cross = Cross(top_words)

        self.play(FadeIn(words, lag_ratio=0.1))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
