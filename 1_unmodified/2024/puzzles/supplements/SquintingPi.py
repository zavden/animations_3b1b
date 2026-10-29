# ==============================================================================
# Scene:      SquintingPi
# Source:     videos/_2024/puzzles/supplements.py (lines 136-148)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquintingPi.py SquintingPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquintingPi(InteractiveScene):
    def construct(self):
        randy = Randolph(mode='pondering')
        randy.to_corner(LEFT)
        randy.look_at(ORIGIN)
        self.add(randy)
        self.play(Blink(randy))
        self.play(randy.change('concentrating'))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change('tease'))
        self.play(Blink(randy))
        self.wait()
