# ==============================================================================
# Scene:      ShowTwoTo32
# Source:     videos/_2017/256.py (lines 181-186)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowTwoTo32.py ShowTwoTo32 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowTwoTo32(Scene):
    def construct(self):
        mob = OldTex("2^{32} = 4{,}294{,}967{,}296")
        mob.scale(1.5)
        self.add(mob)
        self.wait()
