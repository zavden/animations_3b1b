# ==============================================================================
# Scene:      Roughly2
# Source:     videos/_2022/puzzles/subsets.py (lines 4903-4906)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Roughly2.py Roughly2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Roughly2(InteractiveScene):
    def construct(self):
        self.play(Write(Tex("\\approx 2")))
        self.wait()
