# ==============================================================================
# Scene:      ContourIntegralReference
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 613-637)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ContourIntegralReference.py ContourIntegralReference -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ContourIntegralReference(InteractiveScene):
    def construct(self):
        # Test
        inv_words = Text("Inverse Laplace Transfor")
        inv_rect = SurroundingRectangle(inv_words)
        inv_rect.set_fill(BLACK, 1)
        inv_rect.set_stroke(width=0)

        contour_words = Text("Contour Integral")
        contour_words.move_to(inv_rect)

        integral = Tex(R"\int_\gamma")
        integral.next_to(contour_words, UP, MED_LARGE_BUFF)
        integral.shift(0.25 * RIGHT)
        integral_rect = SurroundingRectangle(integral)
        integral_rect.set_stroke(YELLOW, 2)

        self.add(inv_rect)
        self.play(
            Write(contour_words),
            ShowCreation(integral_rect),
            VShowPassingFlash(integral_rect.copy().insert_n_curves(100).set_stroke(YELLOW, 3)),
            run_time=2
        )
        self.wait()
