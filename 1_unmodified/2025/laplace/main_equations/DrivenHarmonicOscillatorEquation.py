# ==============================================================================
# Scene:      DrivenHarmonicOscillatorEquation
# Source:     videos/_2025/laplace/main_equations.py (lines 7-19)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DrivenHarmonicOscillatorEquation.py DrivenHarmonicOscillatorEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DrivenHarmonicOscillatorEquation(InteractiveScene):
    def construct(self):
        colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        equation = Tex(
            R"m x''(t) + \mu x'(t) + k x(t) = F_0 \cos(\omega t)",
            t2c={
                "x(t)": colors[0],
                "x'(t)": colors[1],
                "x''(t)": colors[2],
                R"\omega": PINK,
            }
        )
        self.add(equation)
