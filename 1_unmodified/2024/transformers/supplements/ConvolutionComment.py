# ==============================================================================
# Scene:      ConvolutionComment
# Source:     videos/_2024/transformers/supplements.py (lines 604-621)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConvolutionComment.py ConvolutionComment -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ConvolutionComment(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        morty.to_corner(DR)
        bubble = morty.get_bubble(Text("""
            In other models, the weighted
            sums can be grouped differently,
            e.g. as convolutions, but for
            Transformers it's always
            matrix-vector multiplication.
        """, font_size=36, alignment="LEFT"), bubble_type=SpeechBubble)

        self.add(bubble)
        self.play(morty.change("speaking"))
        for x in range(2):
            self.play(Blink(morty))
            self.wait()
