# ==============================================================================
# Scene:      ISquaredRule
# Source:     videos/_2018/quat3d.py (lines 1092-1099)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ISquaredRule.py ISquaredRule -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ISquaredRule(Scene):
    def construct(self):
        tex = OldTexText("Use", "$i^2 = -1$")
        tex[1].set_color(RED)
        tex.scale(2)
        self.add(tex)
        self.play(Write(tex))
        self.wait()
