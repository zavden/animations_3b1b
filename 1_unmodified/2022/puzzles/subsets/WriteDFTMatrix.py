# ==============================================================================
# Scene:      WriteDFTMatrix
# Source:     videos/_2022/puzzles/subsets.py (lines 5399-5410)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteDFTMatrix.py WriteDFTMatrix -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteDFTMatrix(InteractiveScene):
    def construct(self):
        matrix = Tex(r"""\frac{1}{\sqrt{N}}\left[\begin{array}{cccccc}
            1 & 1 & 1 & 1 & \cdots & 1 \\
            1 & \zeta & \zeta^{2} & \zeta^{3} & \cdots & \zeta^{N-1} \\
            1 & \zeta^{2} & \zeta^{4} & \zeta^{6} & \cdots & \zeta^{2(N-1)} \\
            1 & \zeta^{3} & \zeta^{6} & \zeta^{9} & \cdots & \zeta^{3(N-1)} \\
            \vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
            1 & \zeta^{N-1} & \zeta^{2(N-1)} & \zeta^{3(N-1)} & \cdots & \zeta^{(N-1)(N-1)}
            \end{array}\right] """
        )
        self.play(Write(matrix, lag_ratio=0.05, run_time=5))
