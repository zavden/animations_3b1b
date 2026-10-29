# ==============================================================================
# Scene:      WriteLikelihoodFunction
# Source:     videos/_2020/beta/beta1.py (lines 3341-3366)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl WriteLikelihoodFunction.py WriteLikelihoodFunction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"



# ----- From _2020/beta/beta1.py -----

class WriteLikelihoodFunction(Scene):
    def construct(self):
        formula = OldTex(
            "f({s}) = (\\text{const.})",
            "{s}^{\\#" + CMARK_TEX + "}",
            "(1 - {s})^{\\#" + XMARK_TEX, "}",
            tex_to_color_map={
                "{s}": YELLOW,
                "\\#" + CMARK_TEX: GREEN,
                "\\#" + XMARK_TEX: RED,
            }
        )
        formula.scale(2)

        rect1 = SurroundingRectangle(formula[3:6])
        rect2 = SurroundingRectangle(formula[6:])

        self.play(FadeInFromDown(formula))
        self.wait()
        self.play(ShowCreationThenFadeOut(rect1))
        self.wait()
        self.play(ShowCreationThenFadeOut(rect2))
        self.wait()

        self.add(formula)
        self.embed()
