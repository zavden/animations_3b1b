# ==============================================================================
# Scene:      NewtonRuleLabel
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1101-1113)
# Category:   1 · Renders unmodified
# Includes code copied from: _2021/newton_fractal.py
#
# Run from this folder:
#     manimgl NewtonRuleLabel.py NewtonRuleLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2021/newton_fractal.py -----

def get_newton_rule(font_size=36, var="z", **kwargs):
    terms = [f"{var}_n", f"{var}_{{n + 1}}"]
    t0, t1 = terms
    return OldTex(
        t1, "=", t0, "-",
        "{P(", t0, ")", "\\over ", "P'(", t0, ")}",
        font_size=36,
        **kwargs
    )



# ----- From _2021/holomorphic_dynamics.py -----

class NewtonRuleLabel(Scene):
    def construct(self):
        rule = get_newton_rule()
        rule.scale(1.5)
        rule.set_stroke(BLACK, 5, background=True)
        rule.to_corner(UL)

        box = SurroundingRectangle(rule, buff=0.2)
        box.set_fill(BLACK, 0.9)
        box.set_stroke(WHITE, 1)
        VGroup(box, rule).to_corner(UL, buff=0)

        self.add(box, rule)
