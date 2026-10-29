# ==============================================================================
# Scene:      Thanks
# Source:     videos/_2023/gauss_int/supplements.py (lines 1340-1354)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thanks.py Thanks -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Thanks(InteractiveScene):
    def construct(self):
        message = Text("Thank you \n patrons!", font_size=72)
        morty = Mortimer().flip()
        morty.next_to(ORIGIN, LEFT)
        message.next_to(morty, RIGHT)

        self.play(
            morty.change("gracious"),
            Write(message)
        )
        self.play(Blink(morty))
        self.wait()
        self.play(Blink(morty))
        self.wait(2)
