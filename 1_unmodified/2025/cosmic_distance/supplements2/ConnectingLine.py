# ==============================================================================
# Scene:      ConnectingLine
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 592-597)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConnectingLine.py ConnectingLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConnectingLine(InteractiveScene):
    def construct(self):
        line = Line(2 * UP, 2 * DOWN)
        line.set_stroke(GREEN, 8)
        self.play(ShowCreation(line))
        self.play(line.animate.set_stroke(width=0), run_time=2)
