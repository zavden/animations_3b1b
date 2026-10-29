# ==============================================================================
# Scene:      REq
# Source:     videos/_2020/sir.py (lines 2485-2490)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl REq.py REq -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class REq(Scene):
    def construct(self):
        mob = OldTex("R_0 = ")[0]
        mob[1].set_color(BLACK)
        mob[2].shift(mob[1].get_width() * LEFT * 0.7)
        self.add(mob)
