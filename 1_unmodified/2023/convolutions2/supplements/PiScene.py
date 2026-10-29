# ==============================================================================
# Scene:      PiScene
# Source:     videos/_2023/convolutions2/supplements.py (lines 878-889)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiScene.py PiScene -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PiScene(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=1.5)
        randy = Randolph(height=1.5)
        morty.set_x(3).to_edge(UP)
        randy.set_x(-3).to_edge(UP)

        self.play(
            morty.change("pondering", ORIGIN),
            randy.change("thinking", ORIGIN),
        )
        self.wait()
