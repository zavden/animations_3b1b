# ==============================================================================
# Scene:      RotMatrixStill
# Source:     videos/_2021/matrix_exp.py (lines 3790-3795)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotMatrixStill.py RotMatrixStill -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotMatrixStill(Scene):
    def construct(self):
        mat = IntegerMatrix([[0, -1], [1, 0]])
        br = BackgroundRectangle(mat, buff=SMALL_BUFF)
        br.set_fill(BLACK, 1)
        self.add(br, mat)
