# ==============================================================================
# Scene:      ExtraHint
# Source:     videos/_2018/sphere_area.py (lines 3406-3415)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExtraHint.py ExtraHint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExtraHint(Scene):
    def construct(self):
        title = OldTexText("Extra hint")
        title.scale(2.5)
        title.shift(UP)
        equation = OldTex(
            "\\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta)"
        )
        equation.next_to(title, DOWN)
        self.add(title, equation)
