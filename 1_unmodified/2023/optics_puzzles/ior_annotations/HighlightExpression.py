# ==============================================================================
# Scene:      HighlightExpression
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1052-1072)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighlightExpression.py HighlightExpression -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EQUATION_T2C = {
    R"\vec{\textbf{x}}(t)": RED,
    R"\vec{\textbf{F}}(t)": YELLOW,
    R"\vec{\textbf{a}}(t)": YELLOW,
    R"\frac{d^2 \vec{\textbf{x}}}{dt^2}(t) ": YELLOW,
    R"\vec{\textbf{E}}_0": BLUE,
    R"\omega_r": PINK,
    R"\omega_l": TEAL,
}


class HighlightExpression(InteractiveScene):
    def construct(self):
        # Test
        expr = Tex(
            R"""
                \vec{\textbf{x}}(t) = 
                \frac{q ||\vec{\textbf{E}}_0||}{m\left(\omega_r^2-\omega_l^2\right)}
                \cos(\omega_l t)
            """,
            t2c=EQUATION_T2C
        )
        expr.to_edge(UP)
        rect1 = SurroundingRectangle(expr[R"\omega_r^2-\omega_l^2"])
        rect2 = SurroundingRectangle(expr[R"\frac{q ||\vec{\textbf{E}}_0||}{m\left(\omega_r^2-\omega_l^2\right)}"])

        self.add(expr)
        self.play(ShowCreation(rect1))
        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(FadeOut(rect2))
