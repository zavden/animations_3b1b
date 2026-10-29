# ==============================================================================
# Scene:      DiameterWordOverlay
# Source:     videos/_2018/basel/basel2.py (lines 3769-3775)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiameterWordOverlay.py DiameterWordOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


DEGREES = TAU/360


class DiameterWordOverlay(Scene):
    def construct(self):
        word = OldTexText("Diameter")
        word.set_width(FRAME_X_RADIUS)
        word.rotate(-45*DEGREES)
        self.play(Write(word))
        self.wait()
