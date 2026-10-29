# ==============================================================================
# Scene:      KochTest
# Source:     videos/_2017/fractal_dimension.py (lines 33-42)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KochTest.py KochTest -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KochTest(Scene):
    def construct(self):
        koch = KochCurve(order = 5, stroke_width = 2)

        self.play(ShowCreation(koch, run_time = 3))
        self.play(
            koch.scale, 3, koch.get_left(),
            koch.set_stroke, None, 4
        )
        self.wait()
