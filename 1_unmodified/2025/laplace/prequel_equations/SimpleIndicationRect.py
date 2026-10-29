# ==============================================================================
# Scene:      SimpleIndicationRect
# Source:     videos/_2025/laplace/prequel_equations.py (lines 581-585)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleIndicationRect.py SimpleIndicationRect -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleIndicationRect(InteractiveScene):
    def construct(self):
        rect = Rectangle(3, 2)
        # Test
        self.play(FlashAround(rect, time_width=2.0, run_time=2, color=WHITE))
