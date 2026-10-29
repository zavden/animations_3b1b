# ==============================================================================
# Scene:      YCoordZero
# Source:     videos/_2019/clacks/solution1.py (lines 1169-1179)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl YCoordZero.py YCoordZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class YCoordZero(Scene):
    def construct(self):
        rect = Rectangle(height=4, width=8)
        rect.set_stroke(width=0)
        rect.set_fill(WHITE, 0.5)
        rect.save_state()
        self.play(
            rect.stretch, 0.01, 1,
            rect.set_fill, {"opacity": 1}
        )
        self.wait()
