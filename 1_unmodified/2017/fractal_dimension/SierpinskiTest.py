# ==============================================================================
# Scene:      SierpinskiTest
# Source:     videos/_2017/fractal_dimension.py (lines 44-55)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SierpinskiTest.py SierpinskiTest -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SierpinskiTest(Scene):
    def construct(self):
        sierp = Sierpinski(
            order = 5,
        )

        self.play(FadeIn(
            sierp,
            run_time = 5,
            lag_ratio = 0.5,
        ))
        self.wait()
