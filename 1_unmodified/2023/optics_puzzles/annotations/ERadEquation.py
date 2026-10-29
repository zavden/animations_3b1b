# ==============================================================================
# Scene:      ERadEquation
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 612-624)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ERadEquation.py ERadEquation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ERadEquation(InteractiveScene):
    def construct(self):
        equation = Tex(R"""
            \vec{E}_{\text{rad}}(\vec{r}, t) = 
            {-q \over 4\pi \epsilon_0 c^2}
            {1 \over ||\vec{r}||}
            \vec{a}_\perp(t - ||\vec{r}|| / c)
        """, font_size=36)
        lhs = equation[R"\vec{E}_{\text{rad}}(\vec{r}, t)"]
        lhs.set_color(BLUE)
        equation[R"\vec{a}_\perp("].set_color(PINK)
        equation[R")"][1].set_color(PINK)
        self.add(equation)
