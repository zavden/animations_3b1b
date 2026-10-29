# ==============================================================================
# Scene:      AskAboutProvingCollision
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 278-286)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutProvingCollision.py AskAboutProvingCollision -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutProvingCollision(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_edge(DOWN)
        self.play(randy.thinks("Why must there\nbe a collision?"))
        self.play(Blink(randy))
        self.play(randy.change("confused"))
        self.wait()
