# ==============================================================================
# Scene:      EulersFormula
# Source:     videos/_2020/ldm.py (lines 767-778)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EulersFormula.py EulersFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EulersFormula(Scene):
    def construct(self):
        kw = {"tex_to_color_map": {"\\theta": YELLOW}}
        formula = OldTex(
            "&e^{i\\theta} = \\\\ &\\cos\\left(\\theta\\right) + i\\cdot\\sin\\left(\\theta\\right)",
        )[0]
        formula[:4].scale(2, about_edge=UL)
        formula[:4].shift(SMALL_BUFF * RIGHT + MED_LARGE_BUFF * UP)
        VGroup(formula[2], formula[8], formula[17]).set_color(YELLOW)
        formula.scale(1.5)
        formula.set_stroke(BLACK, 5, background=True)
        self.add(formula)
