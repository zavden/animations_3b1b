# ==============================================================================
# Scene:      ArrowPair
# Source:     videos/_2020/hamming.py (lines 5479-5491)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowPair.py ArrowPair -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowPair(Scene):
    def construct(self):
        arrows = VGroup(
            Vector(LEFT),
            Vector(LEFT),
        )
        arrows.scale(1.5)
        arrows.arrange(DOWN, buff=2)
        arrows[0].shift(4 * LEFT)
        arrows.set_fill(YELLOW)

        self.play(*map(GrowArrow, arrows))
        self.wait()
