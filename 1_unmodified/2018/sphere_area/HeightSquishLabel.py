# ==============================================================================
# Scene:      HeightSquishLabel
# Source:     videos/_2018/sphere_area.py (lines 1372-1379)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HeightSquishLabel.py HeightSquishLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HeightSquishLabel(Scene):
    def construct(self):
        text = OldTex(
            "\\text{Height squish factor} =",
            "\\frac{R}{d}"
        )
        self.play(Write(text))
        self.wait()
