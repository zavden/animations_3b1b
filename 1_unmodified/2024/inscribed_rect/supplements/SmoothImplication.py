# ==============================================================================
# Scene:      SmoothImplication
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 677-694)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SmoothImplication.py SmoothImplication -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SmoothImplication(InteractiveScene):
    def construct(self):
        # Test
        smooth = Text("Smooth", font_size=72)
        implies = Tex(R"\Downarrow", font_size=120)
        tangent = Text("Every point has\na tangent line", font_size=60)
        words = VGroup(smooth, implies, tangent)
        words.arrange(DOWN, buff=0.5)
        words.to_edge(RIGHT)
        words.shift(UP)

        self.add(smooth)
        self.wait()
        self.play(
            Write(implies),
            FadeIn(tangent, 0.5 * DOWN),
        )
        self.wait()
