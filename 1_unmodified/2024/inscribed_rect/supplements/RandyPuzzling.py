# ==============================================================================
# Scene:      RandyPuzzling
# Source:     videos/_2024/inscribed_rect/supplements.py (lines 424-437)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandyPuzzling.py RandyPuzzling -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RandyPuzzling(InteractiveScene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(LEFT)
        self.play(randy.change("pondering", 2 * RIGHT))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change('confused', 2 * RIGHT))
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.play(randy.change('maybe', 2 * RIGHT))
        self.play(Blink(randy))
        self.wait()
