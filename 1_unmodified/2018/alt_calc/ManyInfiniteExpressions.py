# ==============================================================================
# Scene:      ManyInfiniteExpressions
# Source:     videos/_2018/alt_calc.py (lines 3577-3610)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyInfiniteExpressions.py ManyInfiniteExpressions -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

def get_nested_one_plus_one_over_x(n_terms, bottom_term="x"):
    tex = "1+ {1 \\over" * n_terms + bottom_term + "}" * n_terms
    return OldTex(tex, isolate=["1", "\\over", bottom_term])


def get_phi_continued_fraction(n_terms):
    return get_nested_one_plus_one_over_x(n_terms, bottom_term="1+\\cdots")


class ManyInfiniteExpressions(Scene):
    def construct(self):
        frac = get_phi_continued_fraction(10)
        frac.set_height(2)
        frac.to_corner(UL)

        n = 9
        radical_str_parts = [
            "%d + \\sqrt{" % d
            for d in range(1, n + 1)
        ]
        radical_str_parts += ["\\cdots"]
        radical_str_parts += ["}"] * n
        radical = OldTex("".join(radical_str_parts))
        radical.to_corner(UR)
        radical.to_edge(DOWN)
        radical.set_color_by_gradient(YELLOW, RED)

        n = 12
        power_tower = OldTex(
            *["\\sqrt{2}^{"] * n + ["\\dots"] + ["}"] * n
        )
        power_tower.to_corner(UR)
        power_tower.set_color_by_gradient(BLUE, GREEN)

        self.play(*[
            LaggedStartMap(
                GrowFromCenter, group,
                lag_ratio=0.1,
                run_time=8,
            )
            for group in (frac, radical, power_tower)
        ])
        self.wait(2)
