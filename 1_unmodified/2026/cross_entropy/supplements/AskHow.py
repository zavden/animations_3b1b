# ==============================================================================
# Scene:      AskHow
# Source:     videos/_2026/cross_entropy/supplements.py (lines 169-175)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskHow.py AskHow -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskHow(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        self.play(randy.thinks("How?", mode="maybe", look_at=3 * UR))
        self.play(Blink(randy))
        self.wait()
