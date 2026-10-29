# ==============================================================================
# Scene:      WhatDoesBlackMean
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2330-2350)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatDoesBlackMean.py WhatDoesBlackMean -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatDoesBlackMean(Scene):
    def construct(self):
        lhs = OldTexText("$z_n$ never gets\\\\near a root")
        rhs = OldTexText("$\\Rightarrow$ ", "Black ", )
        rhs.next_to(lhs, RIGHT)
        words = VGroup(lhs, rhs)
        words.next_to(ORIGIN, UR, MED_LARGE_BUFF)
        words.to_edge(RIGHT)
        words.set_stroke(BLACK, 5, background=True)
        # lhs[0].set_color(BLACK)
        # lhs[0].set_stroke(width=0)

        arrow = Arrow(ORIGIN, words.get_left(), buff=0.1)

        self.play(
            ShowCreation(arrow),
            Write(lhs),
        )
        self.wait()
        self.play(FadeIn(rhs))
        self.wait()
