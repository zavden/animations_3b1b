# ==============================================================================
# Scene:      MeansMatch
# Source:     videos/_2021/quick_eigen.py (lines 1016-1041)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MeansMatch.py MeansMatch -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

COL_COLORS = [MAROON_B, MAROON_C]


EIGEN_COLORS = [TEAL_A, TEAL_D]


class MeansMatch(Scene):
    def construct(self):
        t2c = {
            "{a}": COL_COLORS[0],
            "{d}": COL_COLORS[1],
            "\\lambda_1": EIGEN_COLORS[0],
            "\\lambda_2": EIGEN_COLORS[1],
            "=": WHITE,
        }
        equation = OldTex(
            "{{a} + {d} \\over 2} = {\\lambda_1 + \\lambda_2 \\over 2}",
            tex_to_color_map=t2c
        )
        mean_eq = OldTex(
            "\\text{mean}({a}, {d}) = \\text{mean}(\\lambda_1, \\lambda_2)",
            tex_to_color_map=t2c
        )

        mean_eq.next_to(equation, DOWN, LARGE_BUFF)

        self.add(equation)

        self.play(TransformMatchingShapes(equation[5:].copy(), mean_eq[6:]))
        self.wait()
        self.play(TransformMatchingShapes(equation[:5].copy(), mean_eq[:6]))
        self.wait()
