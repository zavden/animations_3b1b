# ==============================================================================
# Scene:      CrossEntropyWords
# Source:     videos/_2026/cross_entropy/supplements.py (lines 305-319)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CrossEntropyWords.py CrossEntropyWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CrossEntropyWords(InteractiveScene):
    def construct(self):
        text = Text("“Cross-entropy” loss", font_size=72)
        text.to_edge(UP)
        ce = text["Cross-entropy"]
        underline = Underline(ce)
        underline.set_stroke(color=PINK)

        self.play(FadeIn(text, UP))
        self.wait()
        self.play(
            ShowCreation(underline),
            ce.animate.set_color(PINK),
        )
        self.wait()
