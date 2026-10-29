# ==============================================================================
# Scene:      ShowComputer
# Source:     videos/_2018/cramer.py (lines 248-258)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowComputer.py ShowComputer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowComputer(ThreeDScene):
    def construct(self):
        laptop = Laptop()
        laptop.add_updater(lambda m, dt: m.rotate(0.1 * dt, axis=UP))
        self.play(DrawBorderThenFill(
            laptop,
            lag_ratio=0.1,
            rate_func=smooth
        ))
        self.wait(8)
        self.play(FadeOut(laptop))
