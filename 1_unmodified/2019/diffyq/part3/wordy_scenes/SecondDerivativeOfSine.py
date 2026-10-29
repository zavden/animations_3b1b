# ==============================================================================
# Scene:      SecondDerivativeOfSine
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 267-278)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SecondDerivativeOfSine.py SecondDerivativeOfSine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SecondDerivativeOfSine(Scene):
    def construct(self):
        equation = OldTex(
            "{d^2 \\over d{x}^2}",
            "\\cos\\left({x}\\right) =",
            "-\\cos\\left({x}\\right)",
            tex_to_color_map={
                "{x}": GREEN,
            }
        )

        self.add(equation)
