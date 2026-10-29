# ==============================================================================
# Scene:      ShowFlash
# Source:     videos/_2018/borsuk_addition.py (lines 1075-1081)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl ShowFlash.py ShowFlash -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class ShowFlash(Scene):
    def construct(self):
        dot = Dot(ORIGIN, color=YELLOW)
        dot.set_stroke(width=0)
        dot.set_fill(opacity=0)
        self.play(Flash(dot, flash_radius=0.8, line_length=0.6, run_time=2))
        self.wait()
