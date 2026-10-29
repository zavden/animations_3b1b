# ==============================================================================
# Scene:      IndexOfRefraction
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1031-1051)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IndexOfRefraction.py IndexOfRefraction -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IndexOfRefraction(InteractiveScene):
    def construct(self):
        # Test
        equation = Tex(R"{\text{Speed in a vacuum} \over \text{Speed in water}} \approx 1.33")
        equation.shift(UP)
        rhs = equation[R"\approx 1.33"]
        equation.scale(0.75)
        rhs.scale(1 / 0.75, about_edge=LEFT)
        arrow = Vector(DOWN)
        arrow.next_to(rhs, DOWN, SMALL_BUFF)
        words = TexText("``Index of refraction''")
        words.next_to(arrow, DOWN, SMALL_BUFF)
        words.set_color(BLUE)

        self.play(FadeIn(equation, 0.5 * UP))
        self.wait()
        self.play(
            GrowArrow(arrow),
            Write(words)
        )
        self.wait()
