# ==============================================================================
# Scene:      BothPositiveNumbers
# Source:     videos/_2025/laplace/prequel_equations.py (lines 885-900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BothPositiveNumbers.py BothPositiveNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BothPositiveNumbers(InteractiveScene):
    def construct(self):
        tex = Tex("k / m")
        self.add(tex)

        # Test
        rects = VGroup(SurroundingRectangle(tex[c], buff=0.05) for c in "km")
        rects.set_stroke(GREEN, 3)
        plusses = VGroup(Tex(R"+").next_to(rect, DOWN, SMALL_BUFF) for rect in rects)
        plusses.set_fill(GREEN)

        self.play(
            LaggedStartMap(ShowCreation, rects, lag_ratio=0.5),
            LaggedStartMap(FadeIn, plusses, shift=0.25 * DOWN, lag_ratio=0.5)
        )
        self.wait()
