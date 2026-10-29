# ==============================================================================
# Scene:      ShowQ
# Source:     videos/_2018/dandelin.py (lines 1144-1150)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowQ.py ShowQ -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowQ(Scene):
    def construct(self):
        mob = OldTex("Q")
        mob.scale(2)
        mob.add_to_back(mob.copy().set_stroke(BLACK, 5))
        self.play(FadeInFromDown(mob))
        self.wait()
