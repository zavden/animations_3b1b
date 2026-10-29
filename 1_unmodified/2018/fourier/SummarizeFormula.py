# ==============================================================================
# Scene:      SummarizeFormula
# Source:     videos/_2018/fourier.py (lines 3782-3822)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SummarizeFormula.py SummarizeFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SummarizeFormula(Scene):
    def construct(self):
        expression = self.get_expression()
        screen_rect = ScreenRectangle(height = 5)
        screen_rect.to_edge(DOWN)

        exp_rect, g_exp_rect, int_rect = [
            SurroundingRectangle(VGroup(
                expression.get_part_by_tex(p1),
                expression.get_part_by_tex(p2),
            ))
            for p1, p2 in [("e", "t}"), ("g({}", "t}"), ("\\int", "dt")]
        ]

        self.add(expression)
        self.wait()
        self.play(
            ShowCreation(screen_rect),
            ShowCreation(exp_rect),
        )
        self.wait(2)
        self.play(Transform(exp_rect, g_exp_rect))
        self.wait(2)
        self.play(Transform(exp_rect, int_rect))
        self.wait(2)

    def get_expression(self):
        expression = OldTex(
            "\\hat g(", "f", ")", "=", "\\int", "_{t_1}", "^{t_2}",
            "g({}", "t", ")", "e", "^{-2\\pi i", "f", "t}", "dt"
        )
        expression.set_color_by_tex(
            "t", YELLOW, substring = False,
        )
        expression.set_color_by_tex("t}", YELLOW)
        expression.set_color_by_tex(
            "f", RED, substring = False,
        )
        expression.scale(1.2)
        expression.to_edge(UP)
        return expression
