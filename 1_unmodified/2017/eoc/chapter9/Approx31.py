# ==============================================================================
# Scene:      Approx31
# Source:     videos/_2017/eoc/chapter9.py (lines 963-969)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Approx31.py Approx31 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Approx31(Scene):
    def construct(self):
        tex = OldTex("\\approx 31")
        tex.set_width(FRAME_WIDTH - LARGE_BUFF)
        tex.to_edge(LEFT)
        self.play(Write(tex))
        self.wait(3)
