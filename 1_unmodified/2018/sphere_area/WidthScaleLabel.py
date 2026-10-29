# ==============================================================================
# Scene:      WidthScaleLabel
# Source:     videos/_2018/sphere_area.py (lines 1362-1369)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WidthScaleLabel.py WidthScaleLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WidthScaleLabel(Scene):
    def construct(self):
        text = OldTex(
            "\\text{Width scale factor} =",
            "\\frac{R}{d}"
        )
        self.play(Write(text))
        self.wait()
