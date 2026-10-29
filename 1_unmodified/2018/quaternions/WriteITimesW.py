# ==============================================================================
# Scene:      WriteITimesW
# Source:     videos/_2018/quaternions.py (lines 2953-2959)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteITimesW.py WriteITimesW -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteITimesW(Scene):
    def construct(self):
        mob = OldTex("i", "\\cdot", "w")
        mob[0].set_color(GREEN)
        mob.scale(3)
        self.play(Write(mob))
        self.wait()
