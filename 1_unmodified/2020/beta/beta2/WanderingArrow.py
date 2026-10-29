# ==============================================================================
# Scene:      WanderingArrow
# Source:     videos/_2020/beta/beta2.py (lines 598-606)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WanderingArrow.py WanderingArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WanderingArrow(Scene):
    def construct(self):
        arrow = Vector(0.8 * DOWN)
        arrow.move_to(4 * LEFT, DOWN)
        for u in [1, -1, 1, -1, 1]:
            self.play(
                arrow.shift, u * 8 * RIGHT,
                run_time=3
            )
