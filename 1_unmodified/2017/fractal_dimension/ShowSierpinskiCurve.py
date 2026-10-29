# ==============================================================================
# Scene:      ShowSierpinskiCurve
# Source:     videos/_2017/fractal_dimension.py (lines 1156-1173)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowSierpinskiCurve.py ShowSierpinskiCurve -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSierpinskiCurve(Scene):
    CONFIG = {
        "max_order" : 8,
    }
    def construct(self):
        curve = self.get_curve(2)
        self.play(ShowCreation(curve, run_time = 2))
        for order in range(3, self.max_order + 1):
            self.play(Transform(
                curve, self.get_curve(order),
                run_time = 2
            ))
            self.wait()

    def get_curve(self, order):
        curve = SierpinskiCurve(order = order, monochromatic = True)
        curve.set_color(RED)
        return curve
