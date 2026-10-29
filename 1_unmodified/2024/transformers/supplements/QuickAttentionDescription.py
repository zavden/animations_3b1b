# ==============================================================================
# Scene:      QuickAttentionDescription
# Source:     videos/_2024/transformers/supplements.py (lines 1521-1530)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickAttentionDescription.py QuickAttentionDescription -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class QuickAttentionDescription(InteractiveScene):
    def construct(self):
        # To be added standing on an Attention block
        morty = Mortimer(height=2)
        morty.move_to(DOWN + LEFT)
        morty.flip()
        self.play(morty.says("Incorporate context", look_at=4 * DOWN))
        for x in range(2):
            self.play(Blink(morty))
            self.wait(2)
