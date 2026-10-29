# ==============================================================================
# Scene:      LargeInLargeLanguageModel
# Source:     videos/_2024/transformers/chm.py (lines 1239-1254)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LargeInLargeLanguageModel.py LargeInLargeLanguageModel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LargeInLargeLanguageModel(InteractiveScene):
    def construct(self):
        # Test
        text = Text("Large Language Model", font_size=72)
        text.to_edge(UP)
        large = text["Large"][0]
        large.save_state()
        large.set_x(0)

        self.add(large)
        self.play(FlashUnder(large), large.animate.set_color(YELLOW))
        self.play(
            Restore(large, path_arc=-30 * DEGREES),
            Write(text[len(large):], time_span=(0.5, 1.5))
        )
        self.wait()
