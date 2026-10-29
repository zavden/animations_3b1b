# ==============================================================================
# Scene:      InvertArrow
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 396-415)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InvertArrow.py InvertArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InvertArrow(InteractiveScene):
    def construct(self):
        # Add arrow
        arrow = Vector(1.5 * RIGHT, thickness=4)
        arrow.set_fill(border_width=2)
        label = Tex(R"\mathcal{L}", font_size=48)
        label.next_to(arrow, UP, SMALL_BUFF)
        inv_label = Tex(R"\mathcal{L}^{-1}")
        inv_label.next_to(arrow, DOWN, buff=0)

        self.play(
            GrowArrow(arrow),
            FadeIn(label, 0.5 * RIGHT)
        )
        self.wait()
        self.play(
            Rotate(arrow, PI),
            ReplacementTransform(label, inv_label)
        )
        self.wait()
