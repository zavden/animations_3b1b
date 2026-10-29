# ==============================================================================
# Scene:      ShowGeometricSum
# Source:     videos/_2017/crypto.py (lines 4733-4751)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowGeometricSum.py ShowGeometricSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowGeometricSum(Scene):
    def construct(self):
        equation = OldTex(
            "210{,}000", "(", 
            "50", "+", "25", "+", "12.5", "+", 
            "6.25", "+\\cdots", ")", "=", "21{,}000{,}000"
        )
        numbers = ["50", "25", "12.5", "6.25"]
        colors = color_gradient([BLUE_D, BLUE_B], 4)
        for tex, color in zip(numbers, colors):
            equation.set_color_by_tex(tex, color)
        equation[-1].set_color(YELLOW)

        self.add(*equation[:2] + equation[-3:-1])
        for i in range(2, 9, 2):
            self.play(FadeIn(VGroup(*equation[i:i+2])))
        self.wait()
        self.play(Write(equation[-1]))
        self.wait(2)
