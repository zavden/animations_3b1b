# ==============================================================================
# Scene:      DistanceApproximation
# Source:     videos/_2024/holograms/supplements.py (lines 757-780)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DistanceApproximation.py DistanceApproximation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DistanceApproximation(InteractiveScene):
    def construct(self):
        # Test
        expr = Tex(R"\sqrt{L^2 + x^2} \approx L + \frac{x^2}{2L}")
        expr.to_corner(UL)

        circle = SurroundingRectangle(expr[R"\frac{x^2}{2L}"])
        circle.round_corners()
        circle.set_stroke(RED)
        words = Text("First order\nTaylor approx.")
        words.next_to(circle, DOWN, LARGE_BUFF)
        words.set_color(RED)
        words.set_backstroke(BLACK, 5)
        arrow = Arrow(words.get_top(), circle.get_bottom())
        arrow.set_color(RED)

        self.play(Write(expr))
        self.wait()
        self.play(
            ShowCreation(circle),
            GrowArrow(arrow),
            FadeIn(words)
        )
        self.wait()
