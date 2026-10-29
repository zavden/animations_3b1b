# ==============================================================================
# Scene:      Ay
# Source:     videos/_2017/waves.py (lines 1896-1900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Ay.py Ay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class Ay(Scene):
    def construct(self):
        sym = OldTex("A_y").set_color(GREEN)
        sym.scale(5)
        self.add(sym)
