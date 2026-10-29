# ==============================================================================
# Scene:      CircleDerivativeFormula
# Source:     videos/_2026/spheres_talk/volumes.py (lines 773-787)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleDerivativeFormula.py CircleDerivativeFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleDerivativeFormula(InteractiveScene):
    def construct(self):
        # Test
        formulas = VGroup(
            Tex(tex, t2c={"dA": RED_D, "dr": BLUE})
            for tex in [
                R"dA = (2 \pi r) dr",
                R"{dA \over dr} = 2 \pi r",
            ]
        )
        formulas.scale(3)

        self.add(formulas[0])
        self.play(TransformMatchingTex(*formulas, path_arc=-90 * DEG))
        self.wait()
