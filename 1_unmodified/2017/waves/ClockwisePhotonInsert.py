# ==============================================================================
# Scene:      ClockwisePhotonInsert
# Source:     videos/_2017/waves.py (lines 4184-4193)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ClockwisePhotonInsert.py ClockwisePhotonInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class ClockwisePhotonInsert(Scene):
    def construct(self):
        eq = OldTex(
            "\\left| \\frac{-i}{\\sqrt{2}} \\right|^2"
        )
        eq.set_color(BLUE)
        VGroup(*it.chain(eq[:4], eq[-5:])).set_color(WHITE)
        eq.set_height(FRAME_HEIGHT - 1)
        eq.to_edge(LEFT)
        self.add(eq)
