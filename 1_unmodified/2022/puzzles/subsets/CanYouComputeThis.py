# ==============================================================================
# Scene:      CanYouComputeThis
# Source:     videos/_2022/puzzles/subsets.py (lines 5063-5072)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CanYouComputeThis.py CanYouComputeThis -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CanYouComputeThis(InteractiveScene):
    def construct(self):
        text = Text("Can you compute this?")
        text.move_to(2 * RIGHT)
        arrow = Arrow(text.get_bottom(), 2 * DOWN)

        VGroup(text, arrow).set_color(GREEN_B)

        self.play(Write(text), ShowCreation(arrow))
        self.wait()
