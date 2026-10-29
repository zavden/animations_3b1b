# ==============================================================================
# Scene:      QuickRecap
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 108-115)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl QuickRecap.py QuickRecap -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class QuickRecap(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer().flip()
        morty.to_edge(DOWN, buff=1.0).shift(LEFT)
        self.play(morty.says(Text("Quick Recap", font_size=72), bubble_direction=LEFT))
        self.play(Blink(morty))
        self.wait(2)
