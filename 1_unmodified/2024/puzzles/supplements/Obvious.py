# ==============================================================================
# Scene:      Obvious
# Source:     videos/_2024/puzzles/supplements.py (lines 933-939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Obvious.py Obvious -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Obvious(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        self.play(randy.says("Isn't that\nobvious?", mode="confused", bubble_direction=LEFT))
        self.play(randy.animate.look_at(3 * UP))
        self.wait(5)
