# ==============================================================================
# Scene:      SetSToMinus1
# Source:     videos/_2025/laplace/main_equations.py (lines 1376-1381)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SetSToMinus1.py SetSToMinus1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SetSToMinus1(InteractiveScene):
    def construct(self):
        eq = Tex(R"\frac{1}{\minus 1} = \minus 1")
        eq[R"\minus 1"][0].set_color(YELLOW)
        self.play(Write(eq))
        self.wait()
