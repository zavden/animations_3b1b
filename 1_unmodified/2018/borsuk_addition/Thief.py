# ==============================================================================
# Scene:      Thief
# Source:     videos/_2018/borsuk_addition.py (lines 385-388)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl Thief.py Thief -w -m --fps 15
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

class Thief(Scene):
    def construct(self):
        self.play(Write(OldTexText("Thief")))
        self.wait()
