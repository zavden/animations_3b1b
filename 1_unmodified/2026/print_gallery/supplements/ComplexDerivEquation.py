# ==============================================================================
# Scene:      ComplexDerivEquation
# Source:     videos/_2026/print_gallery/supplements.py (lines 388-400)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexDerivEquation.py ComplexDerivEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexDerivEquation(InteractiveScene):
    def construct(self):
        equation = Tex(
            R"\Delta f(z) \approx \Delta z \cdot c",
            t2c={
                R"\Delta f(z)": PINK,
                R"\Delta z": YELLOW,
                "c": GREEN
            },
            font_size=72
        )
        self.play(Write(equation))
        self.wait()
