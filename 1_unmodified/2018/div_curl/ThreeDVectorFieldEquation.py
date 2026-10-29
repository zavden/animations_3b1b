# ==============================================================================
# Scene:      ThreeDVectorFieldEquation
# Source:     videos/_2018/div_curl.py (lines 1353-1361)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDVectorFieldEquation.py ThreeDVectorFieldEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDVectorFieldEquation(Scene):
    def construct(self):
        vector = Matrix([
            "yz",
            "xz",
            "xy",
        ])
        vector.set_height(FRAME_HEIGHT - 1)
        self.add(vector)
