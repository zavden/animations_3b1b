# ==============================================================================
# Scene:      PiCreatureSmiles
# Source:     videos/_2026/cross_entropy/robot.py (lines 8109-8115)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCreatureSmiles.py PiCreatureSmiles -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PiCreatureSmiles(InteractiveScene):
    def construct(self):
        # Randy smiles
        randy = Randolph("happy", flip_at_start=True)
        self.play(FadeIn(randy, shift=LEFT))
        self.wait(0.5)
        self.play(randy.change("hooray", self.camera.frame.get_corner(UL)))
