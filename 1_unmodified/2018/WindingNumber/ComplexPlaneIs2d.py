# ==============================================================================
# Scene:      ComplexPlaneIs2d
# Source:     videos/_2018/WindingNumber.py (lines 1664-1669)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexPlaneIs2d.py ComplexPlaneIs2d -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7


class ComplexPlaneIs2d(Scene):
    def construct(self):
        com_plane = ComplexPlane()
        self.add(com_plane)
        # TODO: Add labels to axes, specific complex points
        self.wait()
