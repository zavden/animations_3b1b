# ==============================================================================
# Scene:      MortyReferencingTwoThings
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 295-307)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MortyReferencingTwoThings.py MortyReferencingTwoThings -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MortyReferencingTwoThings(InteractiveScene):
    def construct(self):
        morty = Mortimer().flip()
        morty.to_edge(DOWN)
        self.play(morty.change("raise_left_hand", 3 * UL))
        self.play(Blink(morty))
        self.play(morty.change("raise_right_hand", 3 * UR))
        for _ in range(2):
            self.play(Blink(morty))
            self.wait(2)
        self.play(morty.change("tease", 3 * UR))
        self.play(Blink(morty))
        self.wait(2)
