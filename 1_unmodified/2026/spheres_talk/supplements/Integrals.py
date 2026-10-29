# ==============================================================================
# Scene:      Integrals
# Source:     videos/_2026/spheres_talk/supplements.py (lines 511-523)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Integrals.py Integrals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Integrals(InteractiveScene):
    def construct(self):
        kw = dict(t2c={"r": BLUE, "R": TEAL})
        inv_power_rules = VGroup(
            Tex(R"\int_0^R 1 \, dr = R", **kw),
            Tex(R"\int_0^R r \, dr = \frac{1}{2} R^2", **kw),
            Tex(R"\int_0^R r^2 \, dr = \frac{1}{3} R^3", **kw),
            Tex(R"\int_0^R r^3 \, dr = \frac{1}{4} R^4", **kw),
            Tex(R"\vdots", **kw),
        )
        inv_power_rules.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        inv_power_rules[-1].match_x(inv_power_rules[-2]["="])
        self.add(inv_power_rules)
