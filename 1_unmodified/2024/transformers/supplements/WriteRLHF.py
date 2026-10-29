# ==============================================================================
# Scene:      WriteRLHF
# Source:     videos/_2024/transformers/supplements.py (lines 2193-2209)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteRLHF.py WriteRLHF -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteRLHF(InteractiveScene):
    def construct(self):
        words = VGroup(
            Text("Reinforcement"),
            Text("Learning with"),
            Text("Human"),
            Text("Feedback"),
        )
        words.scale(1.5)
        words.arrange(DOWN, aligned_edge=LEFT)
        words.set_color(GREY_A)
        self.play(LaggedStartMap(FadeIn, words, shift=0.25 * DOWN, lag_ratio=0.25))
        self.play(*(
            word[1:].animate.set_opacity(0.75)
            for word in words
        ))
        self.wait()
