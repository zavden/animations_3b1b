# ==============================================================================
# Scene:      NamePolarizingFilter
# Source:     videos/_2017/waves.py (lines 2194-2199)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NamePolarizingFilter.py NamePolarizingFilter -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class NamePolarizingFilter(Scene):
    def construct(self):
        words = OldTexText("Polarizing filter")
        words.set_width(FRAME_WIDTH - 1)
        self.play(Write(words))
        self.wait()
