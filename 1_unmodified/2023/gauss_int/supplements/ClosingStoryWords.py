# ==============================================================================
# Scene:      ClosingStoryWords
# Source:     videos/_2023/gauss_int/supplements.py (lines 100-105)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ClosingStoryWords.py ClosingStoryWords -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class StoryWords(InteractiveScene):
    quote = R"""
        ``There is a story about \\
        two friends who were \\
        classmates in high school...
    """

    def construct(self):
        # Test
        quote = TexText(self.quote, font_size=75, alignment=R"")
        quote.to_corner(DL)
        quote.set_backstroke(BLACK, 8)

        self.play(FadeIn(quote, lag_ratio=0.1, run_time=2))
        self.wait()


class ClosingStoryWords(StoryWords):
    quote = R"""
        ...surely the population has \\
        nothing to do with the \\
        circumference of the circle!''
    """
