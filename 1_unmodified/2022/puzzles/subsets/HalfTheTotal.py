# ==============================================================================
# Scene:      HalfTheTotal
# Source:     videos/_2022/puzzles/subsets.py (lines 4820-4831)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HalfTheTotal.py HalfTheTotal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HalfTheTotal(InteractiveScene):
    def construct(self):
        tex = Tex(
            "\\frac{1}{2}\\Big( 2^{2{,}000} + {0} \\Big)",
            tex_to_color_map={
                "2^{2{,}000}": TEAL,
                "{0}": TEAL,
            },
            font_size=60
        )
        self.play(Write(tex))
        self.wait()
