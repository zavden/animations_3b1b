# ==============================================================================
# Scene:      PreviewExplicitCalculation
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 256-354)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewExplicitCalculation.py PreviewExplicitCalculation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PreviewExplicitCalculation(InteractiveScene):
    def construct(self):
        # Title
        goal = Text("Goal: Compute a convolution between two Gaussian functions")
        goal.set_width(FRAME_WIDTH - 1)
        goal.to_edge(UP)
        conv_word = goal["convolution"]
        gauss_word = goal["Gaussian"]

        self.add(goal)

        # Convolution
        conv_color = BLUE
        tex_kw = dict(
            t2c={"{f}": BLUE, "{g}": TEAL, R"\sigma_1": RED, R"\sigma_2": RED_B},
            font_size=42,
        )
        conv_eq = Tex(R"[{f} * {g}](s) = \int_{-\infty}^\infty {f}(x){g}(s - x)dx", **tex_kw)
        conv_eq.next_to(goal, DOWN, buff=1.5)
        conv_eq.to_edge(LEFT)
        conv_arrow = Arrow(conv_word.get_bottom(), conv_eq.get_top() + SMALL_BUFF * UP)
        conv_arrow.set_color(conv_color)

        self.play(LaggedStart(
            FlashAround(conv_word, time_width=1.5, run_time=2.0, color=conv_color),
            conv_word.animate.set_color(conv_color),
            GrowArrow(conv_arrow),
            FadeTransform(conv_word.copy(), conv_eq),
            lag_ratio=0.2,
        ))
        self.wait()

        # Gaussian
        gauss_color = RED
        gaussian1 = Tex(
            R"f(x) = {1 \over \sigma_1 \sqrt{2 \pi}} e^{-x^2 / 2 \sigma_1^2}",
            **tex_kw
        )
        gaussian2 = Tex(
            R"g(y) = {1 \over \sigma_2 \sqrt{2 \pi}} e^{-y^2 / 2 \sigma_2^2}",
            **tex_kw
        )
        gaussian1.match_y(conv_eq)
        gaussian1.to_edge(RIGHT)
        gaussian2.next_to(gaussian1, DOWN, LARGE_BUFF)
        gauss_arrow = Arrow(gauss_word.get_bottom(), gaussian1.get_top() + SMALL_BUFF * UP)
        gauss_arrow.set_color(gauss_color)
        f_rect = SurroundingRectangle(conv_eq["{f}(x)"], buff=0.05)
        g_rect = SurroundingRectangle(conv_eq["{g}(s - x)"], buff=0.05)
        f_rect.set_stroke(RED, 5)
        g_rect.set_stroke(RED, 5)

        self.play(
            ShowCreation(f_rect),
            FadeTransform(gauss_word.copy(), gaussian1),
            GrowArrow(gauss_arrow),
            gauss_word.animate.set_color(gauss_color),
        )
        self.wait()
        self.play(
            ReplacementTransform(f_rect, g_rect),
            FadeIn(gaussian2, DOWN),
        )
        self.wait()
        self.play(FadeOut(g_rect))
        self.wait()

        # Combine
        full_expr = Tex(R"""
            \int_{-\infty}^\infty
            \frac{1}{2\pi \sigma_1 \sigma_2}
            e^{-x^2 / 2\sigma_1^2} e^{-(s-x)^2 / 2\sigma_2^2} \,dx
        """, **tex_kw)
        full_expr.next_to(conv_eq, DOWN, buff=2.0, aligned_edge=LEFT)
        full_expr_rect = SurroundingRectangle(full_expr)
        full_expr_rect.set_stroke(RED_E, 2)
        arrow_kw = dict(stroke_width=2, stroke_color=RED_E)
        arrows = VGroup(*(
            Arrow(conv_eq, full_expr_rect, **arrow_kw),
            Arrow(gaussian1.get_left(), full_expr_rect, **arrow_kw),
            Arrow(gaussian2.get_left(), full_expr_rect.get_right(), **arrow_kw),
        ))

        self.play(
            LaggedStart(*(
                TransformMatchingShapes(conv_eq[9:13].copy(), full_expr[R"\int_{-\infty}^\infty"][0]),
                TransformMatchingShapes(
                    VGroup(*gaussian1[5:13], gaussian2[5:13]).copy(),
                    full_expr[R"\frac{1}{2\pi \sigma_1 \sigma_2}"][0]
                ),
                TransformMatchingShapes(gaussian1[13:].copy(), full_expr[R"e^{-x^2 / 2\sigma_1^2}"][0]),
                TransformMatchingShapes(gaussian2[13:].copy(), full_expr[R"e^{-(s-x)^2 / 2\sigma_2^2}"][0]),
                TransformMatchingShapes(conv_eq[-2:].copy(), full_expr[R"dx"]),
            ), run_time=3, lag_ratio=0.1),
            LaggedStartMap(GrowArrow, arrows),
        )
        self.play(ShowCreation(full_expr_rect))
        self.add(full_expr)
        self.wait(3)
