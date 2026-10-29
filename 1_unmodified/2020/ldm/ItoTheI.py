# ==============================================================================
# Scene:      ItoTheI
# Source:     videos/_2020/ldm.py (lines 1001-1007)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ItoTheI.py ItoTheI -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ItoTheI(Scene):
    def construct(self):
        tex = OldTex("i^i")
        # tex = OldTex("\\sqrt{-1}^{\\sqrt{-1}}")
        tex.set_height(3)
        tex.set_stroke(BLACK, 8, background=True)
        self.add(tex)
