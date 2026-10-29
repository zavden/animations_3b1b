# ==============================================================================
# Scene:      ReferenceLargerContextTechnologies
# Source:     videos/_2024/transformers/supplements.py (lines 1070-1093)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceLargerContextTechnologies.py ReferenceLargerContextTechnologies -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReferenceLargerContextTechnologies(InteractiveScene):
    def construct(self):
        # Test
        words = VGroup(
            Text("Sparse Attention Mechanisms"),
            Text("Blockwise Attention"),
            Text("Linformer"),
            Text("Reformer"),
            Text("Ring attention"),
            Text("Longformer"),
            Text("Adaptive Attention Span"),
            Tex(R"\vdots")
        )
        words.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        words[-1].shift(0.5 * RIGHT)

        self.play(
            LaggedStartMap(FadeIn, words, shift=0.5 * DOWN, lag_ratio=0.5, run_time=4)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, words, shift=RIGHT, lag_ratio=0.1)
        )
        self.wait()
