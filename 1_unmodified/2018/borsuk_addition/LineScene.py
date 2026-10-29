# ==============================================================================
# Scene:      LineScene
# Source:     videos/_2018/borsuk_addition.py (lines 1070-1072)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl LineScene.py LineScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class LineScene(Scene):
    def construct(self):
        self.add(DashedLine(5 * LEFT, 5 * RIGHT, color=WHITE))
