# ==============================================================================
# Scene:      MentionLinearSystem
# Source:     videos/_2022/convolutions/supplements.py (lines 375-384)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionLinearSystem.py MentionLinearSystem -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MentionLinearSystem(InteractiveScene):
    def construct(self):
        # Blah
        morty = Mortimer(height=3).flip().to_edge(DOWN)
        self.play(morty.says("And it's\nlinear!", mode="hooray"))
        self.play(Blink(morty))
        self.play(morty.change("tease"))
        for x in range(2):
            self.play(Blink(morty))
            self.wait(2)
