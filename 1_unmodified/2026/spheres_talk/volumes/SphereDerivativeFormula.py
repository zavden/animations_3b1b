# ==============================================================================
# Scene:      SphereDerivativeFormula
# Source:     videos/_2026/spheres_talk/volumes.py (lines 866-880)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereDerivativeFormula.py SphereDerivativeFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereDerivativeFormula(InteractiveScene):
    def construct(self):
        # Test
        formulas = VGroup(
            Tex(tex, t2c={"dV": RED_D, "{r}": BLUE})
            for tex in [
                R"dV = (4 \pi {r}^2) d{r}",
                R"{dV \over d{r}} = 4 \pi {r}^2",
            ]
        )
        formulas.scale(3)

        self.add(formulas[0])
        self.play(TransformMatchingTex(*formulas, path_arc=-90 * DEG))
        self.wait()
