# ==============================================================================
# Scene:      SimpleArrow
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 450-454)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleArrow.py SimpleArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleArrow(InteractiveScene):
    def construct(self):
        arrow = Vector(0.5 * DL)
        self.play(GrowArrow(arrow))
        self.wait()
