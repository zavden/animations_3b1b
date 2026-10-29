# ==============================================================================
# Scene:      BigCross
# Source:     videos/_2025/laplace/prequel_equations.py (lines 1414-1419)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigCross.py BigCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BigCross(InteractiveScene):
    def construct(self):
        cross = Cross(Rectangle(4, 1.5))
        cross.set_stroke(RED, width=(0, 8, 8, 8, 0))
        self.play(ShowCreation(cross))
        self.wait()
