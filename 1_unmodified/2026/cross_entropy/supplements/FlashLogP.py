# ==============================================================================
# Scene:      FlashLogP
# Source:     videos/_2026/cross_entropy/supplements.py (lines 780-791)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FlashLogP.py FlashLogP -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FlashLogP(InteractiveScene):
    def construct(self):
        # Test
        tex = Tex(R"-\log_2(p)")
        tex.set_fill(opacity=0)
        tex.set_stroke(YELLOW, 5, 0.25)
        flash_parts = VGroup(
            tex.copy().scale(1.02**n)
            for n in range(1, 20)
        )
        self.play(LaggedStartMap(VFadeInThenOut, flash_parts))
        self.wait()
