# ==============================================================================
# Scene:      HLine
# Source:     videos/_2025/grover/qc_supplements.py (lines 727-732)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HLine.py HLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HLine(InteractiveScene):
    def construct(self):
        line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        line.set_stroke(GREY_B, 2)
        self.play(ShowCreation(line))
        self.wait()
