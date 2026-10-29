# ==============================================================================
# Scene:      CalculusStatement
# Source:     videos/_2021/some1.py (lines 670-681)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CalculusStatement.py CalculusStatement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CalculusStatement(Scene):
    def construct(self):
        statement = VGroup(
            OldTexText(
                "If $f(x)$ has a local maximum or minimum\\\\"
                "at $x_0$, and $f$ is differentiable at $x_0$, then"
            ),
            OldTex("\\frac{df}{dx}(x_0) = 0.")
        )
        statement.arrange(DOWN)
        statement[1].scale(1.5, about_edge=UP).shift(0.25 * DOWN)
        self.add(statement)
