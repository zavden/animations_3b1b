# ==============================================================================
# Scene:      AutoregressionArrow2
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 435-448)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AutoregressionArrow2.py AutoregressionArrow2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AutoregressionArrow2(InteractiveScene):
    dims = (1, 1)

    def construct(self):
        # Test
        curve = Rectangle(*self.dims).round_corners().rotate(-90 * DEG)
        line = curve.copy().pointwise_become_partial(curve, 0.05, 0.675)
        line.set_stroke(TEAL, 5)
        tip = ArrowTip(-90 * DEG)
        tip.move_to(line.get_end(), UP).shift(1e-2 * UP)
        tip.match_color(line)
        line.add(tip)

        self.add(line)
