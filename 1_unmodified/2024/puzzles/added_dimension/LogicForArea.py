# ==============================================================================
# Scene:      LogicForArea
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2734-2762)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LogicForArea.py LogicForArea -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LogicForArea(InteractiveScene):
    def construct(self):
        # Test
        det_tex = Tex(R"""
            = \frac{1}{2}\det\left[\begin{array}{ccc}
            x_1 & x_2 & x_3 \\
            y_1 & y_2 & y_3 \\
            1 & 1 & 1
            \end{array}\right]
        """)
        equations = VGroup(
            TexText(R"Volume(Tetra.) = $\frac{1}{3}$ Area(Tri.) $\times 1$"),
            TexText(R"Volume(Tetra.) = $\frac{1}{6}$ Volume(Para.)"),
            Tex(R"\Downarrow"),
            TexText(R"Area(Tri.) = $\frac{1}{2}$ Volume(Para.)"),
        )
        for eq in [det_tex, *equations]:
            eq["Tetra."].set_color(YELLOW)
            eq["Tri."].set_color(YELLOW)
            eq["Para."].set_color(YELLOW)

        equations.arrange(DOWN, buff=LARGE_BUFF)
        equations.to_corner(UL)
        equations[2].scale(2)
        det_tex.next_to(equations[-1]["="], DOWN, LARGE_BUFF, aligned_edge=LEFT)

        self.frame.set_height(10)
        self.add(det_tex)
        self.add(equations)
