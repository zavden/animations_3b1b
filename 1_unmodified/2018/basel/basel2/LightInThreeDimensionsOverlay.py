# ==============================================================================
# Scene:      LightInThreeDimensionsOverlay
# Source:     videos/_2018/basel/basel2.py (lines 1580-1587)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightInThreeDimensionsOverlay.py LightInThreeDimensionsOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class LightInThreeDimensionsOverlay(Scene):
    def construct(self):
        words = OldTexText("""
            ``Solid angle'' \\\\
            (measured in ``steradians'')
        """)
        self.play(Write(words))
        self.wait()
