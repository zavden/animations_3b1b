# ==============================================================================
# Scene:      CylinderIntegral
# Source:     videos/_2023/gauss_int/integral.py (lines 894-1005)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CylinderIntegral.py CylinderIntegral -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CylinderIntegral(InteractiveScene):
    def construct(self):
        # Set up equations
        kw = dict(
            font_size=48,
            t2c={
                "{r}": RED,
                "{0}": RED,
                R"{\infty}": RED,
            }
        )
        exprs = VGroup(
            Tex(R"\int_0^\infty 2\pi {r} \cdot e^{-{r}^2} \, d{r}", **kw),
            Tex(R"\pi \int_0^\infty 2 {r} \cdot e^{-{r}^2}\,  d{r}", **kw),
            Tex(R"= \pi \left[ -e^{-{\infty}^2} - \left(-e^{-{0}^2} \right) \right]", **kw),
            Tex(R"= \pi", **kw),
        )
        exprs[1:].arrange(RIGHT, buff=SMALL_BUFF)
        exprs[1:].to_corner(UL)
        exprs[0].move_to(exprs[1], LEFT)

        # Factor out
        self.add(exprs[0])
        self.wait()
        self.play(TransformMatchingTex(*exprs[:2], run_time=1, path_arc=30 * DEGREES))
        self.wait()

        # Show antiderivative
        integrand = exprs[1][R"2 {r} \cdot e^{-{r}^2}"]
        integrand_rect = SurroundingRectangle(integrand, buff=SMALL_BUFF)
        integrand_rect.set_stroke(YELLOW, 2)
        anti_derivative = Tex(R"-e^{-{r}^2}", **kw)
        anti_derivative.next_to(integrand_rect, DOWN, buff=1.5)
        arrow = Arrow(anti_derivative, integrand_rect)
        arrow.set_color(YELLOW)
        arrow_label = Tex(R"d \over d{r}", **kw)
        arrow_label.scale(0.75)
        arrow_label.next_to(arrow, RIGHT, MED_SMALL_BUFF)

        self.play(
            ShowCreation(integrand_rect),
            GrowArrow(arrow),
            FadeIn(arrow_label, UP),
        )
        self.wait()
        self.play(TransformMatchingShapes(integrand.copy(), anti_derivative))
        self.wait()

        # Evaluate
        self.play(
            Write(exprs[2]["="]),
            TransformFromCopy(exprs[1][R"\pi"], exprs[2][R"\pi"]),
            TransformFromCopy(exprs[1][R"\int"], exprs[2][R"["]),
            TransformFromCopy(exprs[1][R"\int"], exprs[2][R"]"]),
        )
        self.wait()
        self.play(LaggedStart(
            FadeTransform(anti_derivative.copy(), exprs[2][R"-e^{-{\infty}^2}"]),
            FadeIn(VGroup(*exprs[2][R"- \left("], exprs[2][R"\right)"])),
            FadeTransform(anti_derivative.copy(), exprs[2][R"-e^{-{0}^2}"]),
            lag_ratio=0.7
        ))

        self.play(
            TransformMatchingShapes(
                VGroup(
                    *exprs[1][R"\pi \int_0^\infty"],
                    *anti_derivative
                ).copy(),
                exprs[2]
            )
        )
        self.wait()
        self.play(TransformMatchingTex(exprs[2].copy(), exprs[3]))
        self.wait()

        # Simplify
        rects = VGroup(
            SurroundingRectangle(exprs[2][R"-e^{-{\infty}^2}"]),
            SurroundingRectangle(exprs[2][R"-e^{-{0}^2}"]),
        )
        rects.set_stroke(TEAL, 1)
        values = VGroup(*map(Integer, [0, -1]))
        for value, rect in zip(values, rects):
            value.next_to(rect, DOWN)
            value.match_color(rect)

        zero, one = values

        self.play(
            TransformFromCopy(integrand_rect, rects[0]),
            integrand_rect.animate.set_stroke(YELLOW, 1, 0.5)
        )
        self.play(FadeIn(zero, 0.5 * DOWN))
        self.wait()
        self.play(TransformFromCopy(*rects))
        self.play(FadeIn(one, 0.5 * DOWN))
        self.wait()
        self.play(Write(exprs[3]))
        self.wait()

        # Highlight answer
        answer = exprs[3][R"\pi"]
        self.play(
            LaggedStartMap(FadeOut, VGroup(
                integrand_rect, arrow, arrow_label, anti_derivative,
                *rects, *values
            )),
            answer.animate.scale(2, about_edge=LEFT)
        )
        self.play(FlashAround(answer, run_time=2, time_width=1.5, color=TEAL))
        self.wait()
