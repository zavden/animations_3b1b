# ==============================================================================
# Scene:      MaxwellsEquations
# Source:     videos/_2023/gauss_int/supplements.py (lines 876-893)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MaxwellsEquations.py MaxwellsEquations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MaxwellsEquations(InteractiveScene):
    def construct(self):
        kw = dict(
            t2c={R"\mathbf{E}": RED, R"\mathbf{B}": TEAL}
        )
        equations = VGroup(
            Tex(R"\nabla \cdot \mathbf{E}=4 \pi \rho", **kw),
            Tex(R"\nabla \cdot \mathbf{B}=0", **kw),
            Tex(R"\nabla \times \mathbf{E}=-\frac{1}{c} \frac{\partial \mathbf{B}}{\partial t}", **kw),
            Tex(R"\nabla \times \mathbf{B}=\frac{1}{c}\left(4 \pi \mathbf{J}+\frac{\partial \mathbf{E}}{\partial t}\right)", **kw),
        )
        equations.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        equations.set_height(6.5)
        equations.to_edge(LEFT)
        equations.set_backstroke(BLACK, 3)

        self.play(LaggedStartMap(FadeIn, equations, shift=0.5 * DOWN, lag_ratio=0.5))
        self.wait()
