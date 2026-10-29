# ==============================================================================
# Scene:      CanYouDoBetterThanTwo
# Source:     videos/_2024/puzzles/supplements.py (lines 194-203)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CanYouDoBetterThanTwo.py CanYouDoBetterThanTwo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CanYouDoBetterThanTwo(InteractiveScene):
    def construct(self):
        morty = Mortimer().flip()
        morty.to_edge(LEFT)

        self.play(morty.says("Can you do\nbetter than 2?", mode="tease"))
        self.play(Blink(morty))
        self.wait()
        self.play(morty.change("pondering"))
        self.wait()
