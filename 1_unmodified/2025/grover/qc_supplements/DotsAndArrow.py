# ==============================================================================
# Scene:      DotsAndArrow
# Source:     videos/_2025/grover/qc_supplements.py (lines 375-387)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DotsAndArrow.py DotsAndArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DotsAndArrow(InteractiveScene):
    def construct(self):
        # Test
        dots = Tex(R"\cdots", font_size=160)
        dots.space_out_submobjects(0.8)
        arrow = Vector(2.0 * RIGHT, thickness=8)
        arrow.next_to(dots, RIGHT, MED_LARGE_BUFF)
        self.play(LaggedStart(
            FadeIn(dots, lag_ratio=0.5),
            GrowArrow(arrow),
            lag_ratio=0.7
        ))
        self.wait()
