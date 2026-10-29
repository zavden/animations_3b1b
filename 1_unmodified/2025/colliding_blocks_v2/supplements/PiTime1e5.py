# ==============================================================================
# Scene:      PiTime1e5
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 554-559)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiTime1e5.py PiTime1e5 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PiTime1e5(InteractiveScene):
    def construct(self):
        # Test
        value = Integer(PI * 1e5, font_size=60)
        self.play(Write(value, lag_ratio=0.2))
        self.wait()
