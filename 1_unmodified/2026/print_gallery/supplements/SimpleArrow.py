# ==============================================================================
# Scene:      SimpleArrow
# Source:     videos/_2026/print_gallery/supplements.py (lines 179-184)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleArrow.py SimpleArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleArrow(InteractiveScene):
    def construct(self):
        vect = Vector(1.5 * RIGHT, thickness=8)
        vect.set_fill(TEAL)
        self.play(GrowArrow(vect))
        self.wait()
