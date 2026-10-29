# ==============================================================================
# Scene:      NotFoundScene
# Source:     videos/_2018/WindingNumber.py (lines 2698-2701)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotFoundScene.py NotFoundScene -w -m --fps 15
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


class NotFoundScene(Scene):
    def construct(self):
        self.add(OldTexText("SCENE NOT FOUND!"))
        self.wait()
