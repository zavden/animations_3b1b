# ==============================================================================
# Scene:      AskWhat
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 811-828)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhat.py AskWhat -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskWhat(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(DOWN)

        # Test
        bubble = randy.get_bubble("Wait, what?")
        bubble.shift(0.5 * RIGHT + 0.25 * DR)
        self.play(
            randy.change("confused", UP),
            Write(bubble),
        )
        self.play(Blink(randy))
        for mode in ["maybe", "erm"]:
            self.play(randy.change(mode, UP))
            self.wait()
            self.play(Blink(randy))
            self.wait()
