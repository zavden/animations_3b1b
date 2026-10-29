# ==============================================================================
# Scene:      AddingCopiesOfAVariable
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 203-233)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddingCopiesOfAVariable.py AddingCopiesOfAVariable -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AddingCopiesOfAVariable(InteractiveScene):
    def construct(self):
        # Test
        expr = Tex(R"X_1 + X_2 + \cdots + X_N \text{ is approximately Gaussian}")
        expr.set_fill(GREY_A)
        expr_lhs = expr[R"X_1 + X_2 + \cdots + X_N"][0]
        expr.to_edge(UP)
        expr_lhs.save_state()
        expr_lhs.set_x(0)

        self.play(FadeIn(expr_lhs, lag_ratio=0.5, run_time=2))
        self.wait()
        self.play(
            Restore(expr_lhs),
            Write(expr[len(expr_lhs):], run_time=1)
        )
        self.wait(3)

        # Limit
        expr2 = Tex(R"X_1 + X_2 + \cdots + X_N \longrightarrow \text{Gaussian}")
        expr2.match_style(expr)
        expr2.move_to(expr)
        lim = Tex(R"N \to \infty", font_size=24)
        lim.next_to(expr2[R"\longrightarrow"], UP, buff=0.1)
        lim.set_color(YELLOW)

        self.play(
            TransformMatchingTex(expr, expr2),
            FadeIn(lim, 0.25 * UP, time_span=(1, 2))
        )
        self.wait()
