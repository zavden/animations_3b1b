# ==============================================================================
# Scene:      ExplicitSolution
# Source:     videos/_2021/matrix_exp.py (lines 4744-4759)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExplicitSolution.py ExplicitSolution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExplicitSolution(Scene):
    def construct(self):
        kw = {"tex_to_color_map": {
            "x_0": BLUE_D,
            "y_0": BLUE_B,
            "{t}": GREY_B,

        }}
        solutions = VGroup(
            OldTex("x({t}) = \\cos(t) x_0 - \\sin(t) y_0", **kw),
            OldTex("y({t}) = \\sin(t) x_0 + \\cos(t) y_0", **kw),
        )
        solutions.arrange(DOWN, buff=MED_LARGE_BUFF)
        for solution in solutions:
            self.play(Write(solution))
        self.wait()
