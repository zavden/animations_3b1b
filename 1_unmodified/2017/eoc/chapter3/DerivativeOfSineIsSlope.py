# ==============================================================================
# Scene:      DerivativeOfSineIsSlope
# Source:     videos/_2017/eoc/chapter3.py (lines 2141-2153)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DerivativeOfSineIsSlope.py DerivativeOfSineIsSlope -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DerivativeOfSineIsSlope(Scene):
    def construct(self):
        tex = OldTex(
            "\\frac{d(\\sin(\\theta))}{d\\theta} = ",
            "\\text{Slope of this graph}"
        )
        tex.set_width(FRAME_WIDTH-1)
        tex.to_edge(DOWN)
        VGroup(*tex[0][2:8]).set_color(BLUE)
        VGroup(*tex[1][-9:]).set_color(BLUE)

        self.play(Write(tex, run_time = 2))
        self.wait()
