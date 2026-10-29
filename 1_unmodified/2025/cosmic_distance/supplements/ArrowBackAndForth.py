# ==============================================================================
# Scene:      ArrowBackAndForth
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 940-947)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ArrowBackAndForth.py ArrowBackAndForth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ArrowBackAndForth(InteractiveScene):
    def construct(self):
        # Test
        arrow = Arrow(3 * LEFT, 3 * RIGHT, path_arc=-90 * DEG, thickness=6)
        self.play(Write(arrow))
        self.wait()
        self.play(arrow.animate.flip())
        self.wait()
