# ==============================================================================
# Scene:      RewindArrows
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 190-196)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RewindArrows.py RewindArrows -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RewindArrows(InteractiveScene):
    def construct(self):
        # Test
        arrows = ArrowTip(angle=PI).get_grid(1, 3)
        arrows.scale(2)
        self.play(LaggedStartMap(FadeIn, arrows, lag_ratio=0.1, shift=0.5 * LEFT, run_time=1))
        self.wait()
