# ==============================================================================
# Scene:      TranslatedByFourier
# Source:     videos/_2022/borwein/supplements.py (lines 549-584)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TranslatedByFourier.py TranslatedByFourier -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TranslatedByFourier(InteractiveScene):
    def construct(self):
        # Two expressions
        # left_expr = Tex(R"\int_{-\infty}^\infty f(t) \cdot g(t) dt")
        # right_expr = Tex(
        #     R"\Big[ \mathcal{F}[f(t)] * \mathcal{F}[g(t)] \Big](0)",
        #     tex_to_color_map={R"\mathcal{F}": TEAL}
        # )
        left_expr = Text("Multiplication\nand\nIntegration")
        right_expr = Text("Moving averages\nand\nEvaluating at 0")
        left_expr.move_to(2 * UP).set_x(-FRAME_WIDTH / 4)
        right_expr.match_y(left_expr).set_x(FRAME_WIDTH / 4)

        equals = OldTex("=").move_to(midpoint(left_expr.get_right(), right_expr.get_left()))
        arrow = Vector(2 * RIGHT, color=TEAL)
        arrow.move_to(equals)
        arrow_label = Text("Translate to\nFourier land", font_size=24)
        arrow_label.next_to(arrow, UP)
        arrow_label.match_color(arrow)

        # brace = Brace(right_expr[:-3], UP, buff=SMALL_BUFF)
        # brace_text = OldTexText("To be explained,\\\\think ``moving average''", font_size=36)
        # brace_text.next_to(brace, UP, SMALL_BUFF)

        self.play(Write(left_expr))
        self.wait(2)
        self.play(LaggedStart(
            # Write(equals),
            GrowArrow(arrow),
            FadeIn(arrow_label, lag_ratio=0.1),
            FadeTransform(left_expr.copy(), right_expr, path_arc=-PI / 5),
            lag_ratio=0.5
        ))
        self.wait(2)
        # self.play(GrowFromCenter(brace), FadeIn(brace_text, 0.5 * UP))
        self.wait()
