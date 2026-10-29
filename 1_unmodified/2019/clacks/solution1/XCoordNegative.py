# ==============================================================================
# Scene:      XCoordNegative
# Source:     videos/_2019/clacks/solution1.py (lines 1158-1166)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XCoordNegative.py XCoordNegative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class XCoordNegative(Scene):
    def construct(self):
        rect = Rectangle(height=4, width=4)
        rect.set_stroke(width=0)
        rect.set_fill(RED, 0.5)
        rect.save_state()
        rect.stretch(0, 0, about_edge=RIGHT)
        self.play(Restore(rect))
        self.wait()
