# ==============================================================================
# Scene:      WriteNotEquals
# Source:     videos/_2018/sphere_area.py (lines 2179-2185)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteNotEquals.py WriteNotEquals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteNotEquals(Scene):
    def construct(self):
        symbol = OldTex("\\ne")
        symbol.scale(2)
        symbol.set_background_stroke(width=0)
        self.play(Write(symbol))
        self.wait()
