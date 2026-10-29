# ==============================================================================
# Scene:      XComponentArrows
# Source:     videos/_2019/diffyq/part1/staging.py (lines 2063-2076)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl XComponentArrows.py XComponentArrows -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo vector field as a group of arrows, with delta_x/delta_y and get_vector, instead of the current GL API.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import CairoVectorField as VectorField

class XComponentArrows(Scene):
    def construct(self):
        field = VectorField(
            lambda p: np.array([p[1], 0, 0])
        )
        field.set_opacity(0.75)
        for u in (1, -1):
            field.sort(lambda p: u * p[0])
            self.play(LaggedStartMap(
                GrowArrow, field,
                lag_ratio=0.1,
                run_time=1
            ))
            self.play(FadeOut(field))
