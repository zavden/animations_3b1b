# ==============================================================================
# Scene:      Derivatives
# Source:     videos/_2026/spheres_talk/supplements.py (lines 496-508)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Derivatives.py Derivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Derivatives(InteractiveScene):
    def construct(self):
        kw = dict(t2c={"r": BLUE})
        power_rules = VGroup(
            Tex(R"\frac{d}{dr} r = 1", **kw),
            Tex(R"\frac{d}{dr} r^2 = 2r", **kw),
            Tex(R"\frac{d}{dr} r^3 = 3r^2", **kw),
            Tex(R"\frac{d}{dr} r^4 = 4r^3", **kw),
            Tex(R"\vdots", **kw),
        )
        power_rules.arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        power_rules[-1].match_x(power_rules[-2]["="])
        self.add(power_rules)
