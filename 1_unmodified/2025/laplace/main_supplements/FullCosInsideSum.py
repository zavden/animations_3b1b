# ==============================================================================
# Scene:      FullCosInsideSum
# Source:     videos/_2025/laplace/main_supplements.py (lines 254-257)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FullCosInsideSum.py FullCosInsideSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FullCosInsideSum(InteractiveScene):
    def construct(self):
        tex = Tex(R"\frac{1}{2} \left( e^{(i - {s}){t}} + e^{(\minus i - {s}){t}} \right)", t2c={"{t}": BLUE, "{s}": YELLOW})
        self.add(tex)
