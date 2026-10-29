# ==============================================================================
# Scene:      PredictTheProof
# Source:     videos/_2023/convolutions2/supplements.py (lines 868-875)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PredictTheProof.py PredictTheProof -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PredictTheProof(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=2)
        morty.to_corner(DR)
        self.play(morty.says("Try predicting\nthe proof!"))
        for x in range(3):
            self.play(Blink(morty))
            self.wait(4 * random.random())
