# ==============================================================================
# Scene:      FourDDet
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2765-2781)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourDDet.py FourDDet -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class FourDDet(InteractiveScene):
    def construct(self):
        det_tex = Tex(R"""
            \frac{1}{6}\det\left[\begin{array}{cccc}
            x_1 & x_2 & x_3 & x_4 \\
            y_1 & y_2 & y_3 & y_4 \\
            z_1 & z_2 & z_3 & z_4 \\
            1 & 1 & 1 & 1
            \end{array}\right]
        """)
        group = VGroup(
            Text("Volume", font_size=72),
            Tex("=", font_size=72).rotate(90 * DEGREES),
            det_tex
        )
        group.arrange(DOWN, buff=LARGE_BUFF)
        self.add(group)
