# ==============================================================================
# Scene:      NinePercentOfNinety
# Source:     videos/_2020/med_test.py (lines 2426-2430)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NinePercentOfNinety.py NinePercentOfNinety -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NinePercentOfNinety(Scene):
    def construct(self):
        mob = OldTex("(0.09)(90) = 8.1", tex_to_color_map={"8.1": GREEN})
        mob.scale(2)
        self.add(mob)
