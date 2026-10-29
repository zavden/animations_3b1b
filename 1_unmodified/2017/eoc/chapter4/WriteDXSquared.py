# ==============================================================================
# Scene:      WriteDXSquared
# Source:     videos/_2017/eoc/chapter4.py (lines 1360-1365)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteDXSquared.py WriteDXSquared -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteDXSquared(Scene):
    def construct(self):
        term = OldTex("(...)(dx)^2")
        term.set_color(RED)
        self.play(Write(term))
        self.wait()
