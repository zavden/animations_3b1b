# ==============================================================================
# Scene:      GrowingWhiteDot
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 1320-1329)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GrowingWhiteDot.py GrowingWhiteDot -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GrowingWhiteDot(InteractiveScene):
    def construct(self):
        # Test
        dot = GlowDot(radius=1)
        dot.set_color(WHITE)
        self.add(dot)
        self.play(
            dot.animate.set_radius(FRAME_WIDTH).set_glow_factor(0.5),
            run_time=35
        )
