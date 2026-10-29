# ==============================================================================
# Scene:      PropHeadsWithinHundredth
# Source:     videos/_2018/eop/chapter1/million_flips.py (lines 110-118)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PropHeadsWithinHundredth.py PropHeadsWithinHundredth -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *

class PropHeadsWithinHundredth(Scene):
    def construct(self):
        prob = OldTex(
            "P(490{,}000 \\le", "\\# \\text{H}", "\\le 510{,}000)",
            "\\approx", "0.99999999\\dots",
        )
        prob[1].set_color(RED)
        prob[-1].set_color(YELLOW)
        self.add(prob)
