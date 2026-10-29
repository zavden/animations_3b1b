# ==============================================================================
# Scene:      FourierName
# Source:     videos/_2019/diffyq/part4/staging.py (lines 6-10)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourierName.py FourierName -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FourierName(Scene):
    def construct(self):
        name = OldTexText("Joseph Fourier")
        name.scale(1.5)
        self.add(name)
