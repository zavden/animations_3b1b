# ==============================================================================
# Scene:      DerivativeLimitReciprocity
# Source:     videos/_2017/eoc/chapter7.py (lines 2427-2443)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DerivativeLimitReciprocity.py DerivativeLimitReciprocity -w -m --fps 15
# ==============================================================================

# -*- coding: utf-8 -*-
from manim_imports_ext import *

class DerivativeLimitReciprocity(Scene):
    def construct(self):
        arrow = Arrow(LEFT, RIGHT, color = WHITE)
        lim = OldTex("\\lim", "_{h", "\\to 0}")
        lim.set_color_by_tex("h", GREEN)
        lim.next_to(arrow, LEFT)
        deriv = OldTex("{df", "\\over\\,", "dx}")
        deriv.set_color_by_tex("dx", GREEN)
        deriv.set_color_by_tex("df", YELLOW)
        deriv.next_to(arrow, RIGHT)

        self.play(FadeIn(lim, lag_ratio = 0.5))
        self.play(ShowCreation(arrow))
        self.play(FadeIn(deriv, lag_ratio = 0.5))
        self.wait()
        self.play(Rotate(arrow, np.pi, run_time = 2))
        self.wait()
