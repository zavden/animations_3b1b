# ==============================================================================
# Scene:      AddedBubble
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 1048-1053)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddedBubble.py AddedBubble -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AddedBubble(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_corner(DL)
        self.play(randy.says("It follows from \n the CLT"))
        self.remove(randy)
