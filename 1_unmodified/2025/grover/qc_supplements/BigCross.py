# ==============================================================================
# Scene:      BigCross
# Source:     videos/_2025/grover/qc_supplements.py (lines 390-397)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BigCross.py BigCross -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BigCross(InteractiveScene):
    def construct(self):
        # Test
        cross = Cross(Rectangle(4, 7))
        max_width = 15
        cross.set_stroke(RED, width=[0, max_width, max_width, max_width, 1])
        self.play(ShowCreation(cross))
        self.wait()
