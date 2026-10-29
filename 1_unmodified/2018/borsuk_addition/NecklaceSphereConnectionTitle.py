# ==============================================================================
# Scene:      NecklaceSphereConnectionTitle
# Source:     videos/_2018/borsuk_addition.py (lines 1169-1173)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl NecklaceSphereConnectionTitle.py NecklaceSphereConnectionTitle -w -m --fps 15
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

class NecklaceSphereConnectionTitle(Scene):
    def construct(self):
        text = OldTexText("Necklace Sphere Association")
        text.set_width(FRAME_WIDTH - 1)
        self.add(text)
