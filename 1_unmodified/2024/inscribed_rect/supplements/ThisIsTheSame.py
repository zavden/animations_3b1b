# ==============================================================================
# Scene:      ThisIsTheSame
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 192-199)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThisIsTheSame.py ThisIsTheSame -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThisIsTheSame(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer().flip()
        morty.to_edge(DOWN)
        self.play(morty.says("This is the\nsame question"))
        self.play(Blink(morty))
        self.wait()
