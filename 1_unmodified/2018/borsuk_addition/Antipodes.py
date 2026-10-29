# ==============================================================================
# Scene:      Antipodes
# Source:     videos/_2018/borsuk_addition.py (lines 313-319)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl Antipodes.py Antipodes -w -m --fps 15
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

class Antipodes(Scene):
    def construct(self):
        word = OldTexText("``Antipodes''")
        word.set_width(FRAME_WIDTH - 1)
        word.set_color(MAROON_B)
        self.play(Write(word))
        self.wait()
