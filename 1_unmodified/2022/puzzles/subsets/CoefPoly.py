# ==============================================================================
# Scene:      CoefPoly
# Source:     videos/_2022/puzzles/subsets.py (lines 4942-4948)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CoefPoly.py CoefPoly -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CoefPoly(InteractiveScene):
    def construct(self):
        mid_str = "".join((f"c_{{{n}}} x^{{{n}}} + " for n in range(2, 8)))
        self.add(Tex(
            "f(x) = c_0 + c_1 x + " + mid_str + "\\cdots",
            tex_to_color_map={"x": BLUE}
        ).to_edge(UP).shift(DOWN))
