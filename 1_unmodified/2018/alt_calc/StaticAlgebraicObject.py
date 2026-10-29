# ==============================================================================
# Scene:      StaticAlgebraicObject
# Source:     videos/_2018/alt_calc.py (lines 3322-3359)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StaticAlgebraicObject.py StaticAlgebraicObject -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

def get_nested_one_plus_one_over_x(n_terms, bottom_term="x"):
    tex = "1+ {1 \\over" * n_terms + bottom_term + "}" * n_terms
    return OldTex(tex, isolate=["1", "\\over", bottom_term])


def get_phi_continued_fraction(n_terms):
    return get_nested_one_plus_one_over_x(n_terms, bottom_term="1+\\cdots")


class StaticAlgebraicObject(Scene):
    def construct(self):
        frac = get_phi_continued_fraction(40)
        frac.set_width(FRAME_WIDTH - 1)
        # frac.shift(2 * DOWN)
        frac.to_edge(DOWN)
        frac.set_stroke(WHITE, width=0.5)

        title = OldTex(
            "\\infty \\ne \\lim",
            tex_to_color_map={"\\ne": RED}
        )
        title.scale(1.5)
        title.to_edge(UP)

        polynomial = OldTex("x^2 - x - 1 = 0")
        polynomial.move_to(title)

        self.add(title)
        self.play(LaggedStartMap(
            GrowFromCenter, frac,
            lag_ratio=0.1,
            run_time=3
        ))
        self.wait()
        factor = 1.1
        self.play(frac.scale, factor, run_time=0.5)
        self.play(
            frac.scale, 1 / factor,
            frac.set_color, GREY_B,
            run_time=0.5, rate_func=lambda t: t**5,
        )
        self.wait()
        self.play(
            FadeOut(title),
            FadeIn(polynomial)
        )
        self.wait(2)
