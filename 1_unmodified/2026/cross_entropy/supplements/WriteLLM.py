# ==============================================================================
# Scene:      WriteLLM
# Source:     videos/_2026/cross_entropy/supplements.py (lines 263-270)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteLLM.py WriteLLM -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteLLM(InteractiveScene):
    def construct(self):
        llm = Text("LLM", font_size=72)
        llm.arrange(DOWN)

        self.play(FadeIn(llm, lag_ratio=0.1))
        self.wait(0.5)
        self.play(FadeOut(llm))
