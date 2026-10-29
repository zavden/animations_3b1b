# ==============================================================================
# Scene:      DivergenceZeroCondition
# Source:     videos/_2018/div_curl.py (lines 1961-1975)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DivergenceZeroCondition.py DivergenceZeroCondition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DivergenceZeroCondition(Scene):
    def construct(self):
        title = OldTexText(
            "For actual (incompressible) fluid flow:"
        )
        title.to_edge(UP)
        equation = OldTex(
            "\\text{div} \\, \\textbf{F} = 0 \\quad \\text{everywhere}"
        )
        equation.next_to(title, DOWN)

        for mob in title, equation:
            mob.add_background_rectangle(buff=MED_SMALL_BUFF / 2)
            self.add_foreground_mobjects(mob)
        self.wait(1)
