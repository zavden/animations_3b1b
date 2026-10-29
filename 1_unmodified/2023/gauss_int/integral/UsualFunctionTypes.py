# ==============================================================================
# Scene:      UsualFunctionTypes
# Source:     videos/_2023/gauss_int/integral.py (lines 283-308)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UsualFunctionTypes.py UsualFunctionTypes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class UsualFunctionTypes(InteractiveScene):
    def construct(self):
        t2c = {"x": YELLOW}
        functions = VGroup(
            Tex(R"a_n x^n + \cdots a_1 x + a_0", t2c=t2c),
            Tex(R"\sin(x), \cos(x), \arctan(x)", t2c=t2c),
            Tex(R"b^x, \log(x), \cosh(x)", t2c=t2c),
            Tex(R"\vdots")
        )
        functions.arrange(DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)
        functions.set_height(2.5)
        functions.to_edge(RIGHT, buff=0.6)

        box = SurroundingRectangle(functions, buff=MED_LARGE_BUFF)
        box.set_stroke(RED, 2)

        words = Text("Cannot be expressed \n in terms of these:")
        words.next_to(box, UP)
        words.set_fill(RED)

        self.play(
            FadeIn(words, lag_ratio=0.1),
            FadeIn(box),
            LaggedStartMap(FadeIn, functions, shift=DOWN, lag_ratio=0.5, run_time=3),
        )
        self.wait()
