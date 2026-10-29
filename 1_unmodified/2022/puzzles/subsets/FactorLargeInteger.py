# ==============================================================================
# Scene:      FactorLargeInteger
# Source:     videos/_2022/puzzles/subsets.py (lines 5369-5396)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FactorLargeInteger.py FactorLargeInteger -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FactorLargeInteger(InteractiveScene):
    def construct(self):
        p_value = 314159265359
        q_value = 271828182863
        p, q, N = [
            Tex("{:,}".format(value).replace(",", "{,}"))
            for value in (p_value, q_value, p_value * q_value)
        ]
        p.set_color(TEAL)
        q.set_color(BLUE)
        N.to_edge(UP)
        eq = Tex("=", font_size=72).rotate(90 * DEGREES)
        eq.next_to(N, DOWN)
        prod = VGroup(p, Tex('\\times'), q)
        prod.arrange(RIGHT, buff=MED_SMALL_BUFF)
        prod.next_to(eq, DOWN)

        self.play(FadeIn(N))
        self.wait()
        self.play(
            LaggedStart(
                TransformMatchingShapes(N.copy(), p.copy()),
                Write(prod[1]),
                TransformMatchingShapes(N.copy(), q.copy()),
                lag_ratio=0.5,
            )
        )
        self.wait()
