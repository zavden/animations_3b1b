# ==============================================================================
# Scene:      UhWhy
# Source:     videos/_2022/convolutions/supplements.py (lines 463-478)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UhWhy.py UhWhy -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UhWhy(InteractiveScene):
    def construct(self):
        randy = Randolph(height=3)
        randy.to_corner()
        point = LEFT_SIDE + 2 * UR

        self.play(randy.says("Uh...friendlier?", mode="sassy"))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("erm", look_at=point))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.debubble(mode="pondering", look_at=point))
        for x in range(3):
            self.play(Blink(randy))
            self.wait(2)
