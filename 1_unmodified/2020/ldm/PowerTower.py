# ==============================================================================
# Scene:      PowerTower
# Source:     videos/_2020/ldm.py (lines 989-998)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PowerTower.py PowerTower -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PowerTower(Scene):
    def construct(self):
        mob = OldTex("4 = x^{x^{{x^{x^{x^{\cdot^{\cdot^{\cdot}}}}}}}}")
        mob[0][-1].shift(0.1 * DL)
        mob[0][-2].shift(0.05 * DL)

        mob.set_height(4)
        mob.set_stroke(BLACK, 5, background=True)

        self.add(mob)
