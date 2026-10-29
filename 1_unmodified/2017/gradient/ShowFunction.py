# ==============================================================================
# Scene:      ShowFunction
# Source:     videos/_2017/gradient.py (lines 100-111)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFunction.py ShowFunction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowFunction(Scene):
    def construct(self):
        func = OldTex(
            "f(x, y) = e^{-x^2 + \\cos(2y)}",
            tex_to_color_map={
                "x": BLUE,
                "y": RED,
            }
        )
        func.scale(1.5)
        self.play(FadeInFromDown(func))
        self.wait()
