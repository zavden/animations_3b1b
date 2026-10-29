# ==============================================================================
# Scene:      FirstInASequence
# Source:     videos/_2022/borwein/supplements.py (lines 198-204)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FirstInASequence.py FirstInASequence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FirstInASequence(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=2).flip()
        morty.to_corner(DR)
        self.play(morty.says("First in a\nsequence"))
        self.play(Blink(morty))
        self.wait(2)
