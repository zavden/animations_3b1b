# ==============================================================================
# Scene:      DInputAndOutputOfValue
# Source:     videos/_2024/transformers/supplements.py (lines 1207-1226)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DInputAndOutputOfValue.py DInputAndOutputOfValue -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DInputAndOutputOfValue(InteractiveScene):
    def construct(self):
        # Test
        d_embed = 12_288
        in_label, out_label = [
            VGroup(Text(text), Integer(d_embed))
            for text in ["d_input", "d_output"]
        ]
        for label, shift in [(in_label, LEFT), (out_label, RIGHT)]:
            label.arrange(DOWN)
            label.scale(0.65)
            label.next_to(ORIGIN, UP, buff=LARGE_BUFF)
            label.shift(1.0 * shift)
            arrow = Arrow(label, 0.5 * shift)
            label.add(arrow)

        self.play(FadeIn(in_label, lag_ratio=0.1))
        self.wait()
        self.play(FadeIn(out_label, lag_ratio=0.1))
        self.wait()
