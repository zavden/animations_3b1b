# ==============================================================================
# Scene:      QuickMLPDescription
# Source:     videos/_2024/transformers/supplements.py (lines 1533-1541)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickMLPDescription.py QuickMLPDescription -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class QuickMLPDescription(InteractiveScene):
    def construct(self):
        # To be added standing on an MLP block
        morty = Mortimer(height=2, color=GREY_C)
        morty.move_to(DOWN + RIGHT)
        self.play(morty.says("More\ncomputation", mode="maybe", look_at=4 * DOWN))
        for x in range(2):
            self.play(Blink(morty))
            self.wait(2)
