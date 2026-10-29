# ==============================================================================
# Scene:      ReactToModel
# Source:     videos/_2026/cross_entropy/supplements.py (lines 891-907)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReactToModel.py ReactToModel -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ReactToModel(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph().flip()

        self.play(
            VFadeIn(randy),
            randy.change("sassy")
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("hesitant", 3 * UP))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("confused", 3 * UL))
        self.play(Blink(randy))
        self.wait()
