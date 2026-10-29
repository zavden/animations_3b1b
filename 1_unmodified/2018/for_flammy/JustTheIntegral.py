# ==============================================================================
# Scene:      JustTheIntegral
# Source:     videos/_2018/for_flammy.py (lines 19-23)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JustTheIntegral.py JustTheIntegral -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JustTheIntegral(Scene):
    def construct(self):
        tex = OldTex("\\int_0^{\\pi / 2} \\cos(\\theta)d\\theta")
        tex.scale(2)
        self.add(tex)
