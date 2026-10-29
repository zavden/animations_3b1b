# ==============================================================================
# Scene:      XCoordinateLabelTypoFix
# Source:     videos/_2018/fourier.py (lines 4024-4028)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XCoordinateLabelTypoFix.py XCoordinateLabelTypoFix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class XCoordinateLabelTypoFix(Scene):
    def construct(self):
        words = OldTexText("$x$-coordinate for center of mass")
        words.set_color(RED)
        self.add(words)
