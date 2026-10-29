# ==============================================================================
# Scene:      EqualsZeta3
# Source:     videos/_2022/puzzles/subsets.py (lines 4891-4900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EqualsZeta3.py EqualsZeta3 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EqualsZeta3(InteractiveScene):
    def construct(self):
        arrow = Vector(0.5 * DOWN)
        tex = Tex("\\zeta^3", tex_to_color_map={"\\zeta": YELLOW})
        tex.next_to(arrow, DOWN)
        self.play(
            GrowArrow(arrow),
            FadeIn(tex, DOWN)
        )
        self.wait()
