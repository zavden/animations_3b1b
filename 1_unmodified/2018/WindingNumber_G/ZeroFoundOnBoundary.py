# ==============================================================================
# Scene:      ZeroFoundOnBoundary
# Source:     videos/_2018/WindingNumber_G.py (lines 2871-2886)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl ZeroFoundOnBoundary.py ZeroFoundOnBoundary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class ZeroFoundOnBoundary(Scene):
    def construct(self):
        arrow = Vector(DOWN+LEFT, color = WHITE)
        words = OldTexText("Found zero on boundary!")
        words.next_to(arrow.get_start(), UP)
        words.shift(1.5*RIGHT)

        point = VectorizedPoint()
        point.next_to(arrow, DOWN+LEFT)

        self.play(Flash(point))
        self.play(
            GrowArrow(arrow),
            Write(words),
        )
        self.wait()
