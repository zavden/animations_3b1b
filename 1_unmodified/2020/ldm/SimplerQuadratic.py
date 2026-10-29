# ==============================================================================
# Scene:      SimplerQuadratic
# Source:     videos/_2020/ldm.py (lines 99-104)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplerQuadratic.py SimplerQuadratic -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimplerQuadratic(Scene):
    def construct(self):
        tex = OldTex("m \\pm \\sqrt{m^2 - p}")
        tex.set_stroke(BLACK, 12, background=True)
        tex.scale(1.5)
        self.add(tex)
