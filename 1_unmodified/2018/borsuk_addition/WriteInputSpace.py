# ==============================================================================
# Scene:      WriteInputSpace
# Source:     videos/_2018/borsuk_addition.py (lines 1058-1061)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl WriteInputSpace.py WriteInputSpace -w -m --fps 15
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

class WriteInputSpace(Scene):
    def construct(self):
        self.play(Write(OldTexText("Input space")))
        self.wait()
