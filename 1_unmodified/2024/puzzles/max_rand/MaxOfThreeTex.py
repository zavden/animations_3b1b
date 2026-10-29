# ==============================================================================
# Scene:      MaxOfThreeTex
# Source:     videos/_2024/puzzles/max_rand.py (lines 560-566)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MaxOfThreeTex.py MaxOfThreeTex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MaxOfThreeTex(InteractiveScene):
    def construct(self):
        # Test
        expr = TexText(R"max(rand(), rand(), rand()) $\leftrightarrow$ rand()$^{1 / 3}$")
        expr["rand()"].set_submobject_colors_by_gradient(BLUE, YELLOW, RED, BLUE)
        self.play(Write(expr))
        self.wait()
