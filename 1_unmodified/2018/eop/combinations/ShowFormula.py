# ==============================================================================
# Scene:      ShowFormula
# Source:     videos/_2018/eop/combinations.py (lines 3260-3282)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFormula.py ShowFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowFormula(Scene):
    def construct(self):
        specific_formula = OldTex(
            "{9 \\choose 4}", "=",
            "{9 \\cdot 8 \\cdot 7 \\cdot 6", "\\over",
            "4 \\cdot 3 \\cdot 2 \\cdot 1}"
        )
        general_formula = OldTex(
            "{n \\choose k}", "=",
            "{n \\cdot (n-1) \\cdots (n-k+1)", "\\over",
            "k \\cdot (k-1) \\cdots 2 \\cdot 1}"
        )
        for i, j in (0, 1), (2, 0), (2, 3), (2, 11):
            general_formula[i][j].set_color(BLUE)
        for i, j in (0, 2), (2, 13), (4, 0), (4, 3):
            general_formula[i][j].set_color(YELLOW)
        formulas = VGroup(specific_formula, general_formula)
        formulas.arrange(DOWN, buff = 2)
        formulas.to_edge(UP)

        self.play(FadeIn(specific_formula))
        self.play(FadeIn(general_formula))
        self.wait(3)
