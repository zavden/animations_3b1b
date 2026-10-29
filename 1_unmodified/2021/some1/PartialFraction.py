# ==============================================================================
# Scene:      PartialFraction
# Source:     videos/_2021/some1.py (lines 166-172)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PartialFraction.py PartialFraction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PartialFraction(Scene):
    def construct(self):
        frac = OldTex(
            r"\frac{x+9}{(x-3)(x+5)} = \frac{?}{x - 3} + \frac{?}{x + 5}"
        )
        frac.set_width(10)
        self.add(frac)
