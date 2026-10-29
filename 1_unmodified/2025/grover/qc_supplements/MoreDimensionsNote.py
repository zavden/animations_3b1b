# ==============================================================================
# Scene:      MoreDimensionsNote
# Source:     videos/_2025/grover/qc_supplements.py (lines 410-416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreDimensionsNote.py MoreDimensionsNote -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreDimensionsNote(InteractiveScene):
    def construct(self):
        # Test
        words = TexText(R"(Except $2^k$ dimensions instead of 3)")
        words.set_color(GREY_B)
        self.play(FadeIn(words, lag_ratio=1))
        self.wait()
