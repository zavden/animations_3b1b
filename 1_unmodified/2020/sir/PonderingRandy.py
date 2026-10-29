# ==============================================================================
# Scene:      PonderingRandy
# Source:     videos/_2020/sir.py (lines 2952-2959)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PonderingRandy.py PonderingRandy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PonderingRandy(Scene):
    def construct(self):
        randy = Randolph()
        self.play(FadeIn(randy))
        self.play(randy.change, "pondering")
        for x in range(3):
            self.play(Blink(randy))
            self.wait(2)
